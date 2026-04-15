from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
import re

class UserCreate(BaseModel):
    username: str = Field(
        min_length=4,
        max_length=20,
        pattern=r"^[a-zA-Z0-9]+$"
    )
    email: EmailStr
    password: str
    confirm_password: str
    age: int = Field(ge=18, le=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if value == "123":
            raise ValueError("Password is too weak")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")

        if not re.search(r"[!@#$%^&*]", value):
            raise ValueError("Password must contain at least one special character")

        return value

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
