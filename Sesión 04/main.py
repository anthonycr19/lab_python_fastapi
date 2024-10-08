from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum

#from .db.model import UserModel
from app.v1.db.database import engine

# instanciamos la clase FastAPI
app = FastAPI()


class Post(BaseModel):
    author: str
    title: str
    content: str
    tags: str


class Role(str, Enum):
    admin = "admin"
    user = "user"


class User(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    city: str
    roles: List[Role]


# Creamos un nuevo modelo para realizar la actualización de registros en la BD en memoria
class UpdateUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    roles: Optional[List[Role]]


@app.get("/")
async def root():
    return {"name": "Carolina Gutierrez"}


@app.get('/posts/{id}')
def getPost(id):
    return {"data": id}


@app.post('/posts')
def addPost(post: Post):
    return {"message": f"The post {post.title} has been added"}


@app.get("/api/v1/users")
def get_users():
    return db


@app.post("/api/v1/users")
async def create_user(user: User):
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{id}")
def delete_user(id: UUID):
    for user in db:
        if user.id == id:
            db.remove(user)
            return


@app.put("/api/v1/users/{id}")
async def update_user(user_update: UpdateUser, id: UUID):
    for user in db:
        if user.id == id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.roles is not None:
                user.roles = user_update.roles
        return user.id
    #raise HTTPException(status_code=404, detail=f"Could not find user with id: {id}")

#Migración de modelos a mi BD.



db: List[User] = [
    User(
        id=uuid4(),
        first_name="Freddy",
        last_name="Nolasco",
        city="Lima",
        roles=[Role.user],
    ),
    User(
        id=uuid4(),
        first_name="Juana",
        last_name="Falcón",
        city="Trujillo",
        roles=[Role.admin],
    ),
    User(
        id=uuid4(),
        first_name="Noelia",
        last_name="Perez",
        city="Lima",
        roles=[Role.user],
    ),
    User(
        id=uuid4(),
        first_name="Edwin",
        last_name="Deza",
        city="Cusco",
        roles=[Role.admin, Role.user],
    ),
]


