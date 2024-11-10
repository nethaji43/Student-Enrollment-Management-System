# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace with your actual database credentials
user = 'root'  # e.g., 'root'
password = 'nani1234'  # Your MySQL password
host = 'localhost'  # Typically 'localhost' for local development
database = 'education_system'  # The name of your MySQL database

# Create a connection string for MySQL
connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"

# Create an engine and session
engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()