from pathlib import Path

from setuptools import setup  # type: ignore


APP = ["../build/study.py"]
ICON_FILE = "../assets/study-helper-icon.png"
OPTIONS = {
    "argv_emulation": False,
    "iconfile": ICON_FILE,
    "includes": [
        "tkinter",
        "tkinter.ttk",
        "pathlib",
        "json",
        "datetime",
        "collections",
        "collections.abc",
        "csv",
        "copy",
    ],
    "semi_standalone": True,
    "plist": {
        "CFBundleName": "Syllabus",
        "CFBundleDisplayName": "Syllabus",
        "CFBundleIdentifier": "com.darsh.syllabus",
        "CFBundleShortVersionString": "1.0",
        "CFBundleVersion": "1",
        "LSMinimumSystemVersion": "11.0",
        "NSHighResolutionCapable": True,
    },
}


setup(
    app=APP,
    data_files=[
        ("", ["../tools/study_data.json"]),
        (
            "assets",
            ["../assets/study-helper-icon.png", "../assets/study-helper-logo.svg"],
        ),
    ],
    name="Syllabus",
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
