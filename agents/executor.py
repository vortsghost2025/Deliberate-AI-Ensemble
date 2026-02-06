"""
Execution Agent
Handles trade execution with paper trading mode by default.
Tracks simulated positions and performance.
Supports live trading via KuCoin API integration.
"""

from typing import Any, Dict, Optional, List
from datetime import datetime
import logging
from enum import Enum
import os

from .base_agent import BaseAgent, AgentStatus

# KuCoin API client (optional import)
try:
    from kucoin.client import Client as KuCoinClient
    KUCOIN_AVAILABLE = True
except ImportError:
    KUCOIN_AVAILABLE = False
    KuCoinClient = None


class TradeStatus(Enum):
    """Status of a trade."""
    OPEN = "open"
    CLOSED = "closed"
    PENDING = "pending"
    CANCELLED = "cancelled"


class ExecutionAgent(BaseAgent):
    """
    Execution Agent: Handles trade execution and position tracking.
    
    Responsibilities:
    - Execute trades (paper trading by default)
    - Track open positions
    - Monitor profit/loss on positions
    - Close positions when profit targets or stops are hit
    - Generate performance reports
    - Ready for future live trading integration
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the execution agent."""
        super().__init__("ExecutionAgent", config)
        self.paper_trading = config.get('paper_trading', True) if config else True
        self.live_mode = config.get('live_mode', False) if config else False
        self.exchange = config.get('exchange') if config else None
        self.order_type = config.get('order_type', 'market') if config else 'market'
        self.slippage_tolerance_percent = config.get('slippage_tolerance_percent') if config else None
        self.min_balance_usd = config.get('min_balance_usd') if config else None
        self.max_position_size_usd = config.get('max_position_size_usd') if config else None
        self.max_trade_loss_usd = config.get('max_trade_loss_usd') if config else None
        self.max_daily_loss_usd = config.get('max_daily_loss_usd') if config else None
        configured_max_open_positions = config.get('max_open_positions') if config else None
        if configured_max_open_positions is None:
            self.max_open_positions = 1
        else:
            self.max_open_positions = min(configured_max_open_positions, 1)
        configured_max_trades = config.get('max_trades_per_session') if config else None
        if configured_max_trades is None:
            self.max_trades_per_session = 2
        else:
            self.max_trades_per_session = min(configured_max_trades, 2)

        self.open_positions: List[Dict[str, Any]] = []
        self.closed_trades: List[Dict[str, Any]] = []
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        
        # KuCoin client initialization for live trading
        self.kucoin_client = None
        if self.live_mode and not self.paper_trading:
            self._initialize_kucoin_client(config)

    def _initialize_kucoin_client(self, config: Dict[str, Any]) -> None:
        """Initialize KuCoin API client for live trading."""
        if not KUCOIN_AVAILABLE:
            raise RuntimeError(
                "KuCoin library not installed. Run: pip install python-kucoin"
            )
        
        # Get credentials from config or environment
        api_key = config.get('api_key') or os.getenv('KUCOIN_API_KEY')
        api_secret = config.get('api_secret') or os.getenv('KUCOIN_API_SECRET')
        api_passphrase = config.get('api_passphrase') or os.getenv('KUCOIN_API_PASSPHRASE')
        
        if not all([api_key, api_secret, api_passphrase]):
            raise ValueError(
                "KuCoin API credentials missing. Set KUCOIN_API_KEY, "
                "KUCOIN_API_SECRET, and KUCOIN_API_PASSPHRASE in environment "
                "or pass in config."
            )
        
        try:
            self.kucoin_client = KuCoinClient(
                api_key=api_key,
                api_secret=api_secret,
                passphrase=api_passphrase
            )
            # Test connection
            self.kucoin_client.get_accounts()
            self.logger.info("✅ KuCoin API connected successfully")
        except Exception as e:
            self.logger.error(f"❌ KuCoin API connection failed: {e}")
            raise RuntimeError(f"Failed to initialize KuCoin client: {e}")

    def _get_total_pnl(self) -> float:
        return sum(t['pnl'] for t in self.closed_trades)

    def _validate_live_trade(
        self,
        entry_price: float,
        position_size: float,
        stop_loss: float,
        account_balance: Optional[float],
    ) -> Optional[str]:
        """Validate live trade against configured risk limits."""
        if self.order_type not in {'market', 'limit'}:
            return f"Unsupported order type: {self.order_type}"
        if self.max_open_positions is not None and len(self.open_positions) >= self.max_open_positions:
            return f"Max open positions reached ({self.max_open_positions})"
        if self.max_position_size_usd is not None:
            position_size_usd = entry_price * position_size
            if position_size_usd > self.max_position_size_usd:
                return f"Position size ${position_size_usd:.2f} exceeds limit ${self.max_position_size_usd:.2f}"
        if self.max_trade_loss_usd is not None and stop_loss > 0 and entry_price > 0:
            risk_per_unit = max(entry_price - stop_loss, 0)
            projected_loss = risk_per_unit * position_size
            if projected_loss > self.max_trade_loss_usd:
                return f"Projected loss ${projected_loss:.2f} exceeds limit ${self.max_trade_loss_usd:.2f}"
        if self.max_daily_loss_usd is not None:
            total_pnl = self._get_total_pnl()
            if total_pnl <= -self.max_daily_loss_usd:
                return f"Daily loss limit reached (${total_pnl:.2f} <= -${self.max_daily_loss_usd:.2f})"
        if self.min_balance_usd is not None and account_balance is not None:
            if account_balance < self.min_balance_usd:
                return f"Account balance ${account_balance:.2f} below minimum ${self.min_balance_usd:.2f}"
        return None

    def _validate_session_limits(self) -> Optional[str]:
        if self.max_trades_per_session is not None and self.total_trades >= self.max_trades_per_session:
            return f"Max trades per session reached ({self.max_trades_per_session})"
        if self.max_open_positions is not None and len(self.open_positions) >= self.max_open_positions:
            return f"Max open positions reached ({self.max_open_positions})"
        return None
    
    def _place_live_order(
        self,
        pair: str,
        side: str,
        position_size: float,
        entry_price: float,
        stop_loss: float,
        take_profit: float
    ) -> Dict[str, Any]:
        """
        Place a live order on KuCoin exchange.
        
        Args:
            pair: Trading pair (e.g., 'BTC/USDT')
            side: 'buy' or 'sell'
            position_size: Size in base currency
            entry_price: Entry price
            stop_loss: Stop loss price
            take_profit: Take profit price
            
        Returns:
            Order details including order_id
        """
        if not self.kucoin_client:
            raise RuntimeError("KuCoin client not initialized")
        
        # Convert pair format: BTC/USDT -> BTC-USDT
        symbol = pair.replace('/', '-')
        
        try:
            # Place main entry order
            if self.order_type == 'market':
                self.logger.info(f"Placing MARKET {side} order: {position_size} {symbol}")
                order = self.kucoin_client.create_market_order(
                    symbol=symbol,
                    side=side,
                    size=position_size
                )
            else:  # limit order
                self.logger.info(
                    f"Placing LIMIT {side} order: {position_size} {symbol} @ ${entry_price}"
                )
                order = self.kucoin_client.create_limit_order(
                    symbol=symbol,
                    side=side,
                    price=str(entry_price),
                    size=str(position_size)
                )
            
            order_id = order['orderId']
            self.logger.info(f"✅ Order placed successfully: {order_id}")
            
            # Place stop-loss order (conditional)
            stop_order_id = None
            if stop_loss > 0:
                try:
                    stop_side = 'sell' if side == 'buy' else 'buy'
                    stop_order = self.kucoin_client.create_stop_order(
                        symbol=symbol,
                        side=stop_side,
                        stop='loss',
                        stopPrice=str(stop_loss),
                        size=str(position_size),
                        price=str(stop_loss * 0.99)  # Slightly below stop for market
                    )
                    stop_order_id = stop_order.get('orderId')
                    self.logger.info(f"✅ Stop-loss order placed: {stop_order_id} @ ${stop_loss}")
                except Exception as e:
                    self.logger.warning(f"⚠️ Failed to place stop-loss order: {e}")
            
            # Place take-profit order (conditional)
            tp_order_id = None
            if take_profit > 0:
                try:
                    tp_side = 'sell' if side == 'buy' else 'buy'
                    tp_order = self.kucoin_client.create_limit_order(
                        symbol=symbol,
                        side=tp_side,
                        price=str(take_profit),
                        size=str(position_size)
                    )
                    tp_order_id = tp_order.get('orderId')
                    self.logger.info(f"✅ Take-profit order placed: {tp_order_id} @ ${take_profit}")
                except Exception as e:
                    self.logger.warning(f"⚠️ Failed to place take-profit order: {e}")
            
            return {
                'order_id': order_id,
                'stop_order_id': stop_order_id,
                'tp_order_id': tp_order_id,
                'symbol': symbol,
                'side': side,
                'size': position_size,
                'price': entry_price
            }
            
        except Exception as e:
            self.logger.error(f"❌ Live order placement failed: {e}")
            raise RuntimeError(f"Failed to place live order: {e}")
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute trade order.
        
        Args:
            input_data: Contains market_data, position_size, stop_loss, take_profit
            
        Returns:
            Message with execution result
        """
        self.log_execution_start("execute_trade")
        
        try:
            market_data = input_data.get('market_data', {})
            position_size = input_data.get('position_size', 0)
            stop_loss = input_data.get('stop_loss', 0)
            take_profit = input_data.get('take_profit', 0)
            paper_trading = input_data.get('paper_trading', self.paper_trading)
            account_balance = input_data.get('account_balance')
            position_approved = input_data.get('position_approved', None)
            risk_approved = input_data.get('risk_approved', None)

            if position_approved is False or risk_approved is False:
                self.log_execution_end("execute_trade", success=True)
                return self.create_message(
                    action='execute_trade',
                    success=True,
                    data={'trade_executed': False, 'reason': 'Risk approval required'}
                )
            
            if not market_data or position_size <= 0:
                self.log_execution_end("execute_trade", success=True)
                return self.create_message(
                    action='execute_trade',
                    success=True,
                    data={'trade_executed': False, 'reason': 'Invalid position size'}
                )

            session_limit_reason = self._validate_session_limits()
            if session_limit_reason:
                self.logger.warning(session_limit_reason)
                self.log_execution_end("execute_trade", success=True)
                return self.create_message(
                    action='execute_trade',
                    success=True,
                    data={'trade_executed': False, 'reason': session_limit_reason}
                )
            
            # Get first pair for execution (simplified)
            pair = list(market_data.keys())[0]
            market_info = market_data[pair]
            entry_price = market_info.get('current_price', 0)

            if self.live_mode and not paper_trading:
                rejection_reason = self._validate_live_trade(
                    entry_price=entry_price,
                    position_size=position_size,
                    stop_loss=stop_loss,
                    account_balance=account_balance,
                )
                if rejection_reason:
                    self.logger.warning(f"Live trade rejected: {rejection_reason}")
                    self.log_execution_end("execute_trade", success=True)
                    return self.create_message(
                        action='execute_trade',
                        success=True,
                        data={
                            'trade_executed': False,
                            'reason': rejection_reason
                        }
                    )
            
            # Place live order if not paper trading
            order_details = None
            if not paper_trading and self.live_mode:
                try:
                    self.logger.warning(
                        f"🔴 LIVE TRADING ACTIVATED - Placing real order on KuCoin"
                    )
                    order_details = self._place_live_order(
                        pair=pair,
                        side='buy',
                        position_size=position_size,
                        entry_price=entry_price,
                        stop_loss=stop_loss,
                        take_profit=take_profit
                    )
                    self.logger.info(
                        f"✅ Live order executed: Order ID {order_details['order_id']}"
                    )
                except Exception as e:
                    error_msg = f"Live order failed: {str(e)}"
                    self.logger.error(f"❌ {error_msg}")
                    self.log_execution_end("execute_trade", success=False)
                    return self.create_message(
                        action='execute_trade',
                        success=False,
                        error=error_msg
                    )
            
            # Create trade record
            trade = {
                'trade_id': self.total_trades + 1,
                'pair': pair,
                'entry_price': entry_price,
                'position_size': position_size,
                'entry_value': entry_price * position_size,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'entry_time': datetime.utcnow().isoformat(),
                'status': TradeStatus.OPEN.value,
                'paper_trading': paper_trading,
                'pnl': 0,
                'pnl_pct': 0,
                'exit_price': None,
                'exit_time': None,
                'exit_reason': None,
                'order_id': order_details['order_id'] if order_details else None,
                'stop_order_id': order_details['stop_order_id'] if order_details else None,
                'tp_order_id': order_details['tp_order_id'] if order_details else None
            }
            
            # Add to open positions
            self.open_positions.append(trade)
            self.total_trades += 1
            
            self.logger.info(
                f"Trade {trade['trade_id']} {'[PAPER]' if paper_trading else '[LIVE]'} OPENED: "
                f"{pair} @ {entry_price:.4f} | Size: {position_size:.4f} | "
                f"SL: {stop_loss:.4f} | TP: {take_profit:.4f}"
            )
            
            self.log_execution_end("execute_trade", success=True)
            
            return self.create_message(
                action='execute_trade',
                success=True,
                data={
                    'trade_executed': True,
                    'trade_id': trade['trade_id'],
                    'pair': pair,
                    'entry_price': entry_price,
                    'position_size': position_size,
                    'entry_value': trade['entry_value'],
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'paper_trading': paper_trading,
                    'open_positions_count': len(self.open_positions)
                }
            )
        
        except Exception as e:
            error_msg = f"Trade execution error: {str(e)}"
            self.set_status(AgentStatus.ERROR, error_msg)
            self.log_execution_end("execute_trade", success=False)
            return self.create_message(
                action='execute_trade',
                success=False,
                error=error_msg
            )
    
    def close_position(
        self,
        trade_id: int,
        exit_price: float,
        reason: str
    ) -> Dict[str, Any]:
        """
        Close an open trade position.
        
        Args:
            trade_id: ID of trade to close
            exit_price: Price at which to close
            reason: Reason for closing (e.g., 'take_profit', 'stop_loss', 'manual')
            
        Returns:
            Closed trade information
        """
        # Find the trade
        trade = None
        for i, t in enumerate(self.open_positions):
            if t['trade_id'] == trade_id:
                trade = self.open_positions.pop(i)
                break
        
        if not trade:
            self.logger.warning(f"Trade {trade_id} not found")
            return {}
        
        # Calculate P&L
        pnl = (exit_price - trade['entry_price']) * trade['position_size']
        pnl_pct = (exit_price - trade['entry_price']) / trade['entry_price'] * 100
        
        # Update trade record
        trade['exit_price'] = exit_price
        trade['exit_time'] = datetime.utcnow().isoformat()
        trade['exit_reason'] = reason
        trade['status'] = TradeStatus.CLOSED.value
        trade['pnl'] = pnl
        trade['pnl_pct'] = pnl_pct
        
        # Move to closed trades
        self.closed_trades.append(trade)
        
        # Update statistics
        if pnl > 0:
            self.winning_trades += 1
        else:
            self.losing_trades += 1
        
        self.logger.info(
            f"Trade {trade_id} CLOSED via {reason}: "
            f"P&L: ${pnl:.2f} ({pnl_pct:+.2f}%)"
        )
        
        return trade
    
    def update_open_positions(self, current_prices: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Update P&L for all open positions based on current prices.
        
        Args:
            current_prices: Dictionary of current prices by pair
            
        Returns:
            List of closed trades (if any hit take-profit or stop-loss)
        """
        closed_trades = []
        trades_to_close = []
        
        for trade in self.open_positions:
            pair = trade['pair']
            if pair not in current_prices:
                continue
            
            current_price = current_prices[pair]
            
            # Calculate current P&L
            pnl = (current_price - trade['entry_price']) * trade['position_size']
            pnl_pct = (current_price - trade['entry_price']) / trade['entry_price'] * 100
            
            trade['pnl'] = pnl
            trade['pnl_pct'] = pnl_pct
            
            # Check if hit stop-loss or take-profit
            if current_price <= trade['stop_loss']:
                trades_to_close.append((trade['trade_id'], current_price, 'stop_loss'))
            elif current_price >= trade['take_profit']:
                trades_to_close.append((trade['trade_id'], current_price, 'take_profit'))
        
        # Close trades that hit targets
        for trade_id, exit_price, reason in trades_to_close:
            closed = self.close_position(trade_id, exit_price, reason)
            closed_trades.append(closed)
        
        return closed_trades
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary of all trades."""
        if self.total_trades == 0:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'total_pnl': 0,
                'avg_pnl': 0,
                'open_positions': 0,
                'max_win': 0,
                'max_loss': 0
            }
        
        # Calculate statistics
        total_pnl = sum(t['pnl'] for t in self.closed_trades)
        max_win = max((t['pnl'] for t in self.closed_trades), default=0)
        max_loss = min((t['pnl'] for t in self.closed_trades), default=0)
        
        return {
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades,
            'win_rate': self.winning_trades / self.total_trades if self.total_trades > 0 else 0,
            'total_pnl': total_pnl,
            'avg_pnl': total_pnl / self.total_trades if self.total_trades > 0 else 0,
            'open_positions': len(self.open_positions),
            'max_win': max_win,
            'max_loss': max_loss
        }
    
    def get_open_positions(self) -> List[Dict[str, Any]]:
        """Get list of currently open positions."""
        return self.open_positions.copy()
    
    def get_trade_history(self) -> List[Dict[str, Any]]:
        """Get history of all closed trades."""
        return self.closed_trades.copy()
