from datetime import datetime
from typing import List, Tuple

import pytest
from PIL import Image

from photo_backup.exif import check_datetime_format, Exif, extract_exif


class TestCheckDatetimeFormat:

    test_data: List[Tuple[str, bool]] = [
        ("2020:11:12 21:48:39", True),
        ("20200:11:12 21:48:39", False),
        ("2020:110:12 21:48:39", False),
        ("2020:11:120 21:48:39", False),
        ("2020:11:12 210:48:39", False),
        ("2020:11:12 21:480:39", False),
        ("2020:11:12 21:48:390", False),
        ("2020:11:12-21:48:39", False),
        ("2020/11/12 21:48:39", False),
    ]

    @pytest.mark.parametrize("datetime_str, expected", test_data)
    def test_check_datetime_format(self, datetime_str, expected):
        result = check_datetime_format(datetime_str)
        assert result is expected


class TestExifInit:
    @pytest.mark.parametrize(
        "exif",
        [
            {36867: "2019:09:11 10:55:46"},
            {36867: "2019:09:11 10:55:46", 40963: "1108"},
        ],
    )
    def test_datetime_original(self, exif):
        actual = Exif(exif)
        expected = datetime.strptime(exif[36867], "%Y:%m:%d %H:%M:%S")
        assert actual.datetime_original == expected

    @pytest.mark.parametrize("exif", [{36867: "2019-09-11 10:55:46"}])
    def test_datetime_original_raise_ValueError(self, exif):
        with pytest.raises(ValueError):
            Exif(exif)

    @pytest.mark.parametrize("exif", [{}, {40963: "1108"}])
    def test_datetime_original_raise_KeyError(self, exif):
        with pytest.raises(KeyError):
            Exif(exif)


class TestExifMakeFilename:
    @pytest.mark.parametrize(
        "exif, expected",
        [
            ({36867: "2019:09:11 10:55:46"}, "20190911105546"),
            ({36867: "2019:09:11 10:55:46", 40963: "1108"}, "20190911105546"),
        ],
    )
    def test_make_filename(self, exif, expected):
        _exif = Exif(exif)
        actual = _exif.make_filename()
        assert actual == expected


class TestExtractExif:
    def test_extract_exif(self):
        im = Image.open("data/images/IMG_9235.jpeg")
        exif = extract_exif(im)
        expected = datetime(2020, 8, 13, 14, 7, 8)
        assert exif.datetime_original == expected
