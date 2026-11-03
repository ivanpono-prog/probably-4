# 🎩 Probably 4

**Correct answers. Questionable manners.**

A beautifully designed calculator that performs ordinary decimal arithmetic while treating its users with quiet, aristocratic contempt.

*Deliberately terrible UX, meticulously implemented.*

## Motivation

Probably 4 explores a simple question:

**What if software were technically excellent but fundamentally uninterested in helping its users?**

Probably 4 is a deliberately frustrating desktop calculator with impeccable manners and an inflated sense of intellectual superiority.

It performs ordinary calculations correctly. Unfortunately, it has its own opinions about how you should perform them.

The goal isn't broken mathematics or random crashes. It's a consistent, intentionally inconvenient experience delivered through a polished interface.

Every unnecessary confirmation is a feature. Every rearranged button is a design decision.

## Features

- **The Unstable Keypad** — Number buttons rearrange themselves after every digit you enter.
- **Aristocratic Superiority** — The calculator grows increasingly judgmental as you use it.
- **The Keyboard Inquisition** — Prefer typing? Expect an unnecessarily elaborate confirmation process.
- **The Illusion of Choice** — A temperature converter that respectfully disregards your preferences.
- **Occasional Gentleman** — Rare moments when the calculator briefly acknowledges your competence.
- **Decimal Arithmetic** — Ordinary calculations use Python's decimal arithmetic; repeating fractions and large numbers are subject to finite precision.

## Quick Start

### Windows

Download the Windows version from the [Releases](../../releases) page.

1. Download the latest Windows ZIP archive.
2. Extract the entire archive.
3. Open `Probably4.exe` inside the extracted `Probably4` folder.
4. Question your decisions.

No Python installation required. Keep the executable and its accompanying `_internal` folder together.

**Security note:** The Windows build is x64 and currently unsigned. Windows may show an unknown publisher or reputation warning. Download only from this repository's Releases; do not disable Windows protection to run it.

See each release's notes for the actual tested Windows versions. The v1.0.1 candidate still needs manual validation on clean Windows 10/11 systems.

Starting with v1.0.1, compare the ZIP's SHA256 with the attached `.sha256` file:

```powershell
Get-FileHash .\Probably4-v1.0.1-win64.zip -Algorithm SHA256
```

This verifies download integrity, not the publisher's identity. New packages also contain `LICENSE`, `licenses/`, `THIRD_PARTY_NOTICES.md` and `BUILD-INFO.json`.

### Run From Source

Install [uv](https://docs.astral.sh/uv/), then run:

```bash
git clone https://github.com/ivanpono-prog/probably-4.git
cd probably-4
uv sync
uv run python main.py
```

## Usage

Probably 4 provides two modes:

**Calculator**

Click the number buttons to enter an expression, choose an arithmetic operator, and press `=` to calculate. The currently selected operator is highlighted, and the complete expression appears on the display.

The number buttons rearrange themselves after every digit. You can also use your keyboard, although the calculator may have some objections.

**Converter**

Switch to the Converter tab, select Celsius or Fahrenheit, enter a temperature, and press **Convert**.

The calculator may respectfully disagree with your preferred input unit. Always check the displayed conversion direction before interpreting the result.

**Personality**

As you perform more operations, Probably 4 becomes increasingly judgmental. Expect occasional confirmations, theatrical processing delays, and rare moments of unexpected courtesy.

Calculations use Decimal's default 28 significant digits; temperature results are rounded to two decimal places. This playful app is not intended for high-precision or safety-critical calculations.

## Built With

- Python 3.13
- CustomTkinter
- Pillow
- PyInstaller
- pytest
- Ruff

## Contributing

Contributions, bug reports, and suggestions are welcome.

1. Fork the repository and create a branch for your changes.
2. Make your changes while preserving the application's deliberately inconvenient personality.
3. Run the automated tests and code quality checks:

```bash
uv run python -m pytest -v
uv run ruff check .
uv run ruff format --check .
```

4. Open a pull request describing your changes.

Please keep the distinction between *intentional bad UX* and *unintentional bugs*. The calculator should be frustrating by design, not because something is broken.

See [BUILDING.md](BUILDING.md) for the Windows build recipe and release checklist.

## License

Probably 4 is [MIT licensed](LICENSE). Bundled components have their own [third-party notices](THIRD_PARTY_NOTICES.md).

---

*Probably 4 — Because the answer is the least interesting part of the calculation.*
