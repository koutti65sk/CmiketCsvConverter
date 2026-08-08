import json
from pathlib import Path


SETTINGS_FILE = (
    Path(__file__).resolve().parent
    / "settings.json"
)

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


    # 読み込み方法のチェック
    if settings["default_mode"] not in ("1", "2"):

        settings["default_mode"] = DEFAULT_SETTINGS["default_mode"]


    # 読み込み行数のチェック
    if (
        not isinstance(settings["default_max_rows"], int)
        or settings["default_max_rows"] <= 0
    ):

        settings["default_max_rows"] = (
            DEFAULT_SETTINGS["default_max_rows"]
        )


    # ZIP作成のチェック
    if not isinstance(settings["create_zip"], bool):

        settings["create_zip"] = (
            DEFAULT_SETTINGS["create_zip"]
        )


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