import pandas as pd
import os
from sqlalchemy import create_engine


def main():
    csv_files = [file for file in os.listdir() if ".csv" in file]

    overall_df = pd.DataFrame()
    for file in csv_files:
        overall_df = pd.concat([overall_df, pd.read_csv(file)])

    engine = create_engine('postgresql://postgres:localpost17@localhost:5432/postgres')
    overall_df.to_sql('trees', engine, index=False)


if __name__ == "__main__":
    main()