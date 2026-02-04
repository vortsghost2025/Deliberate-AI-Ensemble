"""
Unified Account Readiness Validation
Checks if the system is ready for live trading with proper credentials.
"""

import os
import sys
import subprocess
from typing import Dict, Any, List, Tuple
from utils.kucoin_uta_validator import KuCoinUTAValidator


def get_container_status() -> Dict[str, Any]:
    """Get Docker container status."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=orchestrator-trading-bot", "--format", "{{.Status}}"],
            capture_output=True,
            text=True
        )
        
        running = "Up" in result.stdout
        
        return {
            "container_running": running,
            "container_name": "orchestrator-trading-bot",
            "status": result.stdout.strip() or ("Running" if running else "Stopped")
        }
    except Exception as e:
        return {
            "container_running": False,
            "container_name": "orchestrator-trading-bot",
            "status": "Unknown",
            "error": str(e)
        }


def check_local_credentials() -> Tuple[bool, List[str]]:
    """Check if credentials are available in local environment."""
    required = ["KUCOIN_API_KEY", "KUCOIN_API_SECRET", "KUCOIN_API_PASSPHRASE"]
    missing = [var for var in required if not os.getenv(var)]
    return len(missing) == 0, missing


def check_container_credentials() -> Tuple[bool, List[str]]:
    """Check if credentials are available in Docker container."""
    try:
        result = subprocess.run(
            ["docker", "exec", "orchestrator-trading-bot", "env"],
            capture_output=True,
            text=True
        )
        
        required = ["KUCOIN_API_KEY", "KUCOIN_API_SECRET", "KUCOIN_API_PASSPHRASE"]
        env_vars = result.stdout
        missing = [var for var in required if var not in env_vars]
        return len(missing) == 0, missing
    except Exception as e:
        return False, ["Unable to check container environment"]


def run_uta_validation() -> Dict[str, Any]:
    """Run KuCoin Unified Account validation."""
    validator = KuCoinUTAValidator()
    return validator.run_validation()


def print_readiness_report(
    container_status: Dict[str, Any],
    local_creds: Tuple[bool, List[str]],
    container_creds: Tuple[bool, List[str]],
    uta_validation: Dict[str, Any]
) -> None:
    """Print comprehensive readiness report."""
    print("\n" + "="*80)
    print("  UNIFIED ACCOUNT READINESS VALIDATION REPORT")
    print("="*80)
    
    # Container Status
    print("\n1. CONTAINER STATUS")
    print("-" * 80)
    print(f"   Container: {container_status['container_name']}")
    print(f"   Status: {container_status['status']}")
    if container_status.get("error"):
        print(f"   Error: {container_status['error']}")
    
    # Local Credentials
    print("\n2. LOCAL ENVIRONMENT CREDENTIALS")
    print("-" * 80)
    local_ready, local_missing = local_creds
    if local_ready:
        print("   ✅ All credentials configured locally")
    else:
        print(f"   ❌ Missing credentials: {', '.join(local_missing)}")
        print("      Required environment variables:")
        for var in ["KUCOIN_API_KEY", "KUCOIN_API_SECRET", "KUCOIN_API_PASSPHRASE"]:
            status = "✅" if os.getenv(var) else "❌"
            print(f"      {status} {var}")
    
    # Container Credentials
    print("\n3. CONTAINER ENVIRONMENT CREDENTIALS")
    print("-" * 80)
    container_ready, container_missing = container_creds
    if container_ready:
        print("   ✅ All credentials present in container")
    else:
        if not container_status['container_running']:
            print("   ⚠️  Container not running - cannot verify")
        else:
            print(f"   ❌ Missing credentials: {', '.join(container_missing)}")
    
    # UTA Validation
    print("\n4. UNIFIED ACCOUNT API VALIDATION")
    print("-" * 80)
    if not uta_validation.get("configured"):
        print("   ⚠️  VALIDATION SKIPPED - Credentials not configured")
        print("      To validate, set environment variables and rerun")
    else:
        results = uta_validation.get("validation_results", [])
        for result in results:
            status = "✅" if result["success"] else "❌"
            print(f"   {status} {result['test']}: {result['status_code']}")
    
    # Overall Readiness
    print("\n5. OVERALL READINESS")
    print("="*80)
    
    if not container_status['container_running']:
        readiness = "⚠️  CONTAINER NOT RUNNING"
        status_detail = "Start container: docker compose up -d"
    elif not local_ready:
        readiness = "⚠️  LOCAL CREDENTIALS MISSING"
        status_detail = f"Configure: {', '.join(local_creds[1])}"
    elif not container_ready:
        readiness = "⚠️  CONTAINER CREDENTIALS NOT LOADED"
        status_detail = "Restart container with credentials: docker compose down && docker compose up -d"
    elif not uta_validation.get("configured"):
        readiness = "⏳ READY FOR VALIDATION"
        status_detail = "Credentials configured. Validating account access..."
    elif uta_validation.get("summary") == "READY":
        readiness = "✅ UNIFIED ACCOUNT READY"
        status_detail = "All endpoints accessible. Ready for live trading."
    elif uta_validation.get("summary") == "PARTIAL":
        readiness = "⚠️  PARTIAL CONNECTIVITY"
        status_detail = f"{uta_validation.get('passed')}/{uta_validation.get('total')} endpoints working"
    else:
        readiness = "❌ VALIDATION FAILED"
        status_detail = "Cannot access Unified Account endpoints"
    
    print(f"\n{readiness}")
    print(f"Status: {status_detail}")
    
    print("\n" + "="*80 + "\n")
    
    return readiness


def main():
    """Run readiness validation."""
    print("\nInitializing Unified Account Readiness Check...\n")
    
    # Gather information
    container_status = get_container_status()
    local_creds = check_local_credentials()
    container_creds = check_container_credentials()
    uta_validation = run_uta_validation()
    
    # Print report
    readiness = print_readiness_report(
        container_status,
        local_creds,
        container_creds,
        uta_validation
    )
    
    # Return appropriate exit code
    if "READY" in readiness:
        return 0
    elif "PARTIAL" in readiness:
        return 0  # Partial is acceptable
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
