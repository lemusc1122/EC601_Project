import sys
from pathlib import Path

sys.setrecursionlimit(10000)

from setuptools import setup

APP = ["prototype.py"]

OPTIONS = {
    "argv_emulation": False,
    "packages": [
        "PySide6",
        "shiboken6",
    ],
    "qt_plugins": [
        "platforms",
    ],
    "excludes": [],
    "plist": {
        "CFBundleName": "PrototypeApp",
        "CFBundleDisplayName": "Prototype App",
        "CFBundleIdentifier": "com.example.mypythonapp",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
    },
}

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
