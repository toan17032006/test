"""Upload exercise metadata. File bytes are not written to the host filesystem."""

import hashlib
from fastapi import APIRouter, HTTPException, Request

from routes.state import uploaded_files

router = APIRouter()
MAX_LAB_BODY = 1024 * 1024


@router.post("/upload")
async def upload(request: Request, filename: str = "upload.bin", content_type: str = "application/octet-stream"):
    body = await request.body()
    if len(body) > MAX_LAB_BODY:
        raise HTTPException(status_code=413, detail="Lab upload simulation is limited to 1 MiB")
    file_id = str(len(uploaded_files) + 1)
    row = {"id": file_id, "filename": filename, "content_type": content_type, "size": len(body), "sha256": hashlib.sha256(body).hexdigest(), "public_url": f"/api/v1/files/{file_id}"}
    uploaded_files[file_id] = row
    return {"file": row, "note": "Metadata-only lab simulation; content was discarded"}


@router.get("")
async def list_files():
    return {"items": list(uploaded_files.values()), "total": len(uploaded_files)}


@router.get("/{file_id}")
async def get_file(file_id: str):
    row = uploaded_files.get(file_id)
    if not row:
        raise HTTPException(status_code=404, detail="File not found")
    return row
