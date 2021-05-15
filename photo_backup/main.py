from pathlib import Path

import click

import photo_backup.consts as consts
from photo_backup.photo import Photo, Photos
from photo_backup.upload import S3Uploader


@click.group(help="Backup Your Photos")
def main():
    pass


@main.command(help="Upload photos which are put on SRC_DIR")
@click.argument("src_dir", type=Path)
def upload(src_dir):
    photos = Photos(S3Uploader(consts.S3_BUCKET))
    for filepath in src_dir.iterdir():
        if filepath.name.startswith("."):
            # Skipping hidden files or directories
            continue
        photos.append(Photo(filepath))
    photos.upload()


if __name__ == "__main__":
    main()
