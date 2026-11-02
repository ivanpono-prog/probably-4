"""Verify and launch the newly built ZIP outside the source/build directory."""

import hashlib
import json
import os
import subprocess
import tempfile
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text("utf-8"))["project"]
    version = project["version"]
    archive = ROOT / "dist" / f"Probably4-v{version}-win64.zip"
    with tempfile.TemporaryDirectory(prefix="Probably 4 verification ") as temp:
        destination = Path(temp)
        with zipfile.ZipFile(archive) as bundle:
            for name in bundle.namelist():
                target = (destination / name).resolve()
                if not target.is_relative_to(destination.resolve()):
                    raise RuntimeError(f"Unsafe ZIP path: {name}")
            bundle.extractall(destination)
        app = destination / "Probably4"
        manifest = app / "SHA256SUMS.txt"
        listed = set()
        for line in manifest.read_text("utf-8").splitlines():
            expected, name = line.split("  ", 1)
            target = (app / name).resolve()
            if not target.is_relative_to(app.resolve()):
                raise RuntimeError(f"Unsafe manifest path: {name}")
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
            if actual != expected:
                raise RuntimeError(f"Hash mismatch: {name}")
            listed.add(name)
        actual_files = {
            p.relative_to(app).as_posix() for p in app.rglob("*") if p.is_file()
        }
        if listed != actual_files - {"SHA256SUMS.txt"}:
            raise RuntimeError("File manifest does not cover the ZIP")
        report = destination / "result.json"
        env = {key.upper(): value for key, value in os.environ.items()}
        for key in list(env):
            if key.upper().startswith(("PYTHON", "VIRTUAL_ENV", "UV_")):
                env.pop(key)
        env["PATH"] = str(Path(env["SYSTEMROOT"]) / "System32")
        process = subprocess.run(
            [str(app / "Probably4.exe"), "--smoke-test", str(report)],
            cwd=destination,
            env=env,
            check=False,
            timeout=60,
        )
        if not report.is_file():
            raise RuntimeError(f"EXE exited {process.returncode} without a test report")
        result = json.loads(report.read_text("utf-8"))
        if process.returncode != 0 or result.get("ok") is not True:
            raise RuntimeError(result)
        print(json.dumps(result, indent=2))
        (ROOT / "dist" / "smoke-test.json").write_text(
            json.dumps(result, indent=2) + "\n", "utf-8"
        )


if __name__ == "__main__":
    main()
