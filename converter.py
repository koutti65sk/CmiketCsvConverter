from pathlib import Path

from csv_builder import create_row
from excel_reader import read_excel, get_hyperlinks
from zip_manager import create_zip
from csv_writer import save_csv

def excel_to_csv(file_path, mode="1", max_rows=None, log_callback=None):

    def log(message):
        if log_callback:
            log_callback(message)
        else:
            print(message)

    log(f"変換開始 : {file_path}")

    # 保存先は元ファイルと同じフォルダ
    output_dir = Path(file_path).parent
    output_dir = Path(file_path).parent
    excel_name = Path(file_path).stem


    log(
    "Excel読み込み中...",
)

    # 各シートをCSVに変換
    sheets = read_excel(
        file_path,
        max_rows
    )

    log(
        f"{len(sheets)}個のシートを検出",
    )


    for sheet_data in sheets:

        sheet = sheet_data["name"]
        df = sheet_data["df"]
        ws = sheet_data["ws"]

        log(
            f"{sheet} を変換中...",
        )

        links = get_hyperlinks(ws, "URL")

        if len(links) < len(df):
            links.extend([""] * (len(df)-len(links)))

        links = links[:len(df)]

        if "購入内容" not in df.columns:
            log(f"{sheet} に購入内容列がありません")
            continue

        if mode == "1":
            df = df[df["購入内容"].notna()]
            df = df[df["購入内容"].astype(str).str.strip() != ""]

        rows = []

        for i, row in df.iterrows():
            rows.append(
                create_row(row, links[i])
            )

        output_file = save_csv(
            rows,
            output_dir,
            excel_name,
            sheet
        )


        log(
            "ZIP作成中...",
        )
        # CSVをZIPに圧縮
        zip_file = create_zip(output_file)

        # CSVを削除
        output_file.unlink()

        log(f"✔ {zip_file.name} を作成しました")


    log("すべてのシートの変換が完了しました。")