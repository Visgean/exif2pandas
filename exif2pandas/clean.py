from datetime import datetime
import os

from exifread import Ratio

from gps_utils import get_exif_location

IGNORE_STARTSWITH = (
    'MakerNote Tag',
    'Thumbnail',
    'Image Tag',
    'Image PrintIM',
    'MakerNote Internal',
    'EXIF MakerNote',
    'JPEGThumbnail',
)


def parse_exif_date(dt) -> datetime:
    return datetime.strptime(str(dt.values), '%Y:%m:%d %H:%M:%S')


def parse_date(exif_info):
    if 'Image DateTimeOriginal' in exif_info:
        return parse_exif_date(exif_info['Image DateTimeOriginal'])
    if 'Image DateTime' in exif_info:
        return parse_exif_date(exif_info['Image DateTime'])


def clean_exif_data(filename_exif_tuple, ignore_keys=IGNORE_STARTSWITH) -> dict:
    """
    Cleans exif data for each picture
    """
    path, data = filename_exif_tuple
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
                if isinstance(cleaned_val, Ratio):
                    cleaned_data[f'{key}_float'] = (
                        cleaned_val.num / cleaned_val.den
                        if cleaned_val.den != 0 else 0.0
                    )
            else:
                cleaned_val = tag.printable
            cleaned_data[key] = cleaned_val

    return cleaned_data
