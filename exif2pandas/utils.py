import pandas as pd
import exifread
import os

from pathlib import Path
from typing import List
from multiprocessing import Pool
from clean import clean_exif_data

picture_globs = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']

PROCESSES_DEFAULT = 5


def get_extension(filename):
    filename, file_extension = os.path.splitext(filename)
    return file_extension.lower()


def get_pictures(directory: Path):
    pics = []
    for glob in picture_globs:
        pics.extend(directory.rglob(glob))
    return pics


def get_exif(path):
    with open(path, 'rb') as f:
        return path, exifread.process_file(f)


def multiprocess_extract_exif(fnames: List[Path], processes=PROCESSES_DEFAULT):
    with Pool(processes) as pool:
        return pool.map(get_exif, fnames)


def clean_all(exif_with_filenames, processes=PROCESSES_DEFAULT):
    with Pool(processes) as pool:
        return pool.map(clean_exif_data, exif_with_filenames)


def get_panda_dataframe(folder_names):
    pics_filenames = []
    for folder in folder_names:
        abs_path = Path(folder).resolve()
        pics_filenames.extend(get_pictures(abs_path))

    cleaned_data = clean_all(multiprocess_extract_exif(pics_filenames))

    return pd.DataFrame(cleaned_data)
