from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.hash import pbkdf2_sha256
from sqlmodel import Session, create_engine, select
from typing import Annotated

from config import *
from schemas.table_schemas import TreeInfo, TreeHistory, Users
from schemas.token_schemas import Token, TokenData


# authentication configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})

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
async def get_tree_info(session: SessionDep):
    info = session.exec(select(TreeInfo))
    return info


# Endpoint that returns the treehistory table
@app.get("/treehistory")
async def get_tree_history(session: SessionDep):
    history = session.exec(select(TreeHistory))
    return history


# Adds new instance to treeinfo table
@app.post("/treeinfo/new", response_model=TreeInfo)
def create_treeinfo(new_treeinfo: TreeInfo, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    # Gets user if possible and checks if user has data modification permissions
    username = authenticate_token(token)
    if not get_user(username, session).data_permissions:
        raise HTTPException(status_code=403, detail="User does not have data permissions")

    session.add(new_treeinfo)
    session.commit()
    session.refresh(new_treeinfo)
    return new_treeinfo


# Adds new instance to treehistory table
@app.post("/treehistory/new", response_model=TreeHistory)
def create_treehistory(new_treehistory: TreeHistory, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    # Gets user if possible and checks if user has data modification permissions
    username = authenticate_token(token)
    if not get_user(username, session).data_permissions:
        raise HTTPException(status_code=403, detail="User does not have data permissions")

    session.add(new_treehistory)
    session.commit()
    session.refresh(new_treehistory)
    return new_treehistory


# Removes an instance from the treeinfo table by tree_id
@app.delete("/treeinfo/delete/{tree_id}", status_code=204)
def delete_treeinfo(tree_id: int, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    # Gets user if possible and checks if user has data modification permissions
    username = authenticate_token(token)
    if not get_user(username, session).data_permissions:
        raise HTTPException(status_code=403, detail="User does not have data permissions")

    target_tree = session.get(TreeInfo, tree_id)
    if not target_tree:
        raise HTTPException(status_code=404, detail="Tree does not exist.")
    target_history = session.exec(select(TreeHistory).where(TreeHistory.Tree_ID == tree_id))
    for hist_id in target_history:
        session.delete(hist_id)
    session.delete(target_tree)
    session.commit()


# Removes an instance from the treehistory table by hist_id
@app.delete("/treehistory/delete/{hist_id}", status_code=204)
def delete_treehistory(hist_id: int, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    # Gets user if possible and checks if user has data modification permissions
    username = authenticate_token(token)
    if not get_user(username, session).data_permissions:
        raise HTTPException(status_code=403, detail="User does not have data permissions")

    history = session.get(TreeHistory, hist_id)
    if not history:
        raise HTTPException(status_code=404, detail="The history you are looking for does not exist.")
    session.delete(history)
    session.commit()


# Endpoint that updates treeinfo table and returns updated instance
@app.patch("/treeinfo/update/{tree_id}", response_model=TreeInfo)
async def update_treeinfo(tree_id: int, new_treeinfo: TreeInfo, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    # Gets user if possible and checks if user has data modification permissions
    username = authenticate_token(token)
    if not get_user(username, session).data_permissions:
        raise HTTPException(status_code=403, detail="User does not have data permissions")

    # Gets tree of interest to update
    target_tree = session.get(TreeInfo, tree_id)
    if not target_tree:
        raise HTTPException(status_code=404, detail="Tree not found")

    # Cleans new data and updates existing instance
    new_treeinfo = new_treeinfo.model_dump(exclude_unset=True)
    target_tree.sqlmodel_update(new_treeinfo)

    # Adds updated instance to table
    session.add(target_tree)
    session.commit()
    session.refresh(target_tree)
    return target_tree


# Endpoint that updates treehistory table and returns updated instance
@app.patch("/treehistory/update/{hist_id}", response_model=TreeHistory)
async def update_treehistory(hist_id: int, new_treehistory: TreeHistory, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    # Gets user if possible and checks if user has data modification permissions
    username = authenticate_token(token)
    if not get_user(username, session).data_permissions:
        raise HTTPException(status_code=403, detail="User does not have data permissions")

    # Gets tree of interest to update
    target_history = session.get(TreeHistory, hist_id)
    if not target_history:
        raise HTTPException(status_code=404, detail="History not found")

    # Cleans new data and updates existing instance
    new_treehistory = new_treehistory.model_dump(exclude_unset=True)
    target_history.sqlmodel_update(new_treehistory)

    # Adds updated instance to table
    session.add(target_history)
    session.commit()
    session.refresh(target_history)
    return target_history


# Adds new user to the site
@app.post("/users/new", response_model=Users)
def create_user(new_user: Users, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    # Gets user if possible and checks if user has user permissions
    username = authenticate_token(token)
    if not get_user(username, session).user_permissions:
        raise HTTPException(status_code=403, detail="User does not have user permissions")

    # TODO add password hashing

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


# Deletes user from the site
@app.delete("/users/delete/{user_id}", status_code=204)
def delete_user(user_id: int, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    # Gets user if possible and checks if user has user permissions
    username = authenticate_token(token)
    if not get_user(username, session).user_permissions:
        raise HTTPException(status_code=403, detail="User does not have user permissions")

    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="The user you are looking for does not exist.")
    session.delete(user)
    session.commit()


# Endpoint that updates users table and returns updated user instance
@app.patch("/users/update/{user_id}", response_model=Users)
async def update_user(user_id: int, new_user: Users, session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    # Gets user if possible and checks if user has user permissions
    username = authenticate_token(token)
    if not get_user(username, session).user_permissions:
        raise HTTPException(status_code=403, detail="User does not have user permissions")

    # Gets tree of interest to update
    target_user = session.get(Users, user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # TODO add password hashing

    # Cleans new data and updates existing instance
    new_user = new_user.model_dump(exclude_unset=True)
    target_user.sqlmodel_update(new_user)

    # Adds updated instance to table
    session.add(target_user)
    session.commit()
    session.refresh(target_user)
    return target_user


# Authenticates that token is real and for valid user, and returns username if true
def authenticate_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    return username


# Login endpoint that returns a token given an authenticated user
@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep) -> Token:
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

# Gets a specified user based off of the given username
def get_user(username: str, session: SessionDep):
    statement = select(Users).where(Users.username == username)
    user_info = session.exec(statement).first()
    return user_info


# Authenticates the given user returning their info if possible or false otherwise
def authenticate_user(username: str, password: str, session: SessionDep):
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
