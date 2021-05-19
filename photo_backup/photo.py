from pathlib import Path
from typing import List

from PIL import Image

from .exif import extract_exif
from .upload import Uploader


class Photo(object):
    def __init__(self, path: str):
        self.path = Path(path)
        self.exif = extract_exif(Image.open(path))

    def extract_file_extension(self) -> str:
        return self.path.suffix

    def create_dst_path(self) -> str:
        datetime_original = self.exif.datetime_original
        year = datetime_original.strftime("%Y")
        month = datetime_original.strftime("%m")
        filename = datetime_original.strftime("%Y%m%d%H%M%S")
        extension = self.extract_file_extension()
        return f"{year}/{month}/{filename}{extension}"


class Photos(object):
    def __init__(self, uploader: Uploader):
        self.uploader = uploader
        self.photos: List[Photo] = []

    def append(self, photo: Photo):
        self.photos.append(photo)
        return self

    def upload(self):
        for photo in self.photos:
            src = photo.path
            dst = photo.create_dst_path()
            self.uploader.upload(src, dst)
