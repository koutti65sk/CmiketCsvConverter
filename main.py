python.exe -m pip install --upgrade pipimport pandas as pd
from pathlib import Path
from openpyxl import load_workbook
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import zipfile

def convert_excel_to_csv(file_path):
    try:
        print("読み込み方法を選択してください")
        print("1：購入内容が空白になるまで")
        print("2：指定した行まで")

        mode = input("選択 (1/2)：").strip()

        max_rows = None

        if mode == "2":
            while True:
                try:
                    max_rows = int(input("最大行数を入力してください："))
                    break
                except ValueError:
                    print("数字を入力してください。")

        columns = [
            "ホール","スペース","サークル名","サークルメモ","サークルタグ","色","マップ番号","ピンX","ピンY","ピン型","ピン値","サークル画像","アイテム名","アイテム画像","単価","数量","アイテムメモ","アイテムタグ","チェック","買い物リスト名","買い物メモ"
        ]

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

                if pd.notna(row["サークル名"]) and str(row["サークル名"]).strip() != "":

                    # サークル行
                    rows.append({
                        "ホール": row["地区"],
                        "スペース": str(row["区分"] if pd.notna(row["区分"]) else "") +
                                str(row["場所"] if pd.notna(row["場所"]) else ""),
                        "サークル名": row["サークル名"],
                        "サークルメモ": "",
                        "サークルタグ": "お品書き@" + links[i] if links[i] else "",
                        "色": 0,
                        "マップ番号": 0,
                        "ピンX": -1.0,
                        "ピンY": -1.0,
                        "ピン型": 0,
                        "ピン値": 0,
                        "サークル画像": "",
                        "アイテム名": row["購入内容"],
                        "アイテム画像": "",
                        "単価": f"{float(row['金額']):.1f}" if pd.notna(row["金額"]) else "0.0",
                        "数量": row["数量"],
                        "アイテムメモ": row["メモ"],
                        "アイテムタグ": "",
                        "チェック": 0,
                        "買い物リスト名": "",
                        "買い物メモ": ""
                    })

                else:
                    # アイテムだけ追加
                    rows.append({
                        "ホール": "",
                        "スペース": "",
                        "サークル名": "",
                        "サークルメモ": "",
                        "サークルタグ": "",
                        "色": "",
                        "マップ番号": "",
                        "ピンX": "",
                        "ピンY": "",
                        "ピン型": "",
                        "ピン値": "",
                        "サークル画像": "",
                        "アイテム名": row["購入内容"],
                        "アイテム画像": "",
                        "単価": f"{float(row['金額']):.1f}" if pd.notna(row["金額"]) else "0.0",
                        "数量": row["数量"],
                        "アイテムメモ": row["メモ"],
                        "アイテムタグ": "",
                        "チェック": 0,
                        "買い物リスト名": "",
                        "買い物メモ": ""
                    })

            csv_df = pd.DataFrame(rows, columns=columns)

            excel_name = Path(file_path).stem

            # 1行目を作成
            first_row = {col: "" for col in columns}
            first_row["買い物リスト名"] = f"{excel_name}_{sheet}"

            # 先頭へ追加
            csv_df = pd.concat(
                [pd.DataFrame([first_row]), csv_df],
                ignore_index=True
            )

            output_file = output_dir / f"list.csv"
            csv_df = csv_df.reindex(columns=columns)

            csv_df.to_csv(
                output_file,
                index=False,
                encoding="utf-8-sig",
                columns=columns
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

    except PermissionError:
        print("エラー: Excelファイルが開かれています。閉じてから再実行してください。")

    except Exception as e:
        print(f"エラー: {e}")

# ------------------------------

# メインウィンドウを表示しない
root = Tk()
root.withdraw()
root.attributes("-topmost", True)  # ダイアログを最前面に表示

# ファイル選択
file_path = askopenfilename(
    title="変換するExcelファイルを選択してください",
    filetypes=[
        ("Excelファイル", "*.xlsx"),
        ("すべてのファイル", "*.*")
    ]
)

# ファイルが選択されなかった場合
if not file_path:
    print("ファイルが選択されませんでした。")
    input("\nEnterキーで終了...")
    exit()

# ファイルが存在するか確認
if not Path(file_path).exists():
    print("指定されたファイルが存在しません。")
    input("\nEnterキーで終了...")
    exit()

convert_excel_to_csv(file_path)

input("\nEnterキーで終了...")