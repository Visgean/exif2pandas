#!/usr/bin/env python3

from pathlib import Path
import argparse
import utils
from clean import clean_all

parser = argparse.ArgumentParser(description="Generate sql database with exif data.")
parser.add_argument('picture_folders', nargs='+', help='Folders with the images')

parser.add_argument(
    '-o', '--out',
    help='location for the sqlite db file',
    default='photos.sqlite'
)

def main():
    args = parser.parse_args()

    pics_filenames = []
    for folder in args.picture_folders:
        abs_path = Path(folder).resolve()
        pics_filenames.extend(utils.get_pictures(abs_path))

    print("Located", len(pics_filenames), "pictures.")

    cleaned_data = clean_all(utils.multiprocess_extract_exif(pics_filenames))
    print(cleaned_data[0].keys())






if __name__ == '__main__':
    main()
