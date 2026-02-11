import hashlib
from pathlib import Path

KEY_FILES = [
    "AGENT_COORDINATION/SHARED_TASK_QUEUE.md",
    "AGENT_COORDINATION/VSCODE_STATUS.md",
    "AGENT_COORDINATION/DESKTOP_STATUS.md",
]


def compute_workspace_hash() -> str:
    hasher = hashlib.sha256()
    for path_str in KEY_FILES:
        path = Path(path_str)
        if path.exists():
            hasher.update(path.read_bytes())
    return hasher.hexdigest()[:8]


if __name__ == "__main__":
    print(f"WORKSPACE_CHECKSUM={compute_workspace_hash()}")
