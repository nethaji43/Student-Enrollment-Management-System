from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Institute, Course, Student
from schemas import InstituteCreate, CourseCreate, StudentCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Operations for Institute
@router.post("/institutes/")
def create_institute(institute: InstituteCreate, db: Session = Depends(get_db)):
    db_institute = Institute(institute_name=institute.institute_name)
    db.add(db_institute)
    db.commit()
    db.refresh(db_institute)
    return db_institute

@router.get("/institutes/{institute_id}")
def read_institute(institute_id: int, db: Session = Depends(get_db)):
    institute = db.query(Institute).filter(Institute.institute_id == institute_id).first()
    if not institute:
        raise HTTPException(status_code=404, detail="Institute not found")
    return institute

@router.put("/institutes/{institute_id}")
def update_institute(institute_id: int, institute: InstituteCreate, db: Session = Depends(get_db)):
    db_institute = db.query(Institute).filter(Institute.institute_id == institute_id).first()
    if not db_institute:
        raise HTTPException(status_code=404, detail="Institute not found")
    db_institute.institute_name = institute.institute_name
    db.commit()
    db.refresh(db_institute)
    return db_institute

@router.delete("/institutes/{institute_id}")
def delete_institute(institute_id: int, db: Session = Depends(get_db)):
    institute = db.query(Institute).filter(Institute.institute_id == institute_id).first()
    if not institute:
        raise HTTPException(status_code=404, detail="Institute not found")
    db.delete(institute)
    db.commit()
    return {"message": "Institute deleted successfully"}

# CRUD Operations for Course
@router.post("/courses/")
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(institute_id=course.institute_id, course_name=course.course_name)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/courses/{course_id}")
def read_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/courses/{course_id}")
def update_course(course_id: int, course: CourseCreate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.course_id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    db_course.institute_id = course.institute_id
    db_course.course_name = course.course_name
    db.commit()
    db.refresh(db_course)
    return db_course

@router.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}

# CRUD Operations for Student
@router.post("/students/")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(
        institute_id=student.institute_id,
        course_id=student.course_id,
        student_name=student.student_name,
        joining_date=student.joining_date
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/students/{student_id}")
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/students/{student_id}")
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.student_id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student.institute_id = student.institute_id
    db_student.course_id = student.course_id
    db_student.student_name = student.student_name
    db_student.joining_date = student.joining_date
    db.commit()
    db.refresh(db_student)
    return db_student

@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}
