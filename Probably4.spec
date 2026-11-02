# Build from the repository root: uv run --locked --group build pyinstaller Probably4.spec
from pathlib import Path
import tomllib

from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.win32.versioninfo import (
    FixedFileInfo, StringFileInfo, StringStruct, StringTable,
    VarFileInfo, VarStruct, VSVersionInfo,
)

root = Path(SPECPATH)
project = tomllib.loads((root / "pyproject.toml").read_text("utf-8"))["project"]
version = project["version"]
version_tuple = tuple(map(int, version.split("."))) + (0,)
version_info = VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=version_tuple, prodvers=version_tuple,
        mask=0x3f, flags=0, OS=0x40004, fileType=1, subtype=0, date=(0, 0),
    ),
    kids=[
        StringFileInfo([StringTable("040904B0", [
            StringStruct("CompanyName", "ivanpono-prog"),
            StringStruct("FileDescription", "Probably 4 desktop calculator"),
            StringStruct("FileVersion", version),
            StringStruct("InternalName", "Probably4"),
            StringStruct("LegalCopyright", "Copyright (c) 2026 ivanpono-prog"),
            StringStruct("OriginalFilename", "Probably4.exe"),
            StringStruct("ProductName", "Probably 4"),
            StringStruct("ProductVersion", version),
        ])]),
        VarFileInfo([VarStruct("Translation", [1033, 1200])]),
    ],
)
a = Analysis(
    [str(root / "main.py")],
    pathex=[str(root)],
    binaries=[],
    datas=[(str(root / "assets"), "assets")] + collect_data_files("customtkinter"),
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, [], exclude_binaries=True,
    name="Probably4", console=False, debug=False,
    strip=False, upx=False, version=version_info,
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="Probably4")
