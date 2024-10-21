from sqlmodel import Field, SQLModel

class TreeInfo(SQLModel, table=True):
    Tree_ID: int | None = Field(default=None, index=True, primary_key=True)
    Tag_Number: int | None = Field(default=None, index=True)
    Species_Co: str | None
    Latin_Name: str | None
    Species_1: str | None
    Buil_Vinta: str | None
    Azimuth: float | None
    Dist_to_Bu: float | None
    Sun: str | None
    X: float | None
    Y: float | None

class TreeHistory(SQLModel, table=True):
    Hist_ID: int | None = Field(default=None, index=True, primary_key=True)
    Tree_ID: int = Field(index=True, foreign_key="treeinfo.Tree_ID")
    Tag_Number: int | None = Field(default=None, index=True)
    Hazard_Rat: str | None
    DBH: float | None
    Notes: str | None
    Year: int

class Users(SQLModel, table=True):
    User_ID: int | None = Field(default=None, index=True, primary_key=True)
    username: str
    email: str | None = None
    Full_Name: str
    hashed_password: str