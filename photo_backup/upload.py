from abc import ABC, abstractmethod
from pathlib import Path

import boto3

S3Uri = str


class Uploader(ABC):
    @abstractmethod
    def upload(self, src: Path, dst: S3Uri):
        pass


class S3Uploader(Uploader):
    def __init__(self, bucket: str):
        self.bucket = bucket

    def upload(self, src: Path, dst: S3Uri):
        s3 = boto3.client("s3")
        s3.upload_file(
            str(src),
            self.bucket,
            dst,
        )
