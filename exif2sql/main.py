#!/usr/bin/env python3

from pathlib import Path
import argparse
import utils



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

    print(len(pics_filenames))


if __name__ == '__main__':
    main()
