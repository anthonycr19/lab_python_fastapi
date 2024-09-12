import time

from fastapi import FastAPI, Depends, HTTPException, status, Request
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum

from sqlalchemy.orm import Session

from app.v1.utils.db import get_db
from app.v1.model.model import User
from app.v1.schema.schemas import UserCreate, UserOut

# Instanciamos la clase FastAPI
app = FastAPI()


# Modelos que se usarán para interactuar para la B.D. en memoria
class Post(BaseModel):
    author: str
    title: str
    content: str
    tags: str


class Role(str, Enum):
    admin = "admin"
    user = "user"


class UserA(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    city: str
    roles: List[Role]


class UpdateUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    roles: Optional[List[Role]]


# Creamos APIs que afectarán a la BD en memoria que tenemos líneas abajo (db_m)
@app.get("/")
async def root():
    return {"name": "Carolina Gutierrez", "city": "Lima", "age": 24}


@app.get('/posts/{id}')
def getPost(id):
    return {"data": id}


@app.post('/posts')
def addPost(post: Post):
    return {"message": f"The post {post.title} has been added"}


@app.get("/api/v1/users")
def get_users():
    return db_m


@app.post("/api/v1/users")
def create_user(user: UserA):
    db_m.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{id}")
def delete_user(id: UUID):
    for user in db_m:
        if user.id == id:
            db_m.remove(user)
            return


@app.put("/api/v1/user/{id}")
def update_user(id: UUID, user_update: UpdateUser):
    for user in db_m:
        if user.id == id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.roles is not None:
                user.roles = user_update.roles
        return user.id


# Creamos una Base de Datos en memoria
db_m: List[UserA] = [
    UserA(
        id=uuid4(),
        first_name="Freddy",
        last_name="Nolasco",
        city="Lima",
        roles=[Role.user],
    ),
    UserA(
        id=uuid4(),
        first_name="Juana",
        last_name="Falcón",
        city="Trujillo",
        roles=[Role.admin],
    ),
    UserA(
        id=uuid4(),
        first_name="Noelia",
        last_name="Perez",
        city="Lima",
        roles=[Role.user],
    ),
    UserA(
        id=uuid4(),
        first_name="Edwin",
        last_name="Deza",
        city="Cusco",
        roles=[Role.admin, Role.user],
    ),
]


