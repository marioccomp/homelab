import uuid
import shutil
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from sqlalchemy import select


from app.config import settings
from app.files.models import File, Folder

STORAGE_DIR = Path(settings.storage_dir)
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

def _safe_path(relative: str) -> Path:
    base = STORAGE_DIR.resolve()
    path = (base / relative).resolve()
    if not path.is_relative_to(base):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Caminho inválido")
    return path


def save_upload(db: Session, folder_path: str | None, upload: UploadFile) -> File:

    storage_filename = f"{uuid.uuid4().hex}_{upload.filename}"
    target_dir = _safe_path(folder_path) if folder_path else STORAGE_DIR.resolve()

    if not target_dir.is_dir():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pasta não encontrada")

    destination = target_dir / storage_filename

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

def list_files(db: Session) -> None:
    storage_base = STORAGE_DIR
    for item in storage_base.iterdir():
        print(item)

def create_folder(db: Session, folder_name: str) -> Folder:
    stmt = select(Folder).where(Folder.name == folder_name)
    result = db.execute(stmt).scalar_one_or_none()
    if result == None:
        print('Nao tem pasta com esse nome')
        path = Path(STORAGE_DIR) / folder_name
        folder_record = Folder(
            name = folder_name
        )
        path.mkdir(parents=True, exist_ok=True)
        db.add(folder_record)
        db.commit()
        db.refresh(folder_record)
        return folder_record
    else:
        print('tem pasta com esse nome')
        return None



