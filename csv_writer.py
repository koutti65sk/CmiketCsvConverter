from pathlib import Path
import pandas as pd

from constants import CSV_COLUMNS


def save_csv(rows, output_dir, excel_name, sheet):
    """
    CSVファイルを作成して保存する
    """

    csv_df = pd.DataFrame(
        rows,
        columns=CSV_COLUMNS
    )

    # 1行目（買い物リスト名）を作成
    first_row = {
        col: ""
        for col in CSV_COLUMNS
    }

    first_row["買い物リスト名"] = (
        f"{excel_name}_{sheet}"
    )

    # 先頭へ追加
    csv_df = pd.concat(
        [
            pd.DataFrame([first_row]),
            csv_df
        ],
        ignore_index=True
    )

    output_file = (
        Path(output_dir)
        / f"{excel_name}_{sheet}.csv"
    )

    csv_df = csv_df.reindex(
        columns=CSV_COLUMNS
    )

    csv_df.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    return output_file