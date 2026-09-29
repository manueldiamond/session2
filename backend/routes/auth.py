from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from db import delete_user_by_id, get_user, get_db, get_user_by_id, get_user_with_password, get_users,create_user
from auth import get_access_token, get_user_auth, verify_password
from schemas import RegisterRequest, LoginRequest, User, UserInDB

auth_routes = APIRouter()

@auth_routes.post("/register")
def register(user: RegisterRequest):
    user = get_user(user.username)
    if user is not None:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = hash_password(user.password)

    create_user(user.username, user.full_name, user.email, hashed_password)
    
    return {
        "success": True,
        "message": "User registered successfully",
    }
 
 
    
@auth_routes.get("/users")
def get_users() -> list[User]:
    users_raw_list= list(c.execute("SELECT * FROM users").fetchall())
    
    return [User(**user) for user in users_raw_list]

@auth_routes.delete("/users/{id}")
def delete_user(id:int):
    user = get_user_by_id(id)
    if user is None:
        raise HTTPException(status_code=400, detail="User does not exist")
    delete_user_by_id(id)

    return {
        "success": True,
        "message": "User deleted successfully",
    }


#get user credentials, check if user exists, check if password hash matches , return jwt tokens

@auth_routes.post("/login")
def login(user: LoginRequest):
    user = get_user_with_password(user.username)
    if user is None:
        raise HTTPException(status_code=400, detail="User does not exist")
    valid = verify_password(user.password, user.hashed_password)
    
    if not valid:
        raise HTTPException(
            status_code=401,
            detail = "invalid credentials"
        )

    access_token = get_access_token(user.id, user.username)
    
    return {
        "access_token": access_token,
    }
    
    
    
@auth_routes.get("/user/me")
def get_user_me(auth_user = Depends(get_user_auth)):
    
    id = auth_user["id"]
    
    user = get_user_by_id(id)

    return {
       "user": user
    }