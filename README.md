# png2chr

A Python tool for analyzing and converting PNG sprite sheets into the CHR format used by the Nintendo Entertainment System (NES).

The project was created to simplify NES homebrew development by providing an easy workflow to validate sprites, inspect palettes and generate CHR files compatible with the console hardware.

---

# Features

- PNG to CHR conversion
- Sprite sheet support
- Native NES tile generation
- Image size validation (multiples of 8)
- Transparency support
- Per-tile color analysis
- Full image analysis before conversion
- Automatic palette suggestion
- Automatic global palette generation whenever possible
- Optional user-defined global palette
- Color replacement during conversion (`--replace`)
- Debug images for problematic tiles
- Debug map highlighting every problematic tile
- Automatic CHR padding (4K, 8K, 16K or custom size)
- Internationalization (English and Brazilian Portuguese)

---

# Requirements

- Python 3.9+
- Pillow

Install:

```bash
pip install pillow
```

---

# Project structure

```
png2chr/
├── locales/
│   ├── en.json
│   └── pt_BR.json
├── analyzer.py
├── chr_writer.py
├── debug_tools.py
├── i18n.py
├── image_tools.py
├── palette_tools.py
└── png2chr.py
```

---

# Analyzing an image

Before converting, you can analyze the sprite sheet:

```bash
python3 png2chr.py analyze player.png
```

The analysis reports:

- image dimensions;
- tile count;
- detected colors;
- suggested palette;
- problematic tiles.

If issues are found, the tool generates a debug map showing exactly which tiles need attention.

You can also generate an enlarged view of the first problematic tile:

```bash
python3 png2chr.py analyze player.png --debug
```

---

# Converting to CHR

Simple conversion:

```bash
python3 png2chr.py convert player.png player.chr
```

If the image contains four or fewer colors, a global palette is automatically generated to ensure consistent color indices across all tiles.

---

# Using a fixed palette

You can explicitly provide the palette used during conversion.

```bash
python3 png2chr.py convert player.png player.chr \
    --palette "0,0,0,0;0,0,0,255;248,56,0,255;252,224,168,255"
```

---

# Replacing colors

Useful when adapting artwork to NES palette limitations.

```bash
python3 png2chr.py convert player.png player.chr \
    --replace "63,63,116,255=0,0,0,255"
```

Multiple `--replace` options are supported.

---

# Automatic CHR padding

To simplify integration with `ca65`/`ld65`, the generated CHR can be automatically padded.

Example:

```bash
python3 png2chr.py convert player.png player.chr --pad 8k
```

Supported values include:

```
4k
8k
16k
4096
8192
16384
```

---

# Languages

The tool automatically detects the operating system language.

You can also force a language manually:

```bash
python3 png2chr.py --lang en analyze player.png

python3 png2chr.py --lang pt_BR convert player.png player.chr
```

If a translation is unavailable, English is used as the default language.

---

# CHR format

Each tile is 8×8 pixels.

Each tile occupies 16 bytes:

```
8 bytes -> bitplane 0
8 bytes -> bitplane 1
```

Fully compatible with the Nintendo Entertainment System CHR format.

---

# Roadmap

Planned features:

- [ ] Automatic duplicate tile removal
- [ ] CHR preview
- [ ] Tile index export
- [ ] Automatic `.asm` generation
- [ ] Sprite sheet cropping
- [ ] Multiple sprite palettes
- [ ] Graphical interface
- [ ] Metadata export for games
- [ ] Nametable preview generation

---

# Motivation

Most CHR tools available today are old, require Wine or have an inconvenient workflow.

This project aims to provide a modern, simple and cross-platform solution for developers creating NES games in 6502 Assembly.

---

# License

MIT
