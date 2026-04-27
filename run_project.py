from __future__ import annotations

import subprocess
import sys
import venv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
VENV_DIR = PROJECT_ROOT / ".venv"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"
NOTEBOOK_FILE = PROJECT_ROOT / "Analisis_Desempleo_Latinoamerica_Final.ipynb"


def venv_python() -> Path:
    if sys.platform.startswith("win"):
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def ensure_venv() -> Path:
    python_executable = venv_python()
    if python_executable.exists():
        return python_executable

    builder = venv.EnvBuilder(with_pip=True)
    builder.create(VENV_DIR)
    return python_executable


def main() -> None:
    if not REQUIREMENTS_FILE.exists():
        raise FileNotFoundError(f"No se encontró {REQUIREMENTS_FILE}")
    if not NOTEBOOK_FILE.exists():
        raise FileNotFoundError(f"No se encontró {NOTEBOOK_FILE}")

    python_executable = ensure_venv()

    subprocess.check_call([
        str(python_executable),
        "-m",
        "pip",
        "install",
        "--upgrade",
        "pip",
    ])

    subprocess.check_call([
        str(python_executable),
        "-m",
        "pip",
        "install",
        "-r",
        str(REQUIREMENTS_FILE),
    ])

    subprocess.check_call([
        str(python_executable),
        "-m",
        "jupyter",
        "lab",
        str(NOTEBOOK_FILE),
    ], cwd=str(PROJECT_ROOT))


if __name__ == "__main__":
    main()