"""
This file connects to the trees database running locally and
resets the tables in the database using the data in tree_history.csv and tree_info.csv

It should only be run when first initializing the server when there is no existing data, or
to recover from a failure of the postgres database.
"""

import os.path
import pandas as pd
from passlib.hash import pbkdf2_sha256
import psycopg2
from schemas.table_schemas import TreeInfo, TreeHistory, Users
from sqlmodel import SQLModel, create_engine, Session, select

from config import *


def main():

    user_input = input("WARNING: Executing this program will DELETE ALL tables in the trees database\nIf you are positive you want to continue enter \"tree\".\n")
    while user_input != "tree":
        user_input = input("ERROR: You did not enter \"tree\" try again.\n")

    # Ensures that csvs to pull from actually exist
    if not (os.path.isfile("./active_csvs/tree_history.csv") and os.path.isfile("./active_csvs/tree_info.csv")):
        raise Exception("tree_history.csv and/or tree_info.csv do not exist in the active_csvs folder.\nProgram cannot run without those EXACT files existing in that EXACT location./")

    # Opens and reads db csv files
    tree_history = pd.read_csv("./active_csvs/tree_history.csv")
    tree_info = pd.read_csv("./active_csvs/tree_info.csv")

    # Tries to connect to postgres database on default port if possible
    default_user = Users(username=ADMIN_USERNAME, email=ADMIN_EMAIL, full_name=ADMIN_NAME, hashed_password=pbkdf2_sha256.hash(ADMIN_PASSWORD), data_permissions=True, user_permissions=True)
    engine = create_engine(f"postgresql://{LOCAL_DB_USER}:{LOCAL_DB_PASS}@localhost:{LOCAL_DB_PORT}/{LOCAL_DB_NAME}", echo=True)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    tree_info.to_sql('treeinfo', engine, if_exists="append", index=False)
    tree_history.to_sql('treehistory', engine, if_exists="append", index=False)

    # Restores from user csv, if there, and resets admin to config.py info
    if os.path.isfile("./active_csvs/users.csv"):
        print("users.csv found in /active_csvs restoring users table from csv")
        users = pd.read_csv("./active_csvs/users.csv")
        users.to_sql('users', engine, if_exists="append", index=False)
    else:
        print("users.csv NOT found in /active_csvs NOT restoring users table from csv")
    with Session(engine) as session:
        admin_user_check = session.exec(select(Users).where(Users.username == ADMIN_USERNAME)).one_or_none()
        if admin_user_check:
            session.delete(admin_user_check)
        session.add(default_user)
        session.commit()


if __name__ == "__main__":
    main()