# oldonesay

**A Lovecraftian terminal oracle for macOS and Linux.**

`oldonesay` turns your terminal into a tiny cult altar: speech bubble up top, Old One below, rendered in ANSI truecolor from bundled PNG sprite art. It is a Python CLI for Unicode-capable terminals that want something stranger than `cowsay`.

## Preview

- PNG-backed terminal sprite rendering
- Seven gods with names, epithets, and quote pools
- Random, fixed-god, custom-text, and piped-input modes
- One-command loop mode with `./loopones.sh`

## Gallery

Current terminal renders generated from the live CLI output:

![oldonesay gallery](docs/screenshots/gallery.png)

## Install

Install from a git clone of the repository, then install the package in editable mode.

```bash
git clone https://github.com/your-user/oldonesay.git
cd oldonesay
python3 -m pip install -e .
```

Run it:

```bash
oldonesay
```

Requirements:

- Python `3.8+`
- A terminal with ANSI color and Unicode block character support
- `Pillow` is installed automatically through the package dependency

## Quickstart

Random god, canonical quote:

```bash
oldonesay
```

Specific god:

```bash
oldonesay -g hastur
```

Specific god with custom text:

```bash
oldonesay -g cthulhu "The sea remembers."
```

List available gods:

```bash
oldonesay -l
```

Pipe text into the CLI:

```bash
echo "The gate is opening." | oldonesay -g yog-sothoth
```

Loop the oracle in a cleared terminal:

```bash
./loopones.sh
```

## Usage

Command summary:

```text
oldonesay
oldonesay "your message"
oldonesay -g cthulhu
oldonesay -g hastur "He stirs."
oldonesay -l
echo "text" | oldonesay
```

Flags:

- `-g, --god`: choose a specific god or `random`
- `-l, --list`: list available gods and exit
- `-q, --quote`: force a canonical quote even if a message is supplied

Behavior:

- With no message, `oldonesay` uses a canonical quote for the selected god.
- With piped stdin, the piped text is used unless `--quote` is set.
- Art is rendered at runtime from packaged PNG files in `oldones_say/gods/`.

## Examples

Ask Dagon to speak:

```bash
oldonesay -g dagon "From the deep."
```

Force a canonical Azathoth quote:

```bash
oldonesay -g azathoth --quote
```

Run an infinite shell loop manually:

```bash
while true; do
  oldonesay
  sleep 5
  clear
done
```

## Project Layout

- `oldones_say.cli`: CLI entry point and argument parsing
- `oldones_say.gods`: god registry, PNG loading, and terminal rendering
- `oldones_say.bubble`: speech-bubble formatting
- `oldones_say.quotes`: canonical quote pools
- `oldones_say/gods/*.png`: bundled sprite assets used at runtime

## Development

Install editable dependencies:

```bash
python3 -m pip install -e .
```

Sanity checks:

```bash
python3 -m py_compile oldones_say/cli.py oldones_say/gods/__init__.py oldones_say/gods/*.py
python3 -m oldones_say.cli -l
python3 -m oldones_say.cli -g hastur "He stirs."
```

## License

This project is licensed under the MIT License. See `LICENSE`.
