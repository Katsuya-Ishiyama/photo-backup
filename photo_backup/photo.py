from pathlib import Path

import boto3
from PIL import Image

import photo_backup.consts as consts
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

    def upload(self):
        s3 = boto3.client("s3")
        src_path = str(self.path)
        dst_path = self.create_dst_path()
        s3.upload_file(
            src_path,
            consts.S3_BUCKET,
            dst_path,
        )
