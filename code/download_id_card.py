from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib import colors
from sqlalchemy.orm import Session
from models import Student, Course, Institute  # Import the models
from database import SessionLocal
import os

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/download_id_card/")
def download_id_card(student_id: int, db: Session = Depends(get_db)):
    # Fetch student data from the database
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Fetch related course and institute data
    course_name = db.query(Course.course_name).filter(Course.course_id == student.course_id).scalar()
    institute_name = db.query(Institute.institute_name).filter(Institute.institute_id == student.institute_id).scalar()

    if not course_name or not institute_name:
        raise HTTPException(status_code=404, detail="Course or Institute not found")

    # Handle image path - allowing multiple file extensions (jpg, png, etc.)
    file_path_photo = None
    for ext in ['jpg', 'jpeg', 'png']:
        potential_path = f"student_photos/{student_id}.{ext}"
        if os.path.exists(potential_path):
            file_path_photo = potential_path
            break

    if not file_path_photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    # Generate PDF ID card using ReportLab
    pdf_file_path = f"{student_id}_id_card.pdf"
    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    elements = []

    # Add data to the PDF table
    data = [
        [f"Student ID Card for {student.student_name}"],
        [f"Course: {course_name}"],
        [f"Institution: {institute_name}"],
        [Image(file_path_photo, width=100, height=100)],  # Add student photo to the ID card
    ]

    # Define table style
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
    ]))

    elements.append(table)

    # Build the PDF
    doc.build(elements)

    # Return the generated PDF as a file response
    return FileResponse(pdf_file_path, media_type='application/pdf', filename=f"{student.student_name}_id_card.pdf")

    # Optionally: Clean up the generated file after sending (use background task if needed)
