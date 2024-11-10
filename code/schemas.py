from pydantic import BaseModel

class InstituteCreate(BaseModel):
    institute_name: str

    class Config:
        from_attributes = True

class CourseCreate(BaseModel):
    institute_id: int
    course_name: str

    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    institute_id: int
    course_id: int
    student_name: str
    joining_date: str

    class Config:
        from_attributes = True