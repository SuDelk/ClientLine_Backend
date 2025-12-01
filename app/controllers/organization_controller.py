from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from ..models.organization import Organization, OrganizationCreate, OrganizationUpdate

class OrganizationController:
    @staticmethod
    def create_organization(org_data: OrganizationCreate, db: Session):
        try:
            db_org = db.query(Organization).filter(Organization.email == org_data.email).first()
            if db_org:
                raise HTTPException(status_code=400, detail="Email already registered")
            
            db_org = Organization(**org_data.model_dump())
            db.add(db_org)
            db.commit()
            db.refresh(db_org)
            return db_org
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error occurred")
    
    @staticmethod
    def get_organization(org_id: int, db: Session):
        db_org = db.query(Organization).filter(Organization.id == org_id).first()
        if not db_org:
            raise HTTPException(status_code=404, detail="Organization not found")
        return db_org
    
    @staticmethod
    def get_organizations(skip: int, limit: int, db: Session):
        if skip < 0 or limit <= 0 or limit > 1000:
            raise HTTPException(status_code=400, detail="Invalid pagination parameters")
        return db.query(Organization).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_organization(org_id: int, org_data: OrganizationUpdate, db: Session):
        try:
            db_org = db.query(Organization).filter(Organization.id == org_id).first()
            if not db_org:
                raise HTTPException(status_code=404, detail="Organization not found")
            
            # Check email uniqueness if email is being updated
            if org_data.email and org_data.email != db_org.email:
                existing_org = db.query(Organization).filter(Organization.email == org_data.email).first()
                if existing_org:
                    raise HTTPException(status_code=400, detail="Email already registered")
            
            for field, value in org_data.model_dump(exclude_unset=True).items():
                setattr(db_org, field, value)
            
            db.commit()
            db.refresh(db_org)
            return db_org
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error occurred")
    
    @staticmethod
    def delete_organization(org_id: int, db: Session):
        try:
            db_org = db.query(Organization).filter(Organization.id == org_id).first()
            if not db_org:
                raise HTTPException(status_code=404, detail="Organization not found")
            
            db.delete(db_org)
            db.commit()
            return {"message": "Organization deleted successfully"}
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error occurred")