from sqlmodel import Field, SQLModel

class TreeInfo(SQLModel, table=True):
    Tag_Number: int | None = Field(default=None, index=True, primary_key=True)
    Species_Co: str | None
    Latin_Name: str | None
    Species_1: str | None
    Buil_Vinta: str | None
    Azimuth: float | None
    Dist_to_Bu: float | None
    Sun: str | None
