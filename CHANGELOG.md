# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project follows Semantic Versioning (SemVer).

---

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