from datetime import datetime
from typing import List,  Optional
import uuid
from pydantic import BaseModel, EmailStr, constr
from fastapi.responses  import JSONResponse

class CustomJSONResponse(JSONResponse):
    
    def __init__(self,  *args, status_code=200, **kwargs):
        # Add CORS headers
        kwargs["headers"] = {
            "Access-Control-Allow-Origin": "*",  # Adjust to your specific requirements
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
        
        super().__init__(*args, status_code=status_code, **kwargs)
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
    jersey_name: str
    jersey_number: int
    class Config:
        orm_mode = True

class CreatePlayerSchema(PlayerBaseSchema):
    def to_dict(self):
        return {
            'name': self.name,
            'jersey_name': self.jersey_name,
            'jersey_number': self.jersey_number
        }

    
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


# Income Schemas

class IncomeBaseSchema(BaseModel):
    name: Optional[str]
    amount: int
    paid_to: str
    comment: str
    # name_id: Optional[uuid.UUID] = None

    class Config:
        orm_mode = True

class CreateIncomeSchema(IncomeBaseSchema):
    pass

    
class IncomeResponse(IncomeBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    name_id: Optional[uuid.UUID] = None

class ListIncomeResponse(BaseModel):
    status: str
    results: int
    incomes: List[IncomeResponse]

class UpdateIncomeSchema(BaseModel):
    name: Optional[str] = None
    amount: Optional[int] = None
    paid_to: Optional[str] = None
    amount: Optional[str] = None
    class Config:
        orm_mode = True


# Expense Schemas

class ExpenseBaseSchema(BaseModel):
    expense_name: Optional[str]
    amount: int
    paid_by: str
    comment: str

    class Config:
        orm_mode = True

class CreateExpenseSchema(ExpenseBaseSchema):
    pass

    
class ExpenseResponse(ExpenseBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class ListExpenseResponse(BaseModel):
    status: str
    results: int
    expenses: List[ExpenseResponse]

class UpdateExpenseSchema(BaseModel):
    expense_name: Optional[str] = None
    amount: Optional[int] = None
    paid_by: Optional[str] = None
    comment: Optional[str] = None
    class Config:
        orm_mode = True