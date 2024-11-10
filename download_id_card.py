from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.units import inch
from sqlalchemy.orm import Session
from models import Student, Course, Institute 
from database import SessionLocal
import os

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/download_id_card/")
def download_id_card(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Get course and institute details
    course_name = db.query(Course.course_name).filter(Course.course_id == student.course_id).scalar()
    institute_name = db.query(Institute.institute_name).filter(Institute.institute_id == student.institute_id).scalar()

    if not course_name or not institute_name:
        raise HTTPException(status_code=404, detail="Course or Institute not found")

    # Check for student photo
    file_path_photo = None
    for ext in ['jpg', 'jpeg', 'png']:
        potential_path = f"student_photos/{student_id}.{ext}"
        if os.path.exists(potential_path):
            file_path_photo = potential_path
            break

    if not file_path_photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    # Create the PDF for the ID card
    pdf_file_path = f"{student_id}_id_card.pdf"
    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    elements = []

    # Define the ID card layout data
    data = [
        [f"Student ID Card"],
        [f"Name : {student.student_name}"],
        [f"ID : {student.student_id}"],
        [f"Course: {course_name}"],
        [institute_name],
        [Image(file_path_photo, width=1.5*inch, height=1.5*inch)]  # Add student photo to the ID card
    ]

    # Create the table
    table = Table(data, colWidths=[4*inch])  # Adjust width to 4 inches

    # Set style for the table design
    table.setStyle(TableStyle([
        # Header Row Styling (Student ID Card title)
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),  # Dark blue background for the header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # White text color for the header
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),  # Center align header
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for the header
        ('FONTSIZE', (0, 0), (-1, 0), 18),  # Larger font for the header
        ('BOTTOMPADDING', (0, 0), (-1, 0), 15),  # Padding for header

        # Data Row Styling (Name, ID, Course, Institute)
        ('BACKGROUND', (0, 1), (-1, 4), colors.lightgrey),  # Light grey background for the data rows
        ('TEXTCOLOR', (0, 1), (-1, 4), colors.black),  # Black text for the data rows
        ('ALIGN', (0, 1), (-1, 4), 'CENTER'),  # Center align data rows
        ('FONTNAME', (0, 1), (-1, 4), 'Helvetica'),  # Regular font for data rows
        ('FONTSIZE', (0, 1), (-1, 4), 13),  # Medium font for data rows
        ('TOPPADDING', (0, 1), (-1, 4), 9),  # Top padding for data rows
        ('BOTTOMPADDING', (0, 1), (-1, 4), 9),  # Bottom padding for data rows

        # Photo Styling (Student Photo)
        ('BACKGROUND', (0, 5), (-1, 5), colors.white),  # White background for the photo row
        ('ALIGN', (0, 5), (-1, 5), 'CENTER'),  # Center align the photo
        ('TOPPADDING', (0, 5), (-1, 5), 5),  # Top padding for the photo
        ('BOTTOMPADDING', (0, 5), (-1, 5), 5),  # Bottom padding for the photo

        # Table Borders and Gridlines
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Black gridlines around all cells
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertical alignment to middle
    ]))

    # Add the table to the elements
    elements.append(table)

    # Build the PDF
    doc.build(elements)

    # Return the PDF as a file response
    return FileResponse(pdf_file_path, media_type='application/pdf', filename=f"{student.student_name}_id_card.pdf")

    # Optionally, clean up the file after serving it
    # os.remove(pdf_file_path)
