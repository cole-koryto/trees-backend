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

    user_input = input("Executing this program will reset the admin profile to the default in the \"config.py\"\nWould you like to continue? (y/n)\n")
    while user_input != "y":
        user_input = input("ERROR: You did not enter \"y\" try again.\n")

    # Tries to connect to postgres database on default port if possible
    default_user = Users(username=ADMIN_USERNAME, email=ADMIN_EMAIL, full_name=ADMIN_NAME, hashed_password=pbkdf2_sha256.hash(ADMIN_PASSWORD), data_permissions=True, user_permissions=True)
    engine = create_engine(f"postgresql://{LOCAL_DB_USER}:{LOCAL_DB_PASS}@localhost:{LOCAL_DB_PORT}/{LOCAL_DB_NAME}", echo=True)

    # Connect to the database and reset the admin user to the default
    with Session(engine) as session:
        admin_user_check = session.exec(select(Users).where(Users.username == ADMIN_USERNAME)).one_or_none()
        if admin_user_check:
            session.delete(admin_user_check)
        session.add(default_user)
        session.commit()
        print("Admin user reset to default")

if __name__ == "__main__":
    main()