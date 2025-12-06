# pdf_utils.py
from typing import List
import base64
import fitz  # PyMuPDF

def pdf_bytes_to_images_b64(pdf_bytes: bytes, dpi: int = 200) -> List[str]:
    """
    Nhận vào bytes của file PDF, trả về list các ảnh PNG
    được encode base64 (mỗi phần tử tương ứng 1 page).
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    images: List[str] = []

    try:
        for page_index in range(len(doc)):
            page = doc.load_page(page_index)
            # convert page -> pixmap. PyMuPDF khuyến nghị dùng get_pixmap/getPixmap để render page. :contentReference[oaicite:1]{index=1}
            pix = page.get_pixmap(dpi=dpi)
            img_bytes = pix.tobytes("png")
            images.append(base64.b64encode(img_bytes).decode("ascii"))
    finally:
        doc.close()

    return images
