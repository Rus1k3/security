from fastapi import FastAPI
from src.schemas import UserCreate

app = FastAPI()

@app.post("/registration")
def register_user(user: UserCreate):
    return {
        "msg": "User created",
        "user": user.username
    }