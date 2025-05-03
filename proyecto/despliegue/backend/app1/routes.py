from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from .ipfs_utils import upload_to_ipfs, download_from_ipfs, remove_from_ipfs
from .db_utils import init_db, save_to_db, delete_page, get_page_by_id
from .sanitizer import sanitize_html, sanitize_css, verify_file_content, get_file_extension
import os

router = APIRouter()

ALLOWED_EXTENSIONS = {'.html', '.css'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

init_db()

@router.get("/health",status_code=200)
async def healthcheck():
	return "OK"


@router.post("/upload")
async def upload_file(
    file_html: UploadFile = File(...),
    file_css: UploadFile = File(...),
    email: str = Form(...)
):
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Email inválido.")

    ext_html = get_file_extension(file_html.filename)
    ext_css = get_file_extension(file_css.filename)

    if ext_html not in ALLOWED_EXTENSIONS or ext_css not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Extensión no permitida.")

    html_bytes = await file_html.read()
    css_bytes = await file_css.read()

    if len(html_bytes) > MAX_FILE_SIZE or len(css_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Archivo demasiado grande.")

    try:
        html_str = html_bytes.decode('utf-8')
        css_str = css_bytes.decode('utf-8')
    except:
        raise HTTPException(status_code=400, detail="Archivo no es UTF-8.")

    if not verify_file_content(html_str, ext_html) or not verify_file_content(css_str, ext_css):
        raise HTTPException(status_code=400, detail="Contenido no válido.")

    html_sanitized = sanitize_html(html_str)
    css_sanitized = sanitize_css(css_str)

    html_cid = upload_to_ipfs(html_sanitized, ext_html)
    css_cid = upload_to_ipfs(css_sanitized, ext_css)

    save_to_db(email, html_cid, css_cid)

    return JSONResponse({
        "message": "Subido a IPFS y guardado.",
        "html_cid": html_cid,
        "css_cid": css_cid
    })

@router.delete("/delete/{email}")
async def delete_page_by_email(email: str):
    delete_page(email)
    return JSONResponse(content={"message": "Página eliminada correctamente."})

@router.get("/sites/{page_id}")
async def get_page(page_id: int):
    page = get_page_by_id(page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Página no encontrada")
    html_cid, css_cid = page
    html = download_from_ipfs(html_cid)
    css = download_from_ipfs(css_cid)

    if "<head>" not in html:
        html = html.replace("<html>", f"<html><head><style>{css}</style></head>")
    else:
        html = html.replace("<head>", f"<head><style>{css}</style>")

    return HTMLResponse(content=html)
