import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models.documents import Document


@pytest.fixture
def document_data():
    """Fixture with data for document record."""
    return {
        "mechanic_id": 1,
        "type": "passport",
        "file_path": "/path/to/file.pdf",
    }


@pytest.mark.asyncio
async def test_create_document(async_session: AsyncSession, document_data):
    """Test creating a new document record."""
    document = Document(**document_data)
    async_session.add(document)
    await async_session.commit()
    await async_session.refresh(document)

    assert document.document_id is not None
    assert document.mechanic_id == document_data["mechanic_id"]
    assert document.type == document_data["type"]
    assert document.file_path == document_data["file_path"]


@pytest.mark.asyncio
async def test_read_document(async_session: AsyncSession, document_data):
    """Test reading a document record."""
    document = Document(**document_data)
    async_session.add(document)
    await async_session.commit()
    await async_session.refresh(document)

    fetched_document = await async_session.get(Document, document.document_id)
    assert fetched_document is not None
    assert fetched_document.document_id == document.document_id
    assert fetched_document.mechanic_id == document.mechanic_id
    assert fetched_document.type == document.type
    assert fetched_document.file_path == document.file_path


@pytest.mark.asyncio
async def test_update_document(async_session: AsyncSession, document_data):
    """Test updating a document record."""
    document = Document(**document_data)
    async_session.add(document)
    await async_session.commit()
    await async_session.refresh(document)

    document.type = "license"
    document.file_path = "/new/path/to/file.pdf"
    await async_session.commit()
    await async_session.refresh(document)

    updated_document = await async_session.get(Document, document.document_id)
    assert updated_document.type == "license"
    assert updated_document.file_path == "/new/path/to/file.pdf"


@pytest.mark.asyncio
async def test_delete_document(async_session: AsyncSession, document_data):
    """Test deleting a document record."""
    document = Document(**document_data)
    async_session.add(document)
    await async_session.commit()
    await async_session.refresh(document)

    await async_session.delete(document)
    await async_session.commit()

    deleted_document = await async_session.get(Document, document.document_id)
    assert deleted_document is None
