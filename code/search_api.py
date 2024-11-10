import traceback
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from models import Institute, Course, Student
from database import SessionLocal

# Initialize the router
router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Search API: Search by institute name, course name, or student name
@router.post("/search/")
def search(query: str, db: Session = Depends(get_db)):
    try:
        # Perform the query to search across Institute, Course, and Student tables
        results = (
            db.query(Institute.institute_name, Course.course_name, Student.student_name, Student.joining_date)
            .join(Course, Student.course_id == Course.course_id)  # Join the Course table with the Student table
            .join(Institute, Student.institute_id == Institute.institute_id)  # Join the Institute table with the Student table
            .filter(
                or_(
                    Institute.institute_name.ilike(f"%{query}%"),  # Case-insensitive search on institute name
                    Course.course_name.ilike(f"%{query}%"),        # Case-insensitive search on course name
                    Student.student_name.ilike(f"%{query}%")       # Case-insensitive search on student name
                )
            )
            .all()
        )

        # Logging for debugging
        print(f"Results: {results}")

        # Raise an exception if no records are found
        if not results:
            raise HTTPException(status_code=404, detail="No records found")

        # Return the response in the required format
        return [
            {
                "institute_name": result[0],
                "course_name": result[1],
                "student_name": result[2],
                "joining_date": result[3].strftime('%d %b %Y')  # Format the date
            }
            for result in results
        ]

    except Exception as e:
        # Log the full stack trace for better debugging
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")