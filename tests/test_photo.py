import subprocess
from datetime import datetime
from pathlib import Path

import boto3
import pytest
from PIL import Image

import photo_backup.consts as consts
from photo_backup.photo import Photo, Photos
from photo_backup.upload import S3Uploader


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


class TestPhotosInit:
    def test_init_uploader(self):
        expected = S3Uploader(consts.S3_BUCKET)
        photos = Photos(expected)
        actual = photos.uploader
        assert actual == expected

    def test_init_photos(self):
        photos = Photos(S3Uploader(consts.S3_BUCKET))
        actual = photos.photos
        expected = []
        assert actual == expected


class TestPhotosAppend:
    def test_photos_attribute(self):
        photos = Photos(S3Uploader(consts.S3_BUCKET))

        photo1 = Photo("data/images/IMG_9235.jpeg")
        photos.append(photo1)

        photo2 = Photo("data/images/SOVK6553.jpeg")
        photos.append(photo2)

        expected = [photo1, photo2]
        actual = photos.photos

        assert actual == expected

    def test_return_object(self):
        photos = Photos(S3Uploader(consts.S3_BUCKET))

        photo1 = Photo("data/images/IMG_9235.jpeg")
        actual = photos.append(photo1)
        expected = photos
        assert actual == expected


class TestPhotosUpload:
    def test_upload(self, folder_test, mocker):
        photos = Photos(S3Uploader(consts.S3_BUCKET))

        photo1 = Photo("data/images/IMG_9235.jpeg")
        expected_filename1 = f"{folder_test}/2020/08/20200813140708.jpeg"
        mocker.patch.object(
            photo1, "create_dst_path", side_effect=lambda: expected_filename1
        )
        photos.append(photo1)

        photo2 = Photo("data/images/SOVK6553.jpeg")
        expected_filename2 = f"{folder_test}/2020/10/20201012131028.jpeg"
        mocker.patch.object(
            photo2, "create_dst_path", side_effect=lambda: expected_filename2
        )
        photos.append(photo2)

        photos.upload()

        s3 = boto3.client("s3")
        response = s3.list_objects_v2(
            Bucket=consts.S3_BUCKET, Prefix=f"{folder_test}/2020"
        )
        uploaded_filename = [
            content["Key"] for content in response["Contents"]
        ]
        uploaded_filename.sort()

        expected = [
            expected_filename1,
            expected_filename2,
        ]

        assert uploaded_filename == expected

        response = subprocess.run(
            [
                "aws",
                "s3",
                "rm",
                "--recursive",
                f"s3://{consts.S3_BUCKET}/test/",
            ]
        )
        response.check_returncode()
