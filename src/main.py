from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import bleach
from fastapi import Response
from fastapi import Depends, HTTPException, Path
from schemas import User, File


app = FastAPI()
templates = Jinja2Templates(directory="templates")
comments = []


users_db = [
    User(id=1, username="alice", role="user"),
    User(id=2, username="bob", role="user"),
    User(id=3, username="admin", role="admin"),
]

files_db = [
    File(id=1, filename="alice_report.pdf", size=1234, owner_id=1),
    File(id=2, filename="bob_report.pdf", size=5678, owner_id=2),
    File(id=3, filename="admin_log.txt", size=999, owner_id=3),
]


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


def get_current_user(user_id: int) -> User:
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=401, detail="Unauthorized")


def check_file_permissions(
    file_id: int = Path(...),
    current_user: User = Depends(get_current_user)
):
    for file in files_db:
        if file.id == file_id:

            if current_user.role == "admin":
                return file

            if file.owner_id == current_user.id:
                return file

            raise HTTPException(status_code=404, detail="File not found")

    raise HTTPException(status_code=404, detail="File not found")


@app.get("/files/{file_id}")
def get_file(file=Depends(check_file_permissions)):
    return {
        "filename": file.filename,
        "size": file.size,
        "owner_id": file.owner_id
    }


@app.delete("/files/{file_id}")
def delete_file(file=Depends(check_file_permissions)):
    global files_db
    files_db = [f for f in files_db if f.id != file.id]
    return {"message": "File deleted"}


@app.get("/files/my")
def my_files(current_user: User = Depends(get_current_user)):
    return [f for f in files_db if f.owner_id == current_user.id]


@app.get("/files/all")
def all_files(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return files_db

