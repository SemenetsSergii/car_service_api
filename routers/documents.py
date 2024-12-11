from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends,
    Form,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.engine import get_async_db
from models.documents import Document
from models.mechanics import Mechanic
from schemas.documents import DocumentRead
import os
import aiofiles

router = APIRouter()

UPLOAD_FOLDER = "uploaded_files/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


async def validate_mechanic(mechanic_id: int, db: AsyncSession):
    """Validate if a mechanic exists."""
    stmt = select(Mechanic).where(Mechanic.mechanic_id == mechanic_id)
    mechanic = (await db.execute(stmt)).scalar_one_or_none()
    if not mechanic:
        raise HTTPException(status_code=404, detail="Mechanic not found.")
    return mechanic


@router.post("/", response_model=DocumentRead, status_code=201)
async def create_document_with_file(
    mechanic_id: int = Form(...),
    type: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_db),
):
    """Create a new document record in the database and upload a file."""
    await validate_mechanic(mechanic_id, db)

    stmt = select(Document).where(
        Document.mechanic_id == mechanic_id, Document.type == type
    )
    existing_document = (await db.execute(stmt)).scalar_one_or_none()

    if existing_document:
        raise HTTPException(
            status_code=400,
            detail=f"A document with type '{type}' "
                   f"already exists for this mechanic.",
        )

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    if os.path.exists(file_path):
        raise HTTPException(
            status_code=400,
            detail="A file with the same name already"
                   " exists. Please rename your file.",
        )

    try:
        async with aiofiles.open(file_path, "wb") as buffer:
            while content := await file.read(1024):
                await buffer.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )

    new_document = Document(
        mechanic_id=mechanic_id,
        type=type,
        file_path=file_path
    )
    db.add(new_document)
    await db.commit()
    await db.refresh(new_document)
    return new_document


@router.get("/", response_model=list[DocumentRead])
async def get_all_documents(db: AsyncSession = Depends(get_async_db)):
    """Retrieve all documents."""
    stmt = select(Document)
    documents = (await db.execute(stmt)).scalars().all()
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found.")
    return documents


@router.get("/{document_id}", response_model=DocumentRead)
async def get_document(
        document_id: int,
        db: AsyncSession = Depends(get_async_db)
):
    """Retrieve a document by ID."""
    stmt = select(Document).where(Document.document_id == document_id)
    document = (await db.execute(stmt)).scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")
    return document


@router.put("/{document_id}", response_model=DocumentRead)
async def update_document(
    document_id: int,
    mechanic_id: int = Form(...),
    type: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_db),
):
    """Update document details, including file upload."""
    stmt = select(Document).where(Document.document_id == document_id)
    document = (await db.execute(stmt)).scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    await validate_mechanic(mechanic_id, db)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    if os.path.exists(file_path) and file_path != document.file_path:
        raise HTTPException(
            status_code=400, detail="A file with the same name already exists."
        )

    try:
        async with aiofiles.open(file_path, "wb") as buffer:
            while content := await file.read(1024):
                await buffer.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}"
        )

    if document.file_path != file_path:
        try:
            os.remove(document.file_path)
        except FileNotFoundError:
            pass

    document.mechanic_id = mechanic_id
    document.type = type
    document.file_path = file_path

    await db.commit()
    await db.refresh(document)
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
        document_id: int,
        db: AsyncSession = Depends(get_async_db)
):
    """Delete a document by ID."""
    stmt = select(Document).where(Document.document_id == document_id)
    document = (await db.execute(stmt)).scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    file_path = document.file_path
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except OSError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete file '{file_path}': {str(e)}"
            )

    await db.delete(document)
    await db.commit()

    return {"message": f"Document with ID {document_id}"
                       f" has been successfully deleted."}
