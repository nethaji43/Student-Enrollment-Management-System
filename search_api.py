import traceback
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from models import Institute, Course, Student
from database import SessionLocal


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/search/")
def search(query: str, db: Session = Depends(get_db)):
    try:
        results = (
            db.query(Institute.institute_name, Course.course_name, Student.student_name, Student.joining_date)
            .join(Course, Student.course_id == Course.course_id)  
            .join(Institute, Student.institute_id == Institute.institute_id)  
            .filter(
                or_(
                    Institute.institute_name.ilike(f"%{query}%"),  
                    Course.course_name.ilike(f"%{query}%"),        
                    Student.student_name.ilike(f"%{query}%")      
                )
            )
            .all()
        )

      
        print(f"Results: {results}")

       
        if not results:
            raise HTTPException(status_code=404, detail="No records found")
        return [
            {
                "institute_name": result[0],
                "course_name": result[1],
                "student_name": result[2],
                "joining_date": result[3].strftime('%d %b %Y') 
            }
            for result in results
        ]

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")