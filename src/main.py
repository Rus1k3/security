from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import bleach
from fastapi import Response

app = FastAPI()
templates = Jinja2Templates(directory="templates")

comments = []

@app.get("/comments", response_class=HTMLResponse)
def get_comments(request: Request):
    return templates.TemplateResponse("comments.html", {
        "request": request,
        "comments": comments
    })

@app.post("/comments", response_class=HTMLResponse)
def post_comment(request: Request, text: str = Form(...)):
    clean_text = sanitize_html(text)
    comments.append(clean_text)
    return templates.TemplateResponse("comments.html", {
        "request": request,
        "comments": comments
    })


ALLOWED_TAGS = ['b', 'i', 'u', 'em', 'strong']

def sanitize_html(text: str) -> str:
    return bleach.clean(
        text,
        tags=ALLOWED_TAGS,
        attributes={},
        strip=True
    )

@app.middleware("http")
async def add_csp_header(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'"
    )
    return response