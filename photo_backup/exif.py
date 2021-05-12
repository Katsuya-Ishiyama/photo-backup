import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict

from PIL import Image


def check_datetime_format(value: str):
    allowed_datetime_format = r"^\d{4}:\d{2}:\d{2}\s\d{2}:\d{2}:\d{2}$"
    is_expected = True if re.match(allowed_datetime_format, value) else False
    return is_expected


class ExifTag(Enum):

    DATETIME_ORIGINAL: int = 36867


@dataclass
class Exif(object):

    datetime_original: datetime

    def __init__(self, exif: Dict[int, str]):
        self.set_datetime_original(exif[ExifTag.DATETIME_ORIGINAL.value])

    def set_datetime_original(self, value: str) -> None:
        if not check_datetime_format(value):
            raise ValueError("unavailable format.")

        self.datetime_original = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")

    def make_filename(self) -> str:
        return self.datetime_original.strftime("%Y%m%d%H%M%S")


def extract_exif(image: Image) -> Exif:
    exif = image._getexif()
    return Exif(exif)
