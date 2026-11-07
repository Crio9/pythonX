from fastapi import APIRouter, Depends, HTTPException
from schemas import CreateUserRequest, UserResponse, TaskIn
from schemas.users import UpdateUserRequest
from services.users import UserService

users = []

router = APIRouter(tags=["users"])

@router.post("/users", status_code=201, response_model=UserResponse)
def create_user(raw_user: CreateUserRequest, service: UserService = Depends()):
    user = service.create_user(raw_user)

    if user["success"]:
        return UserResponse(**user)
    else:
        raise HTTPException(status_code=400, detail=user["message"])


@router.get("/users", status_code=200)
def get_users(service: UserService = Depends()):
    users = service.get_all_users()

    return users


@router.get("/user/{username}", status_code=200, response_model=UserResponse)
def get_user_by_username(username: str, service: UserService = Depends()):
    user = service.get_user_by_username(username)

    if user["success"]:
        return UserResponse(**user)
    else:
        raise HTTPException(status_code=404, detail=user["message"])

@router.patch("/users/{username}", status_code=200, response_model=UserResponse)
def update_user(username:str, upd_data: UpdateUserRequest, service: UserService = Depends()):
    user = service.edit_user(username, upd_data)
    if user["success"]:
        return UserResponse(**user)
    else:
        raise HTTPException(status_code=404, detail=user["message"])


@router.delete("/users/{username}", status_code=200)
def delete_user(username: str, service: UserService = Depends()):
    delete_result = service.delete_user(username)
    if delete_result["success"]:
        return delete_result
    else:
        raise HTTPException(status_code=404, detail=delete_result["message"])