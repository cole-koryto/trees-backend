from schemas.input_schemas import TreeInputPayload
import uvicorn
from typing import Annotated, Union
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


# class Tree(SQLModel, table=True):
#     Tag_Number: int | None = Field(default=None, index=True, primary_key=True)
#     Hazard_Rat: str | None
#     DBH__cm_: int
#     Notes: str | None
#     Max_PDOP: int
#     Corr_Type: str
#     GPS_Date: str
#     GPS_Time: str
#     Feat_Name: str
#     Datafile: str
#     Unfilt_Pos:  int
#     Filt_Pos: int
#     Data_Dicti: str
#     Std_Dev: float | None
#     Point_ID: int
#     layer: str
#     path: str
#     TagNumber: int | None
#     Species: str | None
#     LatinName: str | None
#     Species_1: str | None
#     DBH_2019: float | None
#     Azimuth: int | None
#     Dist_to_Bu: int | None
#     Sun: str | None
#     Hazard: int | None
#
#
# postgres_url = "postgresql://postgres:localpost17@localhost:5432/postgres"
# connect_args = {"check_same_thread": False}
# engine = create_engine(postgres_url, connect_args=connect_args)


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)
#
#
# def get_session():
#     with Session(engine) as session:
#         yield session
#
#
# SessionDep = Annotated[Session, Depends(get_session)]



# configure FastAPI
app = FastAPI()


@app.post("/")
def main():
    return "HELLO"

if __name__ == "__main__":
    uvicorn.run("backend_client:app", host="127.0.0.1", port=8000, reload=True)