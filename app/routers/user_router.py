from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..controllers.user_controller import UserController
from ..models.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return UserController.create_user(user_data, db)

@router.get("/", response_model=List[UserResponse])
def get_users(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    return UserController.get_users(skip, limit, db)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    return UserController.get_user(user_id, db)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    return UserController.update_user(user_id, user_data, db)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return UserController.delete_user(user_id, db)