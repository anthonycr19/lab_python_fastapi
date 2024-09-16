from pydantic import BaseModel
from typing import Optional, List

from uuid import UUID

# Esquema de Producto
class ProductBase(BaseModel):
    name_prod: str
    price: float


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int
    class Config:
        orm_mode = True


# Creamos el esquema en base a los campos del modelo de User
class UserBase(BaseModel):
    first_name: str
    last_name: str
    city: str
    username: str
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: UUID    # Debe ser tipo UUID ya que es el tipo de dato con el que se creo en la BD y que viene desde el Modelo
    products: List[ProductOut] = []

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str



