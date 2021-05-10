from pathlib import Path

from PIL import Image

from photo_backup.exif import extract_exif


class Photo(object):
    def __init__(self, path: str):
        self.path = Path(path)
        self.photo = Image.open(path)
        self.exif = extract_exif(self.photo)

    def extract_file_extension(self) -> str:
        return self.path.suffix

    def create_dst_path(self) -> str:
        datetime_original = self.exif.datetime_original
        year = datetime_original.strftime("%Y")
        month = datetime_original.strftime("%m")
        filename = datetime_original.strftime("%Y%m%d%H%M%S")
        extension = self.extract_file_extension()
        return f"{year}/{month}/{filename}{extension}"
