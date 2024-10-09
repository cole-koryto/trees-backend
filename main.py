import pandas as pd
from sqlalchemy import create_engine
import psycopg2


def main():

    overall_df = pd.read_csv("campustrees.csv")

    # Tries to connect to postgres database on default port if possible
    try:
        engine = create_engine('postgresql://postgres:localpost17@localhost:5432/postgres')
        overall_df.to_sql('trees', engine, index=False)

    except Exception as e:
        engine = create_engine('postgresql://postgres:localpost17@localhost:5433/postgres')
        overall_df.to_sql('trees', engine, index=False)


if __name__ == "__main__":
    main()