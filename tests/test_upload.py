import boto3
import photo_backup.consts as consts
from photo_backup.photo import Photo
from photo_backup.upload import S3Uploader


class TestS3UploaderUpload:
    def test_upload(self):
        photo = Photo("data/images/IMG_9235.jpeg")
        uploader = S3Uploader(consts.S3_BUCKET)
        uploader.upload(photo)

        s3 = boto3.client("s3")
        response = s3.list_objects_v2(
            Bucket=consts.S3_BUCKET, Prefix="2020/08"
        )
        uploaded_filename = response["Contents"][0]["Key"]
        expected = "2020/08/20200813140708.jpeg"

        assert uploaded_filename == expected

        s3.delete_object(Bucket=consts.S3_BUCKET, Key=expected)
