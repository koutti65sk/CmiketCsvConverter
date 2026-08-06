import zipfile
from pathlib import Path

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
            arcname=csv_file.name
        )

    return zip_file