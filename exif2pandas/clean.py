import os

from datetime import datetime
from typing import Optional
from fractions import Fraction
from slugify import slugify

from .gps_utils import get_exif_location

IGNORE_STARTSWITH = (
    'MakerNote Tag',
    'Thumbnail',
    'Image Tag',
    'Image PrintIM',
    'MakerNote Internal',
    'EXIF MakerNote',
    'JPEGThumbnail',
)


def parse_exif_date(dt) -> Optional[datetime]:
    try:
        return datetime.strptime(str(dt.values), '%Y:%m:%d %H:%M:%S')
    except ValueError:
        return None


def parse_date(exif_info) -> Optional[datetime]:
    if 'Image DateTimeOriginal' in exif_info:
        return parse_exif_date(exif_info['Image DateTimeOriginal'])
    if 'Image DateTime' in exif_info:
        return parse_exif_date(exif_info['Image DateTime'])


def clean_exif_data(path, data, ignore_keys=IGNORE_STARTSWITH) -> dict:
    """
    Cleans exif data for each picture
    """
    lat, lon = get_exif_location(data)
    size = os.path.getsize(path) / 1024 ** 2

    cleaned_data = {
        'filename': str(path),
        'cleaned_latitude': lat,
        'cleaned_longitude': lon,
        'size_megabytes': size,
        'cleaned_date': parse_date(data)
    }

    for key, tag in data.items():
        if not any([key.startswith(prefix) for prefix in ignore_keys]):
            if tag and tag.values and len(tag.values) == 1:
                cleaned_val = tag.values[0]
                if isinstance(cleaned_val, Fraction):
                    cleaned_data[slugify(f'{key}-float')] = (
                        cleaned_val.numerator / cleaned_val.denominator
                        if cleaned_val.denominator != 0 else 0.0
                    )
                    cleaned_val = tag.printable
            else:
                cleaned_val = tag.printable

            cleaned_data[slugify(key)] = cleaned_val

    return cleaned_data
