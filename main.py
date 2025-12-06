# main.py
from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from pdf_utils import pdf_bytes_to_images_b64

app = FastAPI(
    title="PDF to Images Service",
    description="Upload 1 file PDF, nhận lại list ảnh PNG (base64) cho từng trang.",
    version="1.0.0",
)


@app.get("/")
async def health_check():
    return {"status": "ok", "message": "PDF2Image service is running"}


@app.post("/pdf2images")
async def pdf2images(file: UploadFile = File(...), dpi: int = 200):
    """
    - Input: 1 file PDF dạng form-data, field name = 'file'
    - Output: JSON gồm page_count + list images (base64 PNG)
    """
    if file.content_type not in (
        "application/pdf",
        "application/x-pdf",
        "binary/octet-stream",
    ):
        raise HTTPException(status_code=400, detail="File phải là PDF")

    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="File rỗng")

    try:
        images_b64: List[str] = pdf_bytes_to_images_b64(pdf_bytes, dpi=dpi)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý PDF: {e}")

    return JSONResponse(
        {
            "page_count": len(images_b64),
            "dpi": dpi,
            "images": images_b64,
            # Nếu muốn có prefix sẵn dùng cho <img src="...">:
            # "images": [f"data:image/png;base64,{img}" for img in images_b64],
        }
    )
