from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
