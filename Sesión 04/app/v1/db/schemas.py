from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    surname: str
    email: str
    password: str

    class Config:
        orm_mode = True
