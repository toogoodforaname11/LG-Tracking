"""Processing API — trigger AI matching and summarization."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.ai.processor import process_new_documents
from app.api.dependencies import verify_cron_secret

router = APIRouter()


@router.post("/process", dependencies=[Depends(verify_cron_secret)])
async def trigger_processing(db: AsyncSession = Depends(get_db)):
    """Process new documents against active tracks using Gemini.

    Falls back to keyword matching if Gemini API key is not configured.
    """
    stats = await process_new_documents(db)
    return {"status": "completed", "stats": stats}
