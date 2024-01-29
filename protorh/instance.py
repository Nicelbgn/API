from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

#print(os.environ.get('DATABASE_USER'))
DATABASE_URL = f"postgresql://{os.environ.get('DATABASE_USER')}:{os.environ.get('DATABASE.PASSWORD')}@{os.environ.get('DATABASE_HOST')}/{os.environ.get('DATABASE_NAME')}"
engine = create_engine(DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url,template="template0")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
