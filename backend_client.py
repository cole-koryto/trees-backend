from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.hash import pbkdf2_sha256
from sqlalchemy import ScalarResult
from sqlmodel import Session, create_engine, select
from typing import Annotated

from config import *
from schemas.input_schemas import TreeInputPayload
from schemas.table_schemas import TreeInfo, TreeHistory, Users
from schemas.token_schemas import Token, TokenData


# authentication configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# configure FastAPI
app = FastAPI()

# Creates new database session
def get_session():
    engine = create_engine(f"postgresql://{LOCAL_DB_USER}:{LOCAL_DB_PASS}@localhost:{LOCAL_DB_PORT}/{LOCAL_DB_NAME}")
    with Session(engine) as session:
        yield session
SessionDep = Annotated[Session, Depends(get_session)]


# Endpoint that returns the treeinfo table
@app.get("/treeinfo")
async def get_tree_info(session: SessionDep,):
    info = session.exec(select(TreeInfo))
    return info

# Endpoint that returns the treehistory table
@app.get("/treehistory")
async def get_tree_history(session: SessionDep,):
    history = session.exec(select(TreeHistory))
    return history


# Gets a specified user based off of the given username
def get_user(username: str, session: SessionDep,):
    statement = select(Users).where(Users.username == username)
    user_info = session.exec(statement).first()
    return user_info


# Authenticates the given user returning their info if possible or false otherwise
def authenticate_user(username: str, password: str, session: SessionDep,):
    user = get_user(username, session)
    if not user:
        return False
    if not pbkdf2_sha256.verify(password, user.hashed_password):
        return False
    return user


# Creates an access token with a given expiration
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Login endpoint that returns a token given an authenticated user
@app.post("/token", )
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep,) -> Token:
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# TODO REMOVE
# Temp function to test authentication
@app.get("/test")
async def test_auth(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    return "Works" + token_data.__str__()