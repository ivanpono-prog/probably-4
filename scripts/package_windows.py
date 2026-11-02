"""Package the Windows build, preserving notices and a file hash manifest."""

import hashlib
import json
import os
import platform
import shutil
import struct
import sys
import tomllib
import zipfile
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "dist" / "Probably4"
RUNTIME_PACKAGES = ("customtkinter", "pillow", "darkdetect", "packaging")


def sha256(file):
    with file.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def copy_notice(source, target):
    if not source.is_file() or source.stat().st_size == 0:
        raise RuntimeError(f"Missing or empty license: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def font_notices(font):
    """Read OpenType name records as data, including original copyright."""
    data = font.read_bytes()
    count = struct.unpack_from(">H", data, 4)[0]
    for index in range(count):
        tag, _, offset, _ = struct.unpack_from(">4sIII", data, 12 + 16 * index)
        if tag == b"name":
            break
    else:
        raise RuntimeError(f"No font name table: {font}")
    _, count, strings = struct.unpack_from(">HHH", data, offset)
    found = set()
    for index in range(count):
        plat, _, _, name_id, size, start = struct.unpack_from(
            ">HHHHHH", data, offset + 6 + 12 * index
        )
        if name_id not in (0, 7, 8, 9, 13, 14):
            continue
        raw = data[offset + strings + start : offset + strings + start + size]
        text = raw.decode("utf-16-be" if plat in (0, 3) else "mac_roman")
        found.add((name_id, text))
    if not any(key == 0 for key, _ in found):
        raise RuntimeError(f"No font copyright record: {font}")
    return "\n\n".join(f"Name ID {key}: {text}" for key, text in sorted(found))


def main():
    if sys.platform != "win32" or struct.calcsize("P") != 8:
        raise RuntimeError("Build on 64-bit Windows")
    project = tomllib.loads((ROOT / "pyproject.toml").read_text("utf-8"))["project"]
    version = project["version"]
    required = ["Probably4.exe", "_internal/python313.dll", "_internal/assets/logo.png"]
    for name in required:
        if not (BUNDLE / name).is_file():
            raise RuntimeError(f"Missing bundle file: {name}")
    copy_notice(ROOT / "LICENSE", BUNDLE / "LICENSE")
    copy_notice(ROOT / "README.md", BUNDLE / "README.md")
    copy_notice(ROOT / "THIRD_PARTY_NOTICES.md", BUNDLE / "THIRD_PARTY_NOTICES.md")
    notices = BUNDLE / "licenses"
    shutil.copytree(ROOT / "packaging" / "licenses", notices, dirs_exist_ok=True)
    package_versions = {}
    for name in RUNTIME_PACKAGES:
        dist = metadata.distribution(name)
        package_versions[name] = dist.version
        copied = 0
        for file in dist.files or []:
            parts = [p.lower() for p in file.parts]
            dist_license = "licenses" in parts and any(
                part.endswith(".dist-info") for part in parts
            )
            if dist_license or file.name.lower().startswith(
                ("license", "copying", "notice", "authors")
            ):
                if ".." in file.parts or file.is_absolute():
                    raise RuntimeError(f"Unsafe distribution path: {file}")
                source = Path(dist.locate_file(file))
                if source.is_file() and source.stat().st_size:
                    copy_notice(source, notices / name / str(file))
                    copied += 1
        if not copied:
            raise RuntimeError(f"No license files in installed distribution: {name}")
    # Preserve extra notices supplied by this exact Python runtime, when available.
    base = Path(sys.base_prefix)
    for source in base.rglob("*"):
        if (
            source.is_file()
            and source.name.lower().startswith(("license", "copying"))
            and "site-packages" not in source.parts
            and source.stat().st_size
        ):
            copy_notice(source, notices / "python-runtime" / source.relative_to(base))
    tk_license = BUNDLE / "_internal" / "_tk_data" / "license.terms"
    copy_notice(tk_license, notices / "Tk.txt")
    fonts = BUNDLE / "_internal" / "customtkinter" / "assets" / "fonts"
    for font in fonts.rglob("*"):
        if font.suffix.lower() in (".ttf", ".otf"):
            (notices / f"{font.stem}-notices.txt").write_text(
                font_notices(font), "utf-8"
            )
    info = {
        "version": version,
        "source_commit": os.environ.get("BUILD_SOURCE_SHA", "local-unrecorded"),
        "python": platform.python_version(),
        "architecture": platform.machine(),
        "pyinstaller": metadata.version("pyinstaller"),
        "packages": package_versions,
        "uv_lock_sha256": sha256(ROOT / "uv.lock"),
        "signed": False,
    }
    (BUNDLE / "BUILD-INFO.json").write_text(json.dumps(info, indent=2) + "\n", "utf-8")
    manifest = BUNDLE / "SHA256SUMS.txt"
    lines = [
        f"{sha256(file)}  {file.relative_to(BUNDLE).as_posix()}"
        for file in sorted(BUNDLE.rglob("*"))
        if file.is_file() and file != manifest
    ]
    manifest.write_text("\n".join(lines) + "\n", "utf-8")
    archive = ROOT / "dist" / f"Probably4-v{version}-win64.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as output:
        for file in sorted(BUNDLE.rglob("*")):
            if file.is_file():
                output.write(file, file.relative_to(BUNDLE.parent))
    archive.with_suffix(".zip.sha256").write_text(
        f"{sha256(archive)}  {archive.name}\n", "utf-8"
    )
    print(json.dumps(info, indent=2))
    print(f"Packaged {archive.name}: {sha256(archive)}")


if __name__ == "__main__":
    main()
