from multiprocessing.pool import Pool

ignore_startswith = ['MakerNote Tag', 'Thumbnail']


def clean_exif_data(filename_exif_tuple) -> dict:
    """
    Cleans exif data for each picture
    """
    path, data = filename_exif_tuple

    cleaned_data = {
        'filename': str(path)
    }

    for key, value in data.items():
        if any([key.startswith(prefix) for prefix in ignore_startswith]):
            continue
        cleaned_data[key] = value
    return cleaned_data


def clean_all(exif_with_filenames):
    with Pool(5) as pool:
        return pool.map(clean_exif_data, exif_with_filenames)


