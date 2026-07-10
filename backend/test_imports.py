import subprocess
import sys
from pathlib import Path


def test_database_module_imports_from_repo_root():
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-c", "from backend.src.integrations.database import init_db; print('ok')"],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
