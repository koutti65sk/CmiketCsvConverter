import re
import unicodedata

import pandas as pd


SORT_COLUMNS = ("場所", "区分", "地区")


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
        if _has_value(row["サークル名"]) or current_group is None:
            current_group = {
                "indices": [],
                "sort_row": row,
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
