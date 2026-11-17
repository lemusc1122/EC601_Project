"""Build the Quantum Circuit Builder as a Windows executable with py2exe.

Run this script on Windows from the repository root after installing the
project dependencies and py2exe in the same Python environment.
"""

from pathlib import Path

from setuptools import setup


ROOT = Path(__file__).resolve().parents[2]

wiki_assets = sorted(
    path for path in (ROOT / "assets" / "wiki").iterdir() if path.is_file()
)

setup(
    name="QuantumCircuitBuilder",
    version="1.0.0",
    description="Quantum Circuit Builder desktop learning prototype",
    windows=[
        {
            "script": str(ROOT / "prototype.py"),
            "dest_base": "QuantumCircuitBuilder",
        }
    ],
    data_files=[
        (".", [str(ROOT / "feedback_config.json")]),
        (
            str(Path("assets") / "wiki"),
            [str(path) for path in wiki_assets],
        ),
    ],
    options={
        "py2exe": {
            "bundle_files": 3,
            "compressed": True,
            "includes": [
                "PySide6.QtSvg",
                "PySide6.QtTextToSpeech",
                "matplotlib.backends.backend_agg",
                "matplotlib.backends.backend_svg",
                "qiskit",
                "qiskit_aer",
            ],
            "packages": [
                "PySide6",
                "shiboken6",
                "numpy",
                "matplotlib",
                "qiskit",
            ],
            "excludes": ["tkinter"],
        }
    },
)
