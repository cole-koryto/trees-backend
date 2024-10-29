from sqlmodel import Field, SQLModel

class TreeInfo(SQLModel, table=True):
    tree_id: int | None = Field(default=None, index=True, primary_key=True)
    tag_number: int | None = Field(default=None, index=True)
    species_code: str | None
    latin_name: str | None
    common_name: str | None
    sun: str | None
    long: float
    lat: float

class TreeHistory(SQLModel, table=True):
    hist_id: int | None = Field(default=None, index=True, primary_key=True)
    tree_id: int = Field(index=True, foreign_key="treeinfo.tree_id")
    hazard_rating: str | None
    DBH: float | None
    notes: str | None
    year: int

class Users(SQLModel, table=True):
    username: str | None = Field(default=None, index=True, primary_key=True)
    email: str | None = None
    full_name: str
    hashed_password: str
    data_permissions: bool
    user_permissions: bool