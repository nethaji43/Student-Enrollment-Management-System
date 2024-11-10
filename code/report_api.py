from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from models import Institute, Course, Student  # Ensure models are correctly imported
from database import SessionLocal  # Import your session setup
from typing import Optional

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/report/")
def get_report(
    year: Optional[int] = Query(None, description="Filter by year"),
    month: Optional[int] = Query(None, description="Filter by month"),
    institute_name: Optional[str] = Query(None, description="Filter by institute name"),
    course_name: Optional[str] = Query(None, description="Filter by course name"),
    db: Session = Depends(get_db)
):
    # Query to get the basic data
    query = (
        db.query(
            func.extract('year', Student.joining_date).label('year'),
            func.extract('month', Student.joining_date).label('month'),
            Institute.institute_name,
            Course.course_name,
            func.count(Student.student_id).label('registered_student_count')
        )
        .join(Course, Student.course_id == Course.course_id)
        .join(Institute, Student.institute_id == Institute.institute_id)
    )

    # Apply filters if query parameters are provided
    if year:
        query = query.filter(func.extract('year', Student.joining_date) == year)
    if month:
        query = query.filter(func.extract('month', Student.joining_date) == month)
    if institute_name:
        query = query.filter(Institute.institute_name.ilike(f"%{institute_name}%"))
    if course_name:
        query = query.filter(Course.course_name.ilike(f"%{course_name}%"))

    # Group by year, month, institute name, and course name
    report_data = query.group_by(
        func.extract('year', Student.joining_date),
        func.extract('month', Student.joining_date),
        Institute.institute_name,
        Course.course_name
    ).all()

    if not report_data:
        raise HTTPException(status_code=404, detail="No data found with given filters")

    # Structure the response data
    return [
        {
            "Year": int(row.year),
            "Month": int(row.month),
            "institute_name": row.institute_name,
            "course_name": row.course_name,
            "student_count": row.registered_student_count,
        }
        for row in report_data
    ]
