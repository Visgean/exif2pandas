#!/usr/bin/env python3


from datetime import datetime
from pathlib import Path

import exifread
import os

picture_globs = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']

def get_extension(filename):
    filename, file_extension = os.path.splitext(filename)
    return file_extension.lower()


def get_pictures(directory: Path):
    pics = []
    for glob in picture_globs:
        pics.extend(directory.rglob(glob))
    return pics


def get_exif(filename):
    try:
        with open(filename, 'rb') as f:
            return exifread.process_file(f)
    except:
        return


def parse_date(exif_info):
    if not exif_info:
        return
    date = exif_info.get('Image DateTime')
    if not date:
        return
    try:
        return datetime.strptime(str(date.values), '%Y:%m:%d %H:%M:%S')
    except ValueError:
        return
