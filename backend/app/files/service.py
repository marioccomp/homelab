import uuid
import shutil
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.config import settings
from app.files.models import File

STORAGE_DIR = Path(settings.storage_dir)
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

def save_upload(db: Session, upload: UploadFile) -> File:
    storage_filename = f"{uuid.uuid4().hex}_{upload.filename}"
    destination = STORAGE_DIR / storage_filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(upload.file, buffer) # chunks

    file_record = File(
        original_filename = upload.filename,
        storage_filename = storage_filename,
        content_type = upload.content_type,
        size_bytes = destination.stat().st_size,
    )

    db.add(file_record)
    db.commit()
    db.refresh(file_record)
    return file_record