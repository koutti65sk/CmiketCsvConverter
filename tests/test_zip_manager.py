import tempfile
import unittest
import zipfile
from pathlib import Path

from constants import CAICO_CSV_NAME
from zip_manager import create_zip


class CreateZipTests(unittest.TestCase):
    def test_csv_is_stored_as_caico_list_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "C108_1日目.csv"
            csv_bytes = b"\xef\xbb\xbfheader\nvalue\n"
            csv_path.write_bytes(csv_bytes)

            zip_path = create_zip(csv_path)

            with zipfile.ZipFile(zip_path) as archive:
                self.assertEqual(archive.namelist(), [CAICO_CSV_NAME])
                self.assertEqual(archive.read(CAICO_CSV_NAME), csv_bytes)


if __name__ == "__main__":
    unittest.main()
