import datetime

from pydantic import BaseModel, validator, EmailStr


class BaseUser(BaseModel):
    name: str
    surname: str
    gender: int
    email: EmailStr

    @validator('name', 'surname')
    def name_contain_space(cls, v):
        if ' ' in v:
            raise ValueError('Name or surname contain space')
        return v

    class Config:
        orm_mode = True

    @validator("name", "surname")
    def name_contain_numeric(cls, v):
        if not v.isalpha:
            raise ValueError('Name or surname contains numbers')
        return v

    @validator("gender")
    def valid_gender(cls, v):
        if v not in [0, 1, 2]:
            raise ValueError('Gender is entered incorrectly')
        return v


class UserIn(BaseUser):
    password: str


class UserOut(BaseUser):
    id: int
    created_at: datetime.datetime
    is_active: int
