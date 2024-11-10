from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Institute(Base):
    __tablename__ = 'institute'
    institute_id = Column(Integer, primary_key=True)
    institute_name = Column(String, unique=True)

class Course(Base):
    __tablename__ = 'course'
    course_id = Column(Integer, primary_key=True)
    institute_id = Column(Integer, ForeignKey('institute.institute_id'))
    course_name = Column(String)

class Student(Base):
    __tablename__ = 'student'
    student_id = Column(Integer, primary_key=True)
    institute_id = Column(Integer, ForeignKey('institute.institute_id'))
    course_id = Column(Integer, ForeignKey('course.course_id'))
    student_name = Column(String)
    joining_date = Column(Date)
