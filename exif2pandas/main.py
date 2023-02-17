#!/usr/bin/env python3
import argparse

import pandas
import pandas as pd

from pathlib import Path
from . import utils

parser = argparse.ArgumentParser(description="Generate sql database with exif data.")
parser.add_argument('picture_folders', nargs='+', help='Folders with the images')

parser.add_argument(
    '-s', '--sqlite',
    help='Output the data frame to SQLite file (this will override existing file!)',
)

parser.add_argument(
    '-f', '--feather',
    help='Output the data frame to feather file (this will override existing file!)',
)

parser.add_argument(
    '-e', '--excel',
    help='Output the data frame to excel (this will override existing file!)',
)

parser.add_argument(
    '-a', '--avro',
    help='Output the data frame to avro file',
)


parser.add_argument(
    '-p', '--processes',
    type=int,
    help='number of processes to use for collecting exif data, defaults to 5',
    default=5
)


def main():
    args = parser.parse_args()

    if args.feather:
        existing_df = None

        feather_file = Path(args.feather).resolve()
        if feather_file.exists():
            existing_df = pandas.read_feather(feather_file)
            print('Using existing feather file')

        df = utils.get_panda_df(
            [Path(f).resolve() for f in args.picture_folders],
            processes=args.processes,
            existing_df=existing_df
        )

        # See https://github.com/pandas-dev/pandas/issues/21228
        # in short we need to interpret all "object" columns as text
        converted_pd = df.astype({
            column: str
            for column, dtype in df.dtypes.iteritems()
            if str(dtype) == 'object'
        })
        converted_pd.to_feather(feather_file)
        return


    df = utils.get_panda_df(
        [Path(f).resolve() for f in args.picture_folders],
        processes=args.processes
    )

    if args.sqlite:
        from sqlalchemy import create_engine

        sql_file = Path(args.sqlite).resolve()
        if sql_file.exists():
            sql_file.unlink()
        engine = create_engine(f'sqlite:///{sql_file}', echo=False)
        df.to_sql('photos', con=engine)


    if args.excel:
        excel_file = Path(args.excel).resolve()
        if excel_file.exists():
            excel_file.unlink()
        df.to_excel(excel_file)


if __name__ == '__main__':
    main()
