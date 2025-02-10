import os
import pytesseract
import json
from dotenv import load_dotenv
from PIL import Image
from database import BaseDatos
from modelo_generativo import ModeloGPT

# Configurar la ruta de Tesseract (solo si es necesario)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def main():
    # Cargar la imagen de la factura
    archivo = "factura_ejemplo5.webp"
    ruta = f"C:\\Users\\Diego\\PycharmProjects\\FacturIA\\{archivo}" #Poner la ruta adecuada

    imagen = Image.open(ruta)

    # Extraer texto con Tesseract y configuraciones adicionales
    texto_extraido = pytesseract.image_to_string(imagen, lang='spa')

    # Crear un diccionario con los datos
    datos_factura = {
        "texto": texto_extraido.strip()
    }

    # Guardar en un archivo JSON
    with open("factura.json", "w", encoding="utf-8") as archivo_json:
        json.dump(datos_factura, archivo_json, ensure_ascii=False, indent=4)

    #Cargar los datos de api key privada
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    db = BaseDatos()
    modelo = ModeloGPT("GPT-4", "v1.0", openai_api_key,db)

    with open("ejemplo_factura.json", "r", encoding="utf-8") as archivo_json:
        ejemplo_datos = json.load(archivo_json)
    contexto= (  "Estás ayudando a organizar información extraída de una factura, haciendo que sea fácilmente interpretable y procesable en formato JSON."
                 "Por favor, organiza la información extraída de una factura en un formato JSON estructurado."
                 "El JSON debe incluir campos como el emisor, destinatario, productos, cantidades, precios, impuestos y totales o sus equivalentes en cada factura especifica. "
                 "Devuelve el resultado como un objeto JSON bien formado. Asegúrate de que el formato sea correcto y válido."
                 f"Te paso un ejemplo de otra factura para que tomes contexto de como debes aplicar el formato: {json.dumps(ejemplo_datos, ensure_ascii=False, indent=4)}")

    role="Asistente de facturación"
    prompt = datos_factura
    prompt = modelo.agregar_contexto(contexto,prompt)
    modelo.generar_json(prompt, role)




if __name__ == "__main__":
    main()