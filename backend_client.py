from schemas.input_schemas import TreeInputPayload
from schemas.table_schemas import TreeInfo
from config import *
from typing import Annotated
from fastapi import Depends, FastAPI, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


# Creates new database session
def get_session():
    engine = create_engine(f"postgresql://{LOCAL_DB_USER}:{LOCAL_DB_PASS}@localhost:{LOCAL_DB_PORT}/{LOCAL_DB_NAME}")
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# configure FastAPI
app = FastAPI()


@app.get("/treeinfo")
def get_tree_info(session: SessionDep,) -> list[TreeInfo]:
    info = session.exec(select(TreeInfo))
    return info