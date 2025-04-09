import sqlmodel
from sqlmodel import SQLModel, Session
import timescaledb

from .config import DATABASE_URL, DB_TIMEZONE

if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL is not set. Please set it in the config file.")

engine = timescaledb.create_engine(DATABASE_URL, timezone=DB_TIMEZONE)

def init_db():
  print("Initializing database...")
  SQLModel.metadata.create_all(engine)
  print("Creating hypertables")
  timescaledb.metadata.create_all(engine)

def get_session():
   with Session(engine) as session:
       yield session


