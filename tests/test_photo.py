from datetime import datetime
from pathlib import Path

import pytest
from PIL import Image

from photo_backup.photo import Photo


class TestPhotoInit:
    @pytest.fixture(scope="function")
    def photo(self):
        return (
            "data/images/IMG_9235.jpeg",
            Photo("data/images/IMG_9235.jpeg"),
        )

    def test_init_path(self, photo):
        _path, _photo = photo
        expected = Path(_path)
        assert _photo.path == expected

    def test_init_photo(self, photo):
        _path, _photo = photo
        expected = Image.open(_path)
        assert _photo.photo == expected

    def test_init_exif(self, photo):
        _path, _photo = photo
        expected = datetime(2020, 8, 13, 14, 7, 8)
        assert _photo.exif.datetime_original == expected


class TestPhotoExtractFileExtension:
    def test_extract_file_extension(self):
        actual = Photo("data/images/IMG_9235.jpeg").extract_file_extension()
        expected = ".jpeg"
        assert actual == expected


class TestPhotoCreateDstPath:
    def test_create_dst_path(self):
        actual = Photo("data/images/IMG_9235.jpeg").create_dst_path()
        expected = "2020/08/20200813140708.jpeg"
        assert actual == expected
