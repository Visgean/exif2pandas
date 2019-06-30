from multiprocessing.pool import Pool

from gps_utils import get_exif_location

IGNORE_STARTSWITH = (
    'MakerNote Tag',
    'Thumbnail',
    'Image Tag',
    'Image PrintIM',
    "MakerNote Internal"
    "EXIF MakerNote"
)


def clean_exif_data(filename_exif_tuple, ignore_keys=IGNORE_STARTSWITH) -> dict:
    """
    Cleans exif data for each picture
    """
    path, data = filename_exif_tuple
    lat, lon = get_exif_location(data)
    
    cleaned_data = {
        'filename': str(path),
        'cleaned_latitude': lat,
        'cleaned_longitude': lon,
    }

    for key, value in data.items():
        if any([key.startswith(prefix) for prefix in ignore_keys]):
            continue
        cleaned_data[key] = value
    return cleaned_data


def clean_all(exif_with_filenames):
    with Pool(5) as pool:
        return pool.map(clean_exif_data, exif_with_filenames)
