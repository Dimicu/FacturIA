import os
import pytesseract
import json
from dotenv import load_dotenv
from PIL import Image
from database import BaseDatos
from modelo_generativo import ModeloGPT
# Configurar la ruta de Tesseract (solo si es necesario)
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def extraer_texto():
    # (fotografía o dropping files de la factura)

    # Cargar la imagen de la factura

    #ruta3 = f"ejemplos_Facturas/factura_ejemplo3.jpg"  # Poner la ruta adecuada
    #ruta4 = f"ejemplos_Facturas/factura_ejemplo4.jpg"  # Poner la ruta adecuada
    ruta5 = f"ejemplos_Facturas/factura_ejemplo5.webp"  # Poner la ruta adecuada
    #ruta6 = f"ejemplos_Facturas/factura_ejemplo6.jpeg"  # Poner la ruta adecuada
    #ruta6_2 = f"ejemplos_Facturas/factura_ejemplo6_2.jpeg"  # Poner la ruta adecuada
    imagen = Image.open(ruta5)

    # Extraer texto con Tesseract y configuraciones adicionales
    texto_extraido = pytesseract.image_to_string(imagen)
    return texto_extraido



def estructurar_datos():
    # Ejemplo de como organizar datos formato JSON
    ruta_json_ejemplo = "jsons_plantilla_modelo/ejemplo_factura.json"
    # Lectura del archivo para tomar los datos de ejemplo
    with open(ruta_json_ejemplo, "r", encoding="utf-8") as archivo_json:
        ejemplo_datos = json.load(archivo_json)
    return {json.dumps(ejemplo_datos, ensure_ascii=False, indent=4)}

def main():
    #Extrare los datos de la imagen
    datos_factura = extraer_texto()

    # Cargar los datos de api key privada
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    db = BaseDatos()
    modelo = ModeloGPT("GPT-4", "v1.0", openai_api_key, db)

    contexto = (
        "Estás ayudando a organizar información extraída de una factura, haciendo que sea fácilmente interpretable y procesable en formato JSON."
        "Recibes los datos como un dataframe de la libreria tesseract de python "
        "Por favor, organiza la información extraída de una factura en un formato JSON estructurado."
        "El JSON debe incluir campos como el emisor, destinatario, productos, cantidades, precios, impuestos y totales o sus equivalentes en cada factura especifica. "
        "Devuelve el resultado como un objeto JSON bien formado. Asegúrate de que el formato sea correcto y válido."
        f"Te paso un ejemplo de otra factura para que tomes contexto de como debes aplicar el formato: {estructurar_datos()}")


    prompt = modelo.agregar_contexto(contexto, datos_factura)
    modelo.generar_json(prompt)




if __name__ == "__main__":
    main()