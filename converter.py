import zipfile
from pathlib import Path
import pandas as pd
from openpyxl import load_workbook

from csv_builder import create_row
from constants import CSV_COLUMNS

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

    def hyperlink_list(ws, header_name):
        header = {c.value:i+1 for i,c in enumerate(ws[1])}
        if header_name not in header:
            return []
        col = header[header_name]
        links=[]
        for r in range(2, ws.max_row+1):
            cell = ws.cell(r,col)
            if cell.hyperlink:
                links.append(cell.hyperlink.target)
            else:
                links.append("")
        return links

    # Excelファイルを読み込む
    excel=pd.ExcelFile(file_path)
    wb=load_workbook(file_path,data_only=True)

    # 保存先は元ファイルと同じフォルダ
    output_dir = Path(file_path).parent

    created_csv_files = []

    # 各シートをCSVに変換
    for sheet in excel.sheet_names:
        df = pd.read_excel(
            file_path,sheet_name=sheet,nrows=max_rows
        )

        df.columns = df.columns.astype(str).str.strip()
        if "購入内容" not in df.columns:
            print(f"{sheet} に購入内容列がありません")
            continue

        if mode == "1":
            df = df[df["購入内容"].notna()]
            df = df[df["購入内容"].astype(str).str.strip() != ""]

        ws=wb[sheet]
        links=hyperlink_list(ws,"URL")
        if len(links)<len(df):
            links.extend([""]*(len(df)-len(links)))
        links=links[:len(df)]

        rows = []

        for i, row in df.iterrows():
            rows.append(
                create_row(
                    row,
                    links[i]
                )
            )

        csv_df = pd.DataFrame(rows, columns=CSV_COLUMNS)

        excel_name = Path(file_path).stem

        # 1行目を作成
        first_row = {col: "" for col in CSV_COLUMNS}
        first_row["買い物リスト名"] = f"{excel_name}_{sheet}"

        # 先頭へ追加
        csv_df = pd.concat(
            [pd.DataFrame([first_row]), csv_df],
            ignore_index=True
        )

        output_file = output_dir / f"{excel_name}_{sheet}.csv"
        csv_df = csv_df.reindex(columns=CSV_COLUMNS)

        csv_df.to_csv(
            output_file,
            index=False,
            encoding="utf-8-sig",
            columns=CSV_COLUMNS
        )

        # ZIPファイル名（CSVと同じ名前）
        zip_file = output_dir / f"{excel_name}_{sheet}.zip"

        # CSVをZIPに圧縮
        with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(output_file, arcname=output_file.name)

        # CSVを削除
        output_file.unlink()


        print(f"✔ {zip_file.name} を作成しました")


    print("\nすべてのシートの変換が完了しました。")