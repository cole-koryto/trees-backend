import pandas as pd
from sqlalchemy import create_engine
from config import *
import psycopg2


def main():

    tree_gps = pd.read_csv("tree_gps.csv")
    tree_history = pd.read_csv("tree_history.csv")
    tree_info = pd.read_csv("tree_info.csv")


    # Tries to connect to postgres database on default port if possible
    try:
        engine = create_engine(f"postgresql://{LOCAL_DB_USER}:{LOCAL_DB_PASS}@localhost:5432/{LOCAL_DB_NAME}")
        tree_gps.to_sql('treegps', engine, index=False)
        tree_history.to_sql('treehistory', engine, index=False)
        tree_info.to_sql('treeinfo', engine, index=False)

    except Exception as e:
        engine = create_engine(f"postgresql://{LOCAL_DB_USER}:{LOCAL_DB_PASS}@localhost:5433/{LOCAL_DB_NAME}")
        tree_gps.to_sql('treegps', engine, index=False)
        tree_history.to_sql('treehistory', engine, index=False)
        tree_info.to_sql('treeinfo', engine, index=False)


if __name__ == "__main__":
    main()