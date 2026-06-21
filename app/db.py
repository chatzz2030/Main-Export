"""Database operations and MongoDB helper functions."""
from fastapi import HTTPException
from bson import ObjectId
from bson.errors import InvalidId
from app.config import synopsis_collection
from app.schemas import SynopsisInput

async def _fetch_synopsis(synopsis_id: str) -> SynopsisInput:
    """Pulls the raw document from MongoDB and validates it into our schema."""
    try:
        object_id = ObjectId(synopsis_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid synopsis id format.")

    raw_doc = await synopsis_collection.find_one({"_id": object_id})
    if raw_doc is None:
        raise HTTPException(status_code=404, detail="Synopsis not found.")

    raw_doc.pop("_id", None)
    try:
        return SynopsisInput(**raw_doc)
    except Exception as exc:
        # This means the document stored by M5 doesn't match the agreed
        # schema -- surface it clearly instead of failing inside WeasyPrint.
        raise HTTPException(
            status_code=500,
            detail=f"Stored synopsis is malformed and cannot be exported: {exc}",
        )
