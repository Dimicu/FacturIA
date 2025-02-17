import os
import pytesseract
import json
from dotenv import load_dotenv
from PIL import Image
from supabase_db import SupabaseDB


from modelo_generativo import ModeloGPT

# Configurar la ruta de Tesseract (solo si es necesario)
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
)


def extraer_texto():
    # (fotografía o dropping files de la factura)

    # Cargar la imagen de la factura
    ruta5 = f"ejemplos_Facturas/factura_ejemplo5.webp"  # Poner la ruta adecuada

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


def mostrar_mensaje_bienvenida():
    print("Bienvenido a la aplicación de FacturAi.")
    print("Por favor, inicie sesión o regístrese para continuar.")


def login_o_registro():
    db = SupabaseDB()

    while True:
        email = input("Introduce tu correo electrónico: ")
        password = input("Introduce tu contraseña: ")

        if db.login_usuario(email, password):
            print(f"Bienvenido {email} a FacturAi.")
            break
        else:
            print("Usuario no encontrado o datos incorrectos.")

            respuesta = input("¿Quieres registrarte? (s/n): ").lower()
            if respuesta == "s":
                db.registrar_usuario(email, password)

                print("Usuario registrado correctamente")
                break
            else:
                print("No se ha registrado al usuario. Intenta de nuevo.")


def main():

    mostrar_mensaje_bienvenida()
    login_o_registro()

    # Extrare los datos de la imagen
    datos_factura = extraer_texto()

    # Cargar los datos de api key privada
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    # Asegúrate de que db esté instanciada correctamente
    modelo = ModeloGPT("GPT-4", "v1.0", openai_api_key)

    contexto = (
        "Estás ayudando a organizar información extraída de una factura, haciendo que sea fácilmente interpretable y procesable en formato JSON."
        "Recibes los datos desde una imagen escaneada mediante OCR por la libreria tesseract de python "
        "Organiza la información extraída de una factura en un formato JSON estructurado."
        "El JSON debe incluir campos como el emisor, destinatario, productos, cantidades, precios, impuestos y totales o sus equivalentes en cada factura especifica. "
        "Devuelve el resultado como un objeto JSON bien formado. Asegúrate de que el formato sea correcto y válido."
        f"Te paso un ejemplo de otra factura para que tomes contexto de como debes aplicar el formato: {estructurar_datos()}"
    )

    datos_factura_limpios = modelo.limpiar_prompt(datos_factura)
    datos_factura_mas_ordenes = f"Ahora genera SOLO el JSON, no añadas una respuesta de texto introductoria o final {datos_factura_limpios}"
    prompt = modelo.agregar_contexto(contexto, datos_factura_mas_ordenes)
    modelo.generar_json(prompt)


if __name__ == "__main__":
    main()

    # email = "julian@example.com"
    # password = "123456"
    # db.registrar_usuario(email, password)

    # email = "julian@example.com"
    # password = "12346"
    # db.login_usuario(email, password)
