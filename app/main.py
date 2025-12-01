from fastapi import FastAPI
from .database import engine
from .models import Organization, User
from .routers import organization_router, user_router

Organization.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)

app = FastAPI(title="ClientLine Backend", version="1.0.0")

app.include_router(organization_router)
app.include_router(user_router)

@app.get("/")
def read_root():
    return {"message": "ClientLine Backend API", "version": "1.0.0"}
