import zipfile
from pathlib import Path

from constants import CAICO_CSV_NAME

def create_zip(csv_file):
    """
    CSVファイルをZIP化する
    """

    csv_file = Path(csv_file)

    zip_file = csv_file.with_suffix(".zip")

    with zipfile.ZipFile(
        zip_file,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:
        zipf.write(
            csv_file,
            # CaicoはZIP内の固定名 list.csv を使って
            # 保存データかどうかを判定する。
            arcname=CAICO_CSV_NAME
        )

    return zip_file
