import pandas as pd
# from sqlalchemy import create_engine
from config import *
import psycopg2
from schemas.table_schemas import TreeInfo, TreeHistory
from sqlmodel import Field, SQLModel, create_engine


def main():

    user_input = input("WARNING: Executing this program will DELETE ALL tables in the trees database\nIf you are positive you want to continue enter \"tree\".\n")
    while user_input != "tree":
        user_input = input("ERROR: You did not enter \"tree\" try again.\n")

    tree_history = pd.read_csv("tree_history.csv")
    tree_info = pd.read_csv("tree_info.csv")

    # Tries to connect to postgres database on default port if possible
    try:
        engine = create_engine(f"postgresql://{LOCAL_DB_USER}:{LOCAL_DB_PASS}@localhost:5432/{LOCAL_DB_NAME}", echo=True)
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
        tree_info.to_sql('treeinfo', engine, if_exists="append", index=False)
        tree_history.to_sql('treehistory', engine, if_exists="append", index=False)

    except Exception as e:
        engine = create_engine(f"postgresql://{LOCAL_DB_USER}:{LOCAL_DB_PASS}@localhost:5433/{LOCAL_DB_NAME}", echo=True)
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
        tree_info.to_sql('treeinfo', engine, if_exists="append", index=False)
        tree_history.to_sql('treehistory', engine, if_exists="append", index=False)


if __name__ == "__main__":
    main()