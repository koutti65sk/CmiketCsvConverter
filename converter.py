from pathlib import Path
import pandas as pd

from csv_builder import create_row
from excel_reader import read_excel, get_hyperlinks
from zip_manager import create_zip as create_zip_file
from csv_writer import save_csv, get_csv_path
from circle_sorter import (
    clear_repeated_circle_values,
    sort_circle_groups
)


def excel_to_csv(
    file_path,
    mode="1",
    max_rows=None,
    output_dir=None,
    output_name=None,
    log_callback=None,
    progress_callback=None,
    create_zip=True,
    overwrite_callback=None,
    cancel_event=None
):

    def log(message):
        if log_callback:
            log_callback(message)
        else:
            print(message)

    log(
        "変換を開始しました"
    )

    log(
        f"ファイル: {Path(file_path).name}"
    )

    if Path(file_path).suffix.lower() != ".xlsx":
        raise ValueError(
            "対応しているExcelファイルは.xlsx形式のみです。"
        )

    # 保存先は元ファイルと同じフォルダ
    if output_dir is None:
        output_dir = Path(file_path).parent
    else:
        output_dir = Path(output_dir)

    excel_name = Path(file_path).stem

    if output_name:
        excel_name = output_name

    log("Excel読み込み中...")

    # Excelを読み込む
    sheets = read_excel(
        file_path,
        max_rows
    )

    total_sheets = len(sheets)

    log(
        f"{len(sheets)}個のシートを検出"
    )

    converted_count = 0
    skipped_count = 0
    converted_sheets = []
    skipped_sheets = []

    # 各シートをCSVに変換
    for index, sheet_data in enumerate(sheets, start=1):

        sheet = sheet_data["name"]
        df = sheet_data["df"]
        ws = sheet_data["ws"]

        if cancel_event and cancel_event.is_set():
            log(
                f"{sheet} の処理前にキャンセルされました"
            )
            break

        log("")
        log(
            f"[{index}/{total_sheets}] {sheet} を変換中..."
        )

        links = get_hyperlinks(
            ws,
            "URL"
        )

        if len(links) < len(df):
            links.extend(
                [""] * (len(df) - len(links))
            )

        links = links[:len(df)]

        if "購入内容" not in df.columns:
            log(
                f"↷ {sheet} をスキップしました（購入内容列なし）"
            )

            skipped_count += 1
            skipped_sheets.append(sheet)

            if progress_callback:
                progress_callback(
                    index,
                    total_sheets
                )
            continue

        if mode == "1":

            valid_indices = []

            for row_index, row in df.iterrows():

                value = row["購入内容"]

                if pd.isna(value) or str(value).strip() == "":
                    break

                valid_indices.append(row_index)

            df = df.loc[valid_indices]

        # サークル内の商品順を維持したまま、
        # 地区、区分、場所の順で自動ソートする。
        df = sort_circle_groups(df)

        # 同一サークルの商品が複数行ある場合、先頭行だけに
        # サークル情報を残し、後続行を商品追加行へ変換する。
        df = clear_repeated_circle_values(df)

        rows = []

        for i, row in df.iterrows():

            if cancel_event and cancel_event.is_set():

                log(
                    f"✖ {sheet} の変換をキャンセルしました"
                )

                break

            rows.append(
                create_row(
                    row,
                    links[i]
                )
            )


        if cancel_event and cancel_event.is_set():

            break

        output_file = get_csv_path(
            output_dir,
            excel_name,
            sheet
        )

        zip_file = output_file.with_suffix(".zip")

        if output_file.exists() or zip_file.exists():
            log(
                "既存の出力ファイルを検出しました"
            )

            if overwrite_callback:
                should_overwrite = overwrite_callback(
                    output_file,
                    zip_file
                )

                if should_overwrite is None:

                    log("")

                    log(
                        f"✖ {sheet} の処理をキャンセルしました"
                    )

                    if cancel_event:
                        cancel_event.set()

                    break

                if not should_overwrite:

                    log(
                        f"↷ {sheet} をスキップしました"
                    )

                    skipped_count += 1
                    skipped_sheets.append(sheet)

                    if progress_callback:
                        progress_callback(
                            index,
                            total_sheets
                        )

                    continue

        output_file = save_csv(
            rows,
            output_dir,
            excel_name,
            sheet
        )

        converted_count += 1
        converted_sheets.append(sheet)

        if create_zip:
            log("ZIP作成中...")

            zip_file = create_zip_file(
                output_file
            )

            output_file.unlink()

            log(
                f"✔ {zip_file.name} を作成しました"
            )

        else:
            log(
                f"✔ {output_file.name} を作成しました"
            )

        if progress_callback:
            progress_callback(
                index,
                total_sheets
            )


    if cancel_event and cancel_event.is_set():
        log("")
        log(
            "変換結果"
        )
        log(
            "--------------------"
        )
        log(
            f"✔ 変換：{converted_count}個"
        )
        for sheet in converted_sheets:
            log(
                f"  ・{sheet}"
            )
        log(
            f"↷ スキップ：{skipped_count}個"
        )
        for sheet in skipped_sheets:
            log(
                f"  ・{sheet}"
            )
        log(
            "✖ キャンセル"
        )
        log(
            "--------------------"
        )

    elif converted_count == 0:
        log("")
        log("変換対象のシートはありませんでした。")

    else:
        log("")
        log(
            "変換結果"
        )
        log(
            "--------------------"
        )
        log(
            f"✔ 変換：{converted_count}個"
        )
        for sheet in converted_sheets:
            log(
                f"  ・{sheet}"
            )
        log(
            f"↷ スキップ：{skipped_count}個"
        )
        for sheet in skipped_sheets:
            log(
                f"  ・{sheet}"
            )
        log(
            "--------------------"
        )

    return {
        "converted": converted_count,
        "skipped": skipped_count,
        "converted_sheets": converted_sheets,
        "skipped_sheets": skipped_sheets,
        "cancelled": (
            cancel_event is not None
            and cancel_event.is_set()
        )
    }
