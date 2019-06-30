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

    df = utils.get_panda_dataframe([Path(f).resolve() for f in args.picture_folders])
    print(df)






if __name__ == '__main__':
    main()
