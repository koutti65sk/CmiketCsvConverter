import re
import unicodedata

import pandas as pd


SORT_COLUMNS = ("場所", "区分", "地区")
CIRCLE_COLUMNS = (
    "サークル名",
    "作家",
    "地区",
    "区分",
    "場所",
    "優先度",
    "担当者"
)


def _has_value(value):
    return pd.notna(value) and str(value).strip() != ""


def _natural_key(value):
    """空欄を最後にし、数字部分を数値として比較できるキーを返す。"""

    if not _has_value(value):
        return (1, ())

    text = unicodedata.normalize(
        "NFKC",
        str(value).strip()
    ).casefold()

    parts = tuple(
        (0, int(part)) if part.isdigit() else (1, part)
        for part in re.split(r"(\d+)", text)
        if part != ""
    )

    return (0, parts)


def _normalized_text(value):
    if not _has_value(value):
        return ""

    return unicodedata.normalize(
        "NFKC",
        str(value).strip()
    ).casefold()


def _circle_identity(row):
    """同名サークルの別配置を誤結合しないため、配置情報も識別に使う。"""

    if not _has_value(row.get("サークル名")):
        return None

    return tuple(
        _normalized_text(row.get(column))
        for column in ("サークル名", "地区", "区分", "場所")
    )


def sort_circle_groups(df):
    """
    商品行をサークル単位でまとめたまま、
    場所、区分、地区の順で並べ替える。
    """

    if df.empty or "サークル名" not in df.columns:
        return df.copy()

    groups = []
    current_group = None

    for row_index, row in df.iterrows():
        identity = _circle_identity(row)

        if (
            current_group is None
            or (
                identity is not None
                and identity != current_group["identity"]
            )
        ):
            current_group = {
                "indices": [],
                "sort_row": row,
                "identity": identity,
                "original_order": len(groups)
            }
            groups.append(current_group)

        current_group["indices"].append(row_index)

    groups.sort(
        key=lambda group: (
            *(
                _natural_key(group["sort_row"].get(column))
                for column in SORT_COLUMNS
            ),
            group["original_order"]
        )
    )

    return pd.concat(
        [df.loc[group["indices"]] for group in groups]
    )


def clear_repeated_circle_values(df):
    """
    連続する同一サークルでは先頭行だけサークル情報を残し、
    後続行をCaicoの商品追加行として扱える形にする。
    """

    if df.empty or "サークル名" not in df.columns:
        return df.copy()

    result = df.copy()
    current_identity = None

    for row_index, row in result.iterrows():
        identity = _circle_identity(row)

        if identity is None:
            continue

        if identity == current_identity:
            columns = [
                column
                for column in CIRCLE_COLUMNS
                if column in result.columns
            ]
            result.loc[row_index, columns] = None
        else:
            current_identity = identity

    return result
