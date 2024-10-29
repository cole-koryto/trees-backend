from pydantic import BaseModel

class NewUserInput(BaseModel):
    username: str
    email: str | None = None
    full_name: str
    password: str
    data_permissions: bool
    user_permissions: bool

class ModifyUserInput(BaseModel):
    username: str | None = None
    email: str | None = None
    full_name: str | None = None
    password: str | None = None
    data_permissions: bool| None = None
    user_permissions: bool| None = None