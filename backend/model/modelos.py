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
    nombre: str = Field("", description="Nombre del emisor de la factura")
    NIF_CIF: str = Field("", description="Número de identificación fiscal del emisor")
    domicilio: str = Field("", description="Dirección del emisor")

class Receptor(BaseModel):
    nombre: str = Field("", description="Nombre del receptor de la factura")
    NIF_CIF: str = Field("", description="Número de identificación fiscal del receptor")
    domicilio: str = Field("", description="Dirección del receptor")

class Item(BaseModel):
    descripcion: str = Field("", description="Descripción del producto o servicio")
    cantidad: int = Field(0, description="Cantidad comprada")
    precio_unitario: float = Field(0.0, description="Precio por unidad")
    tipo_IVA: int = Field(0, description="Tipo de IVA aplicado")
    cuota_IVA: float = Field(0.0, description="Cuota de IVA calculada")

class Factura(BaseModel):
    tipo_factura: Optional[str] = Field("", description="Tipo de factura")
    numero_factura: str = Field("", description="Número de factura")
    serie: Optional[str] = Field("", description="Serie de la factura si aplica")
    fecha_expedicion: Optional[date] = Field(None, description="Fecha en la que se expidió la factura")
    fecha_operacion: Optional[date] = Field(None, description="Fecha en la que se realizó la operación")
    emisor: Emisor = Field(Emisor(), description="Datos del emisor")
    receptor: Optional[Receptor] = Field(Receptor(), description="Datos del receptor si aplica")
    items: List[Item] = Field([], description="Lista de productos o servicios incluidos en la factura")
    totales: dict = Field({}, description="Totales calculados de la factura")
    menciones_especiales: List[str] = Field([], description="Menciones especiales de la factura si aplica")
    factura_rectificada: Optional[str] = Field("", description="Número de la factura rectificada si aplica")

