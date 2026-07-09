# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project follows Semantic Versioning (SemVer).

---

## [1.2.0] - 2026-07-09

### Added

- New `concat` command to concatenate multiple CHR files.
- Automatic creation of the output CHR file during concatenation.
- `--pad` support during concatenation.
- `--dedupe` support during concatenation.
- Tile remapping export (`--tile-map`) during concatenation.
- Completely redesigned command-line help (`--help`).
- Usage examples included directly in the help output.
- Detailed descriptions for all commands and arguments.

### Improved

- CHR bank generation workflow, allowing intermediate CHR files without padding and generating the final padded bank only in the last step.
- Improved command-line interface organization.
- Updated documentation.

## [1.1.0] - 2026-07-06

### Added

- User interface internationalization (English and Brazilian Portuguese)
- Automatic operating system language detection
- `--lang` option for manual language selection
- Automatic global palette generation for images with up to four colors
- `--pad` option to automatically pad CHR files (4K, 8K, 16K or custom size)
- `--dedupe` option to remove duplicate tiles
- `--tile-map` option to export tile index remapping
- Debug map generation highlighting all problematic tiles
- Enlarged debug image of the first problematic tile
- Modular project structure prepared for future expansion

### Improved

- Consistent color indexing across all tiles
- Internal project organization
- Error messages and validation
- Documentation and README

---

## [1.0.0] - 2026-07-05

### Added

- Initial public release
- PNG to CHR conversion
- Image dimension validation
- Per-tile color analysis
- Automatic palette suggestion
- Global palette support
- Color replacement (`--replace`)
- Debug image generation
- Nintendo Entertainment System compatible CHR output