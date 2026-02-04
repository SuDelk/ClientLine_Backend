from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError, OperationalError
from fastapi import HTTPException
import logging
from ..models.user import User, UserCreate, UserUpdate

logger = logging.getLogger(__name__)

class UserController:
    @staticmethod
    def _validate_user_id(user_id: int):
        if user_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid user ID")
    
    @staticmethod
    def _validate_organization(organization_id: int, db: Session):
        if organization_id:
            from ..models.organization import Organization
            org = db.query(Organization).filter(Organization.id == organization_id).first()
            if not org:
                raise HTTPException(status_code=400, detail="Organization not found")
    
    @staticmethod
    def _handle_db_error(e: Exception, operation: str, entity_id: str = ""):
        if isinstance(e, HTTPException):
            raise
        elif isinstance(e, IntegrityError):
            if "unique constraint" in str(e).lower():
                raise HTTPException(status_code=400, detail="Email already exists")
            elif "foreign key constraint" in str(e).lower():
                raise HTTPException(status_code=400, detail="Invalid organization ID")
            else:
                raise HTTPException(status_code=400, detail="Data validation error")
        elif isinstance(e, DataError):
            raise HTTPException(status_code=400, detail="Invalid data format")
        elif isinstance(e, OperationalError):
            raise HTTPException(status_code=503, detail="Database unavailable")
        elif isinstance(e, SQLAlchemyError):
            raise HTTPException(status_code=500, detail="Database error occurred")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @staticmethod
    def create_user(user_data: UserCreate, db: Session):
        try:
            # Check email uniqueness
            db_user = db.query(User).filter(User.email == user_data.email).first()
            if db_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            
            UserController._validate_organization(user_data.organization_id, db)
            
            # Create user with hashed password
            user_dict = user_data.model_dump()
            password = user_dict.pop('password')
            db_user = User(**user_dict)
            db_user.set_password(password)
            
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            logger.info(f"User created: {db_user.email}")
            return db_user
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating user: {str(e)}")
            UserController._handle_db_error(e, "create")
    
    @staticmethod
    def get_user(user_id: int, db: Session):
        try:
            UserController._validate_user_id(user_id)
            
            db_user = db.query(User).filter(User.id == user_id).first()
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            return db_user
            
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {str(e)}")
            UserController._handle_db_error(e, "get", str(user_id))
    
    @staticmethod
    def get_users(skip: int, limit: int, db: Session):
        try:
            if skip < 0:
                raise HTTPException(status_code=400, detail="Skip must be non-negative")
            if limit <= 0 or limit > 1000:
                raise HTTPException(status_code=400, detail="Limit must be between 1 and 1000")
                
            return db.query(User).offset(skip).limit(limit).all()
            
        except Exception as e:
            logger.error(f"Error getting users: {str(e)}")
            UserController._handle_db_error(e, "get_all")
    
    @staticmethod
    def update_user(user_id: int, user_data: UserUpdate, db: Session):
        try:
            UserController._validate_user_id(user_id)
            
            db_user = db.query(User).filter(User.id == user_id).first()
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            
            # Check email uniqueness if email is being updated
            if user_data.email and user_data.email != db_user.email:
                existing_user = db.query(User).filter(User.email == user_data.email).first()
                if existing_user:
                    raise HTTPException(status_code=400, detail="Email already registered")
            
            UserController._validate_organization(user_data.organization_id, db)
            
            # Handle password update if provided
            user_dict = user_data.model_dump(exclude_unset=True)
            if 'password' in user_dict:
                password = user_dict.pop('password')
                db_user.set_password(password)
            
            for field, value in user_dict.items():
                setattr(db_user, field, value)
            
            db.commit()
            db.refresh(db_user)
            logger.info(f"User updated: {user_id}")
            return db_user
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating user {user_id}: {str(e)}")
            UserController._handle_db_error(e, "update", str(user_id))
    
    @staticmethod
    def delete_user(user_id: int, db: Session):
        try:
            UserController._validate_user_id(user_id)
            
            db_user = db.query(User).filter(User.id == user_id).first()
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            
            db.delete(db_user)
            db.commit()
            logger.info(f"User deleted: {user_id}")
            return {"message": "User deleted successfully"}
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting user {user_id}: {str(e)}")
            if isinstance(e, IntegrityError):
                raise HTTPException(status_code=400, detail="Cannot delete user with dependencies")
            UserController._handle_db_error(e, "delete", str(user_id))