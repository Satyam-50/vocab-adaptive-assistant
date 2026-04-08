from __future__ import annotations

from io import BytesIO

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pypdf import PdfReader

from backend.app.api.dependencies import get_adaptive_service
from backend.app.core.config import settings
from backend.app.schemas.response_schema import AnalyzeResponse
from backend.app.schemas.text_schema import AnalyzeRequest
from backend.app.services.adaptive_service import AdaptiveService


router = APIRouter(tags=["analysis"])


def extract_text_from_pdf(content: bytes, max_pages: int, max_chars: int) -> str:
	reader = PdfReader(BytesIO(content))
	pages: list[str] = []
	for page in reader.pages[:max_pages]:
		page_text = page.extract_text() or ""
		if page_text.strip():
			pages.append(page_text)
		if sum(len(chunk) for chunk in pages) >= max_chars:
			break

	combined = "\n".join(pages).strip()
	if len(combined) > max_chars:
		return combined[:max_chars]
	return combined


def get_upload_size_bytes(file: UploadFile) -> int:
	stream = file.file
	position = stream.tell()
	stream.seek(0, 2)
	size = stream.tell()
	stream.seek(position)
	return int(size)


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_text(payload: AnalyzeRequest, adaptive_service: AdaptiveService = Depends(get_adaptive_service)) -> AnalyzeResponse:
	if not payload.text.strip():
		raise HTTPException(status_code=400, detail="text must not be empty")
	return adaptive_service.analyze(payload.text)


@router.post("/analyze/pdf", response_model=AnalyzeResponse)
async def analyze_pdf(
	pdf_file: UploadFile = File(...),
	adaptive_service: AdaptiveService = Depends(get_adaptive_service),
) -> AnalyzeResponse:
	if not (pdf_file.filename or "").lower().endswith(".pdf"):
		raise HTTPException(status_code=400, detail="Only PDF files are supported")

	max_pdf_bytes = settings.pdf_max_size_mb * 1024 * 1024
	file_size = get_upload_size_bytes(pdf_file)
	if file_size > max_pdf_bytes:
		raise HTTPException(
			status_code=413,
			detail=f"PDF too large. Maximum supported size is {settings.pdf_max_size_mb} MB.",
		)

	content = await pdf_file.read()
	if not content:
		raise HTTPException(status_code=400, detail="Uploaded PDF is empty")

	try:
		text = extract_text_from_pdf(
			content,
			max_pages=settings.pdf_max_pages,
			max_chars=settings.pdf_max_chars,
		)
	except Exception as exc:  # noqa: BLE001
		raise HTTPException(status_code=400, detail="Failed to parse PDF") from exc

	if not text:
		raise HTTPException(
			status_code=400,
			detail="No readable text found in PDF. Handwritten or scanned-image PDFs need OCR before analysis.",
		)

	return adaptive_service.analyze(text)

