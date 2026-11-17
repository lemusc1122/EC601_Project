import sys
import os
from pathlib import Path

sys.setrecursionlimit(10000)

from setuptools import setup

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
APP = [str(ROOT / "prototype.py")]

# Conda Python links _ctypes and _ssl against @rpath libraries. py2app may not
# discover these dependencies in a venv, so explicitly add the base
# interpreter's libraries to the application bundle when present.
framework_paths = []
for library in ("libffi.8.dylib", "libssl.3.dylib", "libcrypto.3.dylib"):
    candidates = (
        Path(sys.base_prefix) / "lib" / library,
        Path(sys.prefix) / "lib" / library,
    )
    library_path = next((path for path in candidates if path.is_file()), None)
    if library_path is not None:
        framework_paths.append(str(library_path))

OPTIONS = {
    "argv_emulation": False,
    "packages": [
        "PySide6",
        "shiboken6",
        "numpy",
        "matplotlib",
        "qiskit",
        "certifi",
    ],
    "includes": [
        "PySide6.QtSvg",
        "PySide6.QtTextToSpeech",
        "matplotlib.backends.backend_agg",
        "matplotlib.backends.backend_svg",
        "qiskit.visualization",
    ],
    "qt_plugins": ["platforms", "texttospeech"],
    "excludes": [],
    "plist": {
        "CFBundleName": "PrototypeApp",
        "CFBundleDisplayName": "Prototype App",
        "CFBundleIdentifier": "com.example.mypythonapp",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
    },
}
if framework_paths:
    OPTIONS["frameworks"] = framework_paths

setup(
    name="PrototypeApp",
    app=APP,
    data_files=[
        (".", ["feedback_config.json"]),
        ("assets", ["assets/WIKI_IMAGE_SOURCES_MLA.txt"]),
        ("assets/wiki", [str(path) for path in Path("assets/wiki").iterdir()
                          if path.is_file()]),
    ],
    options={"py2app": OPTIONS},
)
