from datetime import datetime
from typing import List,  Optional
import uuid
from pydantic import BaseModel, EmailStr, constr


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr
    photo: str

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    role: str = 'user'
    verified: bool = False


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserResponse(UserBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class FilteredUserResponse(UserBaseSchema):
    id: uuid.UUID


class PostBaseSchema(BaseModel):
    title: str
    content: str
    category: str
    image: str
    user_id: Optional[uuid.UUID] = None

    class Config:
        orm_mode = True


class CreatePostSchema(PostBaseSchema):
    pass


class PostResponse(PostBaseSchema):
    id: uuid.UUID
    user: FilteredUserResponse
    created_at: datetime
    updated_at: datetime


class UpdatePostSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class ListPostResponse(BaseModel):
    status: str
    results: int
    posts: List[PostResponse]


class PlayerBaseSchema(BaseModel):
    name: str
    class Config:
        orm_mode = True

class CreatePlayerSchema(PlayerBaseSchema):
    pass

    
class PlayerResponse(PlayerBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class ListPlayerResponse(BaseModel):
    status: str
    results: int
    players: List[PlayerResponse]

class UpdatePlayerSchema(BaseModel):
    name: Optional[str] = None
    class Config:
        orm_mode = True