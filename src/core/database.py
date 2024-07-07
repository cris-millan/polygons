from src.core.config import configs
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/sinecta"
# SQLALCHEMY_DATABASE_URL = configs.DATABASE_URI
print({"SQLALCHEMY_DATABASE_URL": SQLALCHEMY_DATABASE_URL})

# Create Engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
# Create a local session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for the models.
Base = declarative_base()


# dependencies to get database session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()