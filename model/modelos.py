from datetime import date
from typing import List, Literal, Optional
from pydantic import BaseModel, EmailStr, Field


class Usuario(BaseModel):
    email: EmailStr = Field(example="Facturia@example.com")
    password: str = Field(min_length=6, example="FacturAi123")
    role: Literal["admin", "reader"]
    id: int

"""Clases para elementos de factura"""

class Emisor(BaseModel):
    nombre: str
    NIF_CIF: str
    domicilio: str

class Receptor(BaseModel):
    nombre: str
    NIF_CIF: str
    domicilio: str

class Item(BaseModel):
    descripcion: str
    cantidad: int
    precio_unitario: float
    tipo_IVA: int
    cuota_IVA: float

class Factura(BaseModel):
    tipo_factura: Literal["completa", "simplificada", "rectificativa"]
    numero_factura: str
    serie: Optional[str] = None
    fecha_expedicion: Optional[date] = None
    fecha_operacion: Optional[date] = None
    emisor: Emisor
    receptor: Optional[Receptor] = None
    items: List[Item]
    totales: dict
    menciones_especiales: List[str] = []
    factura_rectificada: Optional[str] = None

    class Config:
        min_anystr_length = 1
        anystr_strip_whitespace = True
        use_enum_values = True