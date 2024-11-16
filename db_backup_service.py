"""
This file connects to the trees database running locally and
backs up the tree data specifically to csvs.

If you then want to use these backed up files, move them to active_csvs and change their names.
"""

import datetime
import pandas as pd
import psycopg2
from sqlmodel import create_engine
import time

from config import *


if __name__ == "__main__":
    while True:
        # Connects to database, reads current tables, and saves them to csv
        try:
            engine = create_engine(f"postgresql://{LOCAL_DB_USER}:{LOCAL_DB_PASS}@localhost:{LOCAL_DB_PORT}/{LOCAL_DB_NAME}", echo=True)
            pd.read_sql_table("treehistory", engine).to_csv(f"./backup_csvs/{datetime.datetime.now().date()}_treehistory.csv", index=False)
            pd.read_sql_table("treeinfo", engine).to_csv(f"./backup_csvs/{datetime.datetime.now().date()}_treeinfo.csv", index=False)
            pd.read_sql_table("users", engine).to_csv(f"./backup_csvs/{datetime.datetime.now().date()}_users.csv", index=False)
            print(f"Database successfully backed up on {datetime.datetime.now().date()}")
        except Exception as e:
            print(e)
            print(f"Database FAILED to back up on {datetime.datetime.now().date()}")

        time.sleep(60*60*24*BACKUP_INTERVAL_DAYS)