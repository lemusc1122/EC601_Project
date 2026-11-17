"""Install the platform's build dependencies and package the desktop app."""

from __future__ import annotations

import platform
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_PYTHON = {(3, 11), (3, 12)}


def run(command: list[str], *, cwd: Path = ROOT) -> None:
    print("\n> " + " ".join(str(part) for part in command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def main() -> int:
    system = platform.system()
    if system == "Windows":
        platform_dir = "windows"
        if sys.version_info[:2] not in SUPPORTED_PYTHON:
            raise SystemExit(
                "Windows builds require Python 3.11 or 3.12 (64-bit). Start this file with "
                "'py -3.11 packaging\\build_app.py' or 'py -3.12 packaging\\build_app.py'."
            )
        python_tag = f"py{sys.version_info.major}{sys.version_info.minor}"
        venv_dir = ROOT / f".venv-windows-{python_tag}"
        python_path = venv_dir / "Scripts" / "python.exe"
        requirements = ROOT / "packaging" / "windows" / "requirements.txt"
    elif system == "Darwin":
        platform_dir = "macos"
        if sys.version_info[:2] not in SUPPORTED_PYTHON:
            raise SystemExit(
                "macOS builds require Python 3.11 or 3.12. Start this file with "
                "'python3.11 packaging/build_app.py' or 'python3.12 packaging/build_app.py'."
            )
        python_tag = f"py{sys.version_info.major}{sys.version_info.minor}"
        venv_dir = ROOT / f".venv-macos-{python_tag}"
        python_path = venv_dir / "bin" / "python"
        requirements = ROOT / "packaging" / "macos" / "requirements.txt"
    else:
        raise SystemExit(f"Building is supported on Windows and macOS, not {system}.")

    if not python_path.exists():
        run([sys.executable, "-m", "venv", str(venv_dir)])

    run([str(python_path), "-m", "pip", "install", "--upgrade", "pip"])
    # pip installs missing packages and updates packages that do not satisfy
    # these requirements, so the same entry point can be rerun safely.
    run([str(python_path), "-m", "pip", "install", "-r", str(requirements)])

    if platform_dir == "windows":
        run(
            [
                str(python_path),
                "-m",
                "PyInstaller",
                "--noconfirm",
                "--clean",
                "--windowed",
                "--onedir",
                "--name",
                "QuantumCircuitBuilder",
                "--add-data",
                "assets\\wiki;assets\\wiki",
                "--add-data",
                "feedback_config.json;.",
                "--collect-all",
                "PySide6",
                "--collect-all",
                "qiskit",
                "--collect-all",
                "matplotlib",
                "--collect-all",
                "certifi",
                "--hidden-import",
                "PySide6.QtSvg",
                "--hidden-import",
                "PySide6.QtTextToSpeech",
                "prototype.py",
            ]
        )
        output = ROOT / "dist" / "QuantumCircuitBuilder" / "QuantumCircuitBuilder.exe"
    else:
        run([str(python_path), "packaging/macos/setup.py", "py2app"])
        output = ROOT / "dist" / "PrototypeApp.app"

    print(f"\nBuild complete: {output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode) from exc
