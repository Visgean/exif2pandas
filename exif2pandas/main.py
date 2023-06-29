#!/usr/bin/env python3
import argparse

from pathlib import Path
from . import extract

parser = argparse.ArgumentParser(description="Generate sql database with exif data.")
parser.add_argument("picture_folders", nargs="+", help="Folders with the images")

parser.add_argument(
    "-s",
    "--sqlite",
    help="Output the data frame to SQLite file (this will override existing file!)",
)

parser.add_argument(
    "-f",
    "--feather",
    help="Output the data frame to feather file (this will override existing file!)",
)

parser.add_argument(
    "-e",
    "--excel",
    help="Output the data frame to excel (this will override existing file!)",
)

parser.add_argument(
    "-a",
    "--avro",
    help="Output the data frame to avro file",
)


parser.add_argument(
    "-p",
    "--processes",
    type=int,
    help="number of processes to use for collecting exif data, defaults to 5",
    default=5,
)


def main():
    args = parser.parse_args()
    picture_dirs = [Path(f).resolve() for f in args.picture_folders]

    if args.feather:
        extract.extract_feather(
            pictures_root=picture_dirs,
            feather_path=Path(args.feather).resolve(),
            processes=args.processes,
        )

    elif args.sqlite:
        extract.extract_sqlite(
            pictures_root=picture_dirs,
            sqlite_path=Path(args.sqlite).resolve(),
            processes=args.processes,
        )

    elif args.excel:
        extract.extract_sqlite(
            pictures_root=picture_dirs,
            sqlite_path=Path(args.excel).resolve(),
            processes=args.processes,
        )


if __name__ == "__main__":
    main()
