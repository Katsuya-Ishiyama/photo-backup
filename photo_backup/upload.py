from abc import ABC, abstractmethod

import boto3

from photo_backup.photo import Photo


class Uploader(ABC):
    @abstractmethod
    def upload(self, photo: Photo):
        pass


class S3Uploader(Uploader):
    def __init__(self, bucket: str):
        self.bucket = bucket

    def upload(self, photo: Photo):
        s3 = boto3.client("s3")
        src_path = str(photo.path)
        dst_path = photo.create_dst_path()
        s3.upload_file(
            src_path,
            self.bucket,
            dst_path,
        )
