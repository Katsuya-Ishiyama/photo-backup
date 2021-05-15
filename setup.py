from setuptools import find_packages, setup

setup(
    name="photo_backup",
    version="0.1.0",
    packages=find_packages(),
    url="",
    license="",
    author="Katsuya-Ishiyama",
    author_email="ishiyama.katsuya@gmail.com",
    description="",
    entry_points={
        "console_scripts": ["photo-backup = photo_backup.main:main"]
    },
)
