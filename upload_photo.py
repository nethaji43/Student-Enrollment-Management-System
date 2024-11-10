from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Student
import os
import logging


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload_photo/")
def upload_photo(student_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    os.makedirs("student_photos", exist_ok=True)
    file_extension = os.path.splitext(file.filename)[1]
    file_path = f"student_photos/{student_id}{file_extension}"  

    try:
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        print(f"File successfully saved at: {file_path}")
    except Exception as e:
        print(f"Error while saving file: {str(e)}")
        raise HTTPException(status_code=500, detail="Error while saving file")
    

    try:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        print(f"Error while querying student: {str(e)}")
        raise HTTPException(status_code=500, detail="Error querying database for student")
    
    try:
        student.photo_path = file_path
        db.commit()
        print("Database updated successfully")
    except Exception as e:
        db.rollback()  # Rollback in case of failure
        print(f"Error while updating database: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating database with photo path")

    return {"message": "Photo uploaded and path saved in database successfully"}
