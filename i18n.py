import json
import locale
from pathlib import Path

DEFAULT_LANGUAGE = "en"

_TRANSLATIONS = {}


def detect_language():
    lang, _ = locale.getlocale()

    if not lang:
        return DEFAULT_LANGUAGE

    return lang


def load_language(language=None):

    if language is None:
        language = detect_language()

    locale_dir = Path(__file__).parent / "locales"

    candidates = [
        f"{language}.json",
        f"{language.split('_')[0]}.json",
        "en.json"
    ]

    for filename in candidates:
        path = locale_dir / filename

        if path.exists():
            with open(path, encoding="utf8") as fp:
                _TRANSLATIONS.clear()
                _TRANSLATIONS.update(json.load(fp))
            return

    raise RuntimeError("No language file found.")


def t(key, **kwargs):

    text = _TRANSLATIONS.get(key, key)

    return text.format(**kwargs)