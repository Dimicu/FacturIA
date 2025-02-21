from typing import Literal
from pydantic import BaseModel, EmailStr, Field
from supabase_db import SupabaseDB
from fastapi import FastAPI
from dotenv import load_dotenv
from modelo_generativo import ModeloGPT
import json
import os
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
)


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
modelo = ModeloGPT("GPT-4", "v1.0", openai_api_key)

app = FastAPI()



def procesar_factura():


    datos_factura = extraer_texto()
    with open ("jsons_plantilla_modelo/instrucciones.txt", "r") as instrucciones:
        contexto2= instrucciones.read()


    contexto = (
        "Estás ayudando a organizar información extraída de una factura, haciendo que sea fácilmente interpretable y procesable en formato JSON. "
        "Recibes los datos desde una imagen escaneada mediante OCR por la libreria tesseract de python. "
        "Organiza la información extraída de una factura en un formato JSON estructurado. "
        "El JSON debe incluir campos como el emisor, destinatario, productos, cantidades, precios, impuestos y totales o sus equivalentes en cada factura específica. "
        f"Te paso un ejemplo de otra factura para que tomes contexto de como debes aplicar el formato: {estructurar_datos()}"
    )

    datos_factura_limpios = modelo.limpiar_prompt(datos_factura)
    datos_factura_mas_ordenes = f"Ahora genera SOLO el JSON, no añadas una respuesta de texto introductoria o final {datos_factura_limpios}"
    prompt = modelo.agregar_contexto(contexto2, datos_factura_mas_ordenes)

    json_generado = modelo.generar_json(prompt)
    return {"resultado": json_generado}


def extraer_texto():
    #ruta = "ejemplos_facturas/factura_ejemplo_diego.jpeg"
    #ruta = "ejemplos_facturas/factura_simplificada1 - copia.jpeg"
    ruta = "ejemplos_facturas/factura_simplificada2 - copia.jpeg"

    ruta5 = f"ejemplos_facturas/factura_ejemplo5.webp"
    imagen = Image.open(ruta)
    custom_config = r'--psm 6 --oem 1'


    texto_extraido = pytesseract.image_to_string(imagen, config=custom_config , lang="spa")

    print(texto_extraido)

    return texto_extraido


def estructurar_datos():
    ruta_json_ejemplo = "jsons_plantilla_modelo/ejemplo_factura.json"

    with open(ruta_json_ejemplo, "r", encoding="utf-8") as archivo_json:
        ejemplo_datos = json.load(archivo_json)
    return {json.dumps(ejemplo_datos, ensure_ascii=False, indent=4)}

def leer_archivo_txt(ruta_instrucciones = "jsons_plantilla_modelo/instrucciones.txt"):

    # Ejemplo de ruta
    # ruta_instrucciones = "jsons_plantilla_modelo/instrucciones.txt"

    with open(ruta_instrucciones,"r",encoding="utf-8") as archivo:
        instrucciones = archivo.read()
    return instrucciones

