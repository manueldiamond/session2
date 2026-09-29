from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    username: str
    email: EmailStr = None
    full_name: str 
    disabled: bool | None = None

class RegisterRequest(User):
    password: str

class UserInDB(User):
    hashed_password: str
class LoginRequest(BaseModel):
    username: str
    password: str

class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    description: str

class CartItem(BaseModel):
    product_id:int
