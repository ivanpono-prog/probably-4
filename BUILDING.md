# Windows release build

The candidate version is read from `pyproject.toml`; do not edit EXE version
strings separately. Builds use Python 3.13.18, PyInstaller 6.22.3 and the committed
`uv.lock`. The recipe is repeatable, not a guarantee of byte-identical outputs:
the Windows runner image and native toolchain can change.

On Windows x64, install uv 0.13.6, then from the repository root:

```powershell
uv python install 3.13.18
uv sync --locked --group build --no-install-project
uv run --no-sync python -m pytest -v
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
$env:BUILD_SOURCE_SHA = git rev-parse HEAD
uv run --no-sync pyinstaller --noconfirm --clean Probably4.spec
uv run --no-sync python scripts/package_windows.py
uv run --no-sync python scripts/verify_windows.py
```

Run each command only after the preceding command succeeds. The build writes
under `build/` and `dist/`, and PyInstaller replaces its existing output there.
Use a clean checkout for release builds. Commit dependency updates and the
regenerated lock file together; normal builds must use `--locked`.

The Windows package workflow runs on pull requests and main, and can be
started manually. It uploads a candidate ZIP, SHA256, build information and
smoke-test results to Actions artifacts. It has read-only repository permissions
and does not create tags or publish releases.

The smoke test extracts the ZIP to a fresh directory with spaces in its name,
checks every file against its hash manifest, clears Python environment variables,
removes Python from PATH, and starts the bundled EXE with a 60-second timeout.
It checks GUI construction, logo loading, arithmetic, zero division, digit input,
backspace and conversion. It does not emulate a clean consumer Windows install
or replace manual interaction and visual checks.

## Before publishing v1.0.1

- Merge the reviewed changes only after both workflows pass.
- Use the candidate from the successful main-branch run for the exact commit
  that will be tagged `v1.0.1`. Do not reuse a PR merge-commit artifact.
- Check BUILD-INFO.json, the ZIP hash, licenses and EXE version.
- Test the ZIP in a disposable Windows 10/11 x64 VM without Python installed.
  Record the actual OS edition/build and results in the release notes.
- Check normal launch, logo, mouse and keyboard entry, double confirmations,
  shuffled digits, both converter directions/modes and graceful errors for
  invalid/large input. Record failures rather than describing untested systems
  as supported.
- Attach the ZIP and its `.sha256` file to a new release. Keep v1.0.0 intact.
- State that the build is unsigned. Do not advise disabling Windows protection.

If code signing is added later, sign before creating the manifests and ZIP,
verify the signature, and update BUILD-INFO's signing status accordingly.
