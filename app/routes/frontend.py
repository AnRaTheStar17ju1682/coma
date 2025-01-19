from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from routes.dependencies import tag_search_api_request


router = APIRouter(tags=["frontend"])
templates = Jinja2Templates("static/html")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    html = templates.TemplateResponse(request, "index.html.jinja")
    return html


@router.get("/items/", response_class=FileResponse)
async def posts(
    request: Request,
    item_hashes: Annotated[list[str], Depends(tag_search_api_request)]
):
    context = {
        "request": request,
        "item_hashes": item_hashes,
    }
    html = templates.TemplateResponse("items.html.jinja", context=context)
    return html