from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()
# Define the database URL (adjust as per your configuration)
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an engine to connect to the database
engine = create_engine(DATABASE_URL, echo=True)

# Create a base class for your models
Base = declarative_base()

# Create a session maker to handle sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Generate a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
