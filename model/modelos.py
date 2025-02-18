from typing import Literal
from pydantic import BaseModel, EmailStr, Field


class Usuario(BaseModel):
    email: EmailStr = Field(example="Facturia@example.com")
    password: str = Field(min_length=6, example="FacturAi123")
    role: Literal["admin", "reader"]
    id: int
