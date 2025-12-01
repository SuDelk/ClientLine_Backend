from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..controllers.organization_controller import OrganizationController
from ..models.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse

router = APIRouter(prefix="/organizations", tags=["organizations"])

@router.post("/", response_model=OrganizationResponse)
def create_organization(org_data: OrganizationCreate, db: Session = Depends(get_db)):
    try:
        return OrganizationController.create_organization(org_data, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[OrganizationResponse])
def get_organizations(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    return OrganizationController.get_organizations(skip, limit, db)

@router.get("/{org_id}", response_model=OrganizationResponse)
def get_organization(org_id: int, db: Session = Depends(get_db)):
    return OrganizationController.get_organization(org_id, db)

@router.put("/{org_id}", response_model=OrganizationResponse)
def update_organization(org_id: int, org_data: OrganizationUpdate, db: Session = Depends(get_db)):
    return OrganizationController.update_organization(org_id, org_data, db)

@router.delete("/{org_id}")
def delete_organization(org_id: int, db: Session = Depends(get_db)):
    return OrganizationController.delete_organization(org_id, db)