from fastapi import FastAPI
from crud_api import router as crud_router
from search_api import router as search_router
from report_api import router as report_router
from upload_photo import router as upload_photo_router
from download_id_card import router as download_id_card_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application"}


app.include_router(crud_router)
app.include_router(search_router)
app.include_router(report_router)
app.include_router(upload_photo_router)
app.include_router(download_id_card_router)
