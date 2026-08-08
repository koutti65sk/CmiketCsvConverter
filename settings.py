import json
from pathlib import Path


SETTINGS_FILE = Path("settings.json")

DEFAULT_SETTINGS = {
    "default_mode": "1",
    "default_max_rows": 150,
    "create_zip": True
}


def load_settings():

    if not SETTINGS_FILE.exists():
        return DEFAULT_SETTINGS.copy()

    try:

        with open(
            SETTINGS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            settings = json.load(f)

    except (json.JSONDecodeError, OSError):

        return DEFAULT_SETTINGS.copy()

    for key, value in DEFAULT_SETTINGS.items():

        if key not in settings:
            settings[key] = value

    return settings


def save_settings(settings):

    with open(
        SETTINGS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            settings,
            f,
            indent=4,
            ensure_ascii=False
        )