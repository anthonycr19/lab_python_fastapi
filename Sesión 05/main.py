import time

from fastapi import FastAPI, Depends, HTTPException, status, Request, APIRouter
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum

from sqlalchemy.orm import Session

from app.v1.utils.db import get_db, authenticate_user, create_access_token, get_password_hash
from app.v1.model.model import User
from app.v1.schema.schemas import UserCreate, UserOut


from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# Instanciamos la clase FastAPI
app = FastAPI()

@app.middleware("htpp")
async def add_custom_header(request: Request, call_next):
    response = await call_next(Request)
    response.headers["X-Hi-Name"] = "Hi carol! Welcome!"

    return response


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # Realiza une acción algo antes de la operación sobre la ruta coincidente
    start_time = time.time()

    # se ejecutará `add_process_time_header` en el middleware y la API se ejecutará con la ruta coincidente.
    response = await call_next(request)

    # Hará una acción después de la operación en la ruta coincidente
    process_time = time.time() - start_time
    # Añadimos el tiempo a las cabeceras de la respuesta
    response.headers["X-Process-Time"] = str(process_time)
    print(f"Tiempo de procesamiento: {process_time:.4f}")

    return response


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


#router = APIRouter()
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# API para agregar un nuevo usuario en la BD en Postgresql
@app.post("/new_user/", response_model=UserOut)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.hashed_password)
    new_user = User(first_name=user.first_name, last_name=user.last_name, city=user.city,
                    hashed_password=hashed_password, username=user.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/all_users/", response_model=List[UserOut])
def lista_usuarios(db: Session = Depends(get_db)):
    list_users = db.query(User).all()   # Obtenemos todos los usuarios

    return list_users


@app.get("/user/{id}", response_model=UserOut)
def leer_usuario(id: UUID, sesion: Session = Depends(get_db)):
    user = sesion.query(User).get(id)  # Obtener los datos del usuario con el id dado

    # Verificar si el id existe. Si no, devolver respuesta 404 not found
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuario con id {id} no se encuentra la BD")

    return user


@app.put("/user/{id}", response_model=UserOut)
def actualizar_usuario(id: UUID, user_update: UserCreate, sesion: Session = Depends(get_db)):
    user = sesion.query(User).get(id)  # Obtener id dado

    if user:
        user.first_name = user_update.first_name
        user.last_name = user_update.last_name
        user.city = user_update.city
        sesion.commit()

    # Verificar si el id existe. Si no, devolver respuesta 404 not found
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuario con id {id} no encontrada")

    return user


@app.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarea(id: UUID, sesion: Session = Depends(get_db)):

    user = sesion.query(User).get(id)  # Obtener el id dado

    # Si la tarea con el id dado existe, eliminarla de la base de datos. De lo contrario, generar error 404
    if user:
        sesion.delete(user)
        sesion.commit()
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuario con id {id} no encontrado")

    return None


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


