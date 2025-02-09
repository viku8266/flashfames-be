from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Update the database URL for MySQL
DATABASE_URL = "mysql+pymysql://root:password@127.0.0.1:3306/flashfames_2"

# Create a new SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a base class for declarative class definitions
Base = declarative_base()

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
session = Session() 