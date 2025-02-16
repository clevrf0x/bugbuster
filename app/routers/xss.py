from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.models import XSSComment
from app.database.utils import get_db
import re

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# XSS Home Page
@router.get("/xss", response_class=HTMLResponse)
async def xss_home(request: Request):
    return templates.TemplateResponse("xss/index.html", {"request": request})


# DOM-based XSS Examples
@router.get("/xss/dom/level1", response_class=HTMLResponse)
async def dom_xss_level1(request: Request):
    return templates.TemplateResponse("xss/dom/level1.html", {"request": request})


@router.get("/xss/dom/level2", response_class=HTMLResponse)
async def dom_xss_level2(request: Request):
    return templates.TemplateResponse("xss/dom/level2.html", {"request": request})


@router.get("/xss/dom/level3", response_class=HTMLResponse)
async def dom_xss_level3(request: Request):
    return templates.TemplateResponse("xss/dom/level3.html", {"request": request})


# Reflected XSS Examples
@router.get("/xss/reflected/level1", response_class=HTMLResponse)
async def reflected_xss_level1(request: Request, query: str = ""):
    return templates.TemplateResponse(
        "xss/reflected/level1.html", {"request": request, "query": query}
    )


@router.get("/xss/reflected/level2", response_class=HTMLResponse)
async def reflected_xss_level2(request: Request, query: str = ""):
    # Remove <script> tags and "javascript:" protocol (case-insensitive)
    sanitized_query = re.sub(r"<script.*?>.*?</script>", "", query, flags=re.IGNORECASE)
    sanitized_query = re.sub(r"javascript:", "", sanitized_query, flags=re.IGNORECASE)
    return templates.TemplateResponse(
        "xss/reflected/level2.html", {"request": request, "query": sanitized_query}
    )


@router.get("/xss/reflected/level3", response_class=HTMLResponse)
async def reflected_xss_level3(request: Request, query: str = ""):
    sanitized_query = query.replace("<", "&lt;").replace(">", "&gt;")
    return templates.TemplateResponse(
        "xss/reflected/level3.html", {"request": request, "query": sanitized_query}
    )


# Stored XSS Examples
@router.get("/xss/stored/level1", response_class=HTMLResponse)
async def stored_xss_level1(request: Request, db: Session = Depends(get_db)):
    comments = db.query(XSSComment).filter(XSSComment.level == 1).all()
    return templates.TemplateResponse(
        "xss/stored/level1.html", {"request": request, "comments": comments}
    )


@router.post("/xss/stored/level1", response_class=RedirectResponse)
async def stored_xss_level1_post(
    comment: str = Form(...), db: Session = Depends(get_db)
):
    new_comment = XSSComment(comment=comment, level=1)
    db.add(new_comment)
    db.commit()
    return RedirectResponse(url="/xss/stored/level1", status_code=303)


@router.get("/xss/stored/level2", response_class=HTMLResponse)
async def stored_xss_level2(request: Request, db: Session = Depends(get_db)):
    comments = db.query(XSSComment).filter(XSSComment.level == 2).all()
    return templates.TemplateResponse(
        "xss/stored/level2.html", {"request": request, "comments": comments}
    )


@router.post("/xss/stored/level2", response_class=RedirectResponse)
async def stored_xss_level2_post(
    comment: str = Form(...), db: Session = Depends(get_db)
):
    # Case-insensitive replacement
    sanitized = re.sub(re.escape("<script>"), "", comment, flags=re.IGNORECASE)
    new_comment = XSSComment(comment=sanitized, level=2)
    db.add(new_comment)
    db.commit()
    return RedirectResponse(url="/xss/stored/level2", status_code=303)


@router.get("/xss/stored/level3", response_class=HTMLResponse)
async def stored_xss_level3(request: Request, db: Session = Depends(get_db)):
    comments = db.query(XSSComment).filter(XSSComment.level == 3).all()
    return templates.TemplateResponse(
        "xss/stored/level3.html", {"request": request, "comments": comments}
    )


@router.post("/xss/stored/level3", response_class=RedirectResponse)
async def stored_xss_level3_post(
    comment: str = Form(...), db: Session = Depends(get_db)
):
    # Case-insensitive blacklist-based sanitization (still vulnerable)
    blacklist = ["<script>", "javascript:", "onerror", "onload", "onmouseover"]
    sanitized = comment
    for bad_word in blacklist:
        # Case-insensitive replacement
        sanitized = re.sub(re.escape(bad_word), "", sanitized, flags=re.IGNORECASE)

    new_comment = XSSComment(comment=sanitized, level=3)
    db.add(new_comment)
    db.commit()
    return RedirectResponse(url="/xss/stored/level3", status_code=303)
