import logging
import pathlib
from typing import List

import pandas
import pandas as pd

from pathlib import Path
from . import utils


def extract_feather(
    pictures_root: List[pathlib.Path],
    feather_path: Path,
    processes: int,
) -> pd.DataFrame:
    """
    Extract dataframe with exif information.
    If an existing file is detected it is used to speed up the scan.
    This function overrides the existing df but also returns the df.

    """
    existing_df = None
    feather_file = Path(feather_path).resolve()
    if feather_file.exists():
        try:
            existing_df = pandas.read_feather(feather_file)
            logging.info("Using existing feather file")
        except:
            logging.error("Could not read existing feather file, possibly corrupted. Deleting file now. ")
            feather_file.unlink()

    df = utils.get_panda_df(
        [Path(f).resolve() for f in pictures_root],
        processes=processes,
        existing_df=existing_df,
    )

    # See https://github.com/pandas-dev/pandas/issues/21228
    # in short we need to interpret all "object" columns as text
    converted_pd = df.astype(
        {column: str for column, dtype in df.dtypes.items() if str(dtype) == "object"}
    )
    converted_pd.to_feather(feather_file)
    return df


def extract_sqlite(
    pictures_root: List[pathlib.Path],
    sqlite_path: Path,
    processes: int,
) -> pd.DataFrame:
    try:
        from sqlalchemy import create_engine
    except ImportError:
        logging.error("sqlalchemy must be installed for sql export")

    df = utils.get_panda_df(
        pictures_root,
        processes=processes,
    )

    sql_file = Path(sqlite_path).resolve()
    if sql_file.exists():
        sql_file.unlink()
    engine = create_engine(f"sqlite:///{sql_file}", echo=False)
    df.to_sql("photos", con=engine)
    return df


def extract_excel(
    pictures_root: List[pathlib.Path],
    excel_path: Path,
    processes: int,
) -> pd.DataFrame:
    df = utils.get_panda_df(
        pictures_root,
        processes=processes,
    )

    excel_file = Path(excel_path).resolve()
    if excel_file.exists():
        excel_file.unlink()
    df.to_excel(excel_file)
    return df
