from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLITE_DB_URL = "sqlite:///mydatabase.db"

# Create the engine that will connect to the SQLite database
engine = create_engine(SQLITE_DB_URL, echo=True)

# Create a declarative base class
Base = declarative_base()


# Create a session factory, which we will use to create new sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    # This will create the tables if they don't exist already.
    # It's a good idea to separate this from the Base declaration
    # so that you can call it explicitly when starting your app.
    Base.metadata.create_all(bind=engine)
