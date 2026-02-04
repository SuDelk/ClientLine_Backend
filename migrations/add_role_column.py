from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_role_type_column():
    db = SessionLocal()
    try:
        # Add the column with default value
        db.execute(text("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS "roleType" VARCHAR(50) DEFAULT 'staff' NOT NULL;
        """))
        
        db.commit()
        print("Successfully added roleType column to users table")
        
    except Exception as e:
        db.rollback()
        print(f"Error adding column: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_role_type_column()