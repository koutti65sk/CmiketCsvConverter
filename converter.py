from pathlib import Path

from csv_builder import create_row
from excel_reader import read_excel, get_hyperlinks
print("読み込んでいるexcel_reader:", excel_reader.__file__)
from zip_manager import create_zip
from csv_writer import save_csv

def excel_to_csv(file_path, mode="1", max_rows=None):
    """
    ExcelをCSVへ変換しZIPを作成する

    Parameters
    ----------
    file_path : str
        Excelファイルのパス

    mode : str
        "1" = 購入内容が空白まで
        "2" = 指定行まで

    max_rows : int | None
        mode="2" の時だけ使用
    """

    print(f"変換開始 : {file_path}")

    # 保存先は元ファイルと同じフォルダ
    output_dir = Path(file_path).parent
    output_dir = Path(file_path).parent
    excel_name = Path(file_path).stem


    # 各シートをCSVに変換
    sheets = read_excel(
        file_path,
        max_rows
    )


    for sheet_data in sheets:

        sheet = sheet_data["name"]
        df = sheet_data["df"]
        ws = sheet_data["ws"]

        links = get_hyperlinks(ws, "URL")

        if len(links) < len(df):
            links.extend([""] * (len(df)-len(links)))

        links = links[:len(df)]

        if "購入内容" not in df.columns:
            print(f"{sheet} に購入内容列がありません")
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

        # CSVをZIPに圧縮
        zip_file = create_zip(output_file)

        # CSVを削除
        output_file.unlink()

        print(f"✔ {zip_file.name} を作成しました")


    print("\nすべてのシートの変換が完了しました。")