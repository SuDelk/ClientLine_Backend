from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from ..models.user import User, UserCreate, UserUpdate

class UserController:
    @staticmethod
    def create_user(user_data: UserCreate, db: Session):
        try:
            db_user = db.query(User).filter(User.email == user_data.email).first()
            if db_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            
            db_user = User(**user_data.model_dump())
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error occurred")
    
    @staticmethod
    def get_user(user_id: int, db: Session):
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    
    @staticmethod
    def get_users(skip: int, limit: int, db: Session):
        if skip < 0 or limit <= 0 or limit > 1000:
            raise HTTPException(status_code=400, detail="Invalid pagination parameters")
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_user(user_id: int, user_data: UserUpdate, db: Session):
        try:
            db_user = db.query(User).filter(User.id == user_id).first()
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            
            # Check email uniqueness if email is being updated
            if user_data.email and user_data.email != db_user.email:
                existing_user = db.query(User).filter(User.email == user_data.email).first()
                if existing_user:
                    raise HTTPException(status_code=400, detail="Email already registered")
            
            for field, value in user_data.model_dump(exclude_unset=True).items():
                setattr(db_user, field, value)
            
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error occurred")
    
    @staticmethod
    def delete_user(user_id: int, db: Session):
        try:
            db_user = db.query(User).filter(User.id == user_id).first()
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            
            db.delete(db_user)
            db.commit()
            return {"message": "User deleted successfully"}
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error occurred")