from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


user = 'root' 
password = 'nani1234'  
host = 'localhost' 
database = 'education_system'


connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"


engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()