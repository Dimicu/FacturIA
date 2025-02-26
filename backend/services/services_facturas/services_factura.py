

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback  #Se instaló para llevar conteo de los tokens de las peticiones
from sqlalchemy.dialects.postgresql import JSONB

from backend.model.modelos import Factura
from backend.supabase_db import SupabaseDB
from fastapi import FastAPI
from dotenv import load_dotenv
from backend.modelo_generativo import ModeloGPT
import json
import os
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
modelo = ModeloGPT("GPT-4", "v1.0", openai_api_key)

app = FastAPI()


def consulta_parseada():
    parser = PydanticOutputParser(pydantic_object=Factura)
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
            Eres un asistente experto en facturación, especializado en la extracción de datos de facturas. 
            Ten en cuenta las siguientes recomendaciones :
            - Identificación del tipo de factura:
                -Rectificativa: si se hace mención a esta palabra y acompaña un numero de otra factura , se considerará rectificativa
                -Simplificada: si se hace mencion a esta palabra , se considera simplificada. En caso de no aparacer la palabra simplificada y no haber datos del receptor se considerará simplificada
                -Completa: cuando existe un emisor y un receptor en la factura
            - Número de factura: puede contener números, letras y caracteres especiales
            - Serie factura : suele formar parte del numero de factura como un año de 2 o 4 digitos, aunque puede ser letras o numeros
            - NIF o CIF : en algunos casos puede aparecer como D.N.I o DNI . En todos los casos puede ser una cadena de numeros y numeros
            - Menciones especiales: solo si alguna referencia a las siguientes esta presente 
                - Operación exenta de IVA (Ejemplo: "exento de IVA" o "artículo 20 LIVA").
                - Facturación por destinatario (mención de "autofacturación").
                - Inversión del sujeto pasivo (Ejemplo: "artículo 84.Uno.2º LIVA").
                - Régimen especial (Ejemplo: agencias de viajes o bienes usados).
            -MUY IMPORTANTE: si algun dato no está presente puedes darle el valor de cadena vacia "", no lo inventes
        """),
        ("human", "Extrae la información de la siguiente factura:\n\n{query}\n\n{format_instructions}"),
    ]).partial(format_instructions=parser.get_format_instructions())

    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

    chain = prompt | llm | parser

    # Usa el callback para obtener métricas de la consulta, tiene que crearse asi con bloque with
    with get_openai_callback() as cb:
        # Ejecuta la cadena con la consulta
        factura_extraida = chain.invoke({"query": extraer_texto()})

        # Guarda las métricas en variables
        total_tokens = cb.total_tokens
        total_cost = cb.total_cost

    generar_coste_consulta_estructurada(llm.model_name, total_tokens, total_cost)
    factura_json = factura_extraida.model_dump_json()
    guardar_datos_factura_json(json.loads(factura_json))
    return factura_extraida

def guardar_datos_factura_json(datos_json):
    db=SupabaseDB()
    db.insertar_factura(datos_json)


def generar_coste_consulta_estructurada(modelo, tokens, tokens_cost):
    db= SupabaseDB()
    db.coste_consulta_estructurada(modelo, tokens,tokens_cost)


async def serv_subir_factura(filedata, file, filename):
    db = SupabaseDB()
    await db.sp_subir_imagen_factura(filedata, file, filename)

def procesar_factura():


    datos_factura = extraer_texto()
    with open ("backend/jsons_plantilla_modelo/instrucciones.txt", "r") as instrucciones:
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
    ruta = "backend/ejemplos_facturas/factura_simplificada1 - copia.jpeg"

    ruta5 = f"ejemplos_facturas/factura_ejemplo5.webp"
    imagen = Image.open(ruta)
    custom_config = r'--psm 3 --oem 1'


    texto_extraido = pytesseract.image_to_string(imagen, config=custom_config , lang="spa")

    print(texto_extraido)

    return texto_extraido


def estructurar_datos():
    ruta_json_ejemplo = "backend/jsons_plantilla_modelo/ejemplo_factura.json"

    with open(ruta_json_ejemplo, "r", encoding="utf-8") as archivo_json:
        ejemplo_datos = json.load(archivo_json)
    return {json.dumps(ejemplo_datos, ensure_ascii=False, indent=4)}

def leer_archivo_txt(ruta_instrucciones = "jsons_plantilla_modelo/instrucciones.txt"):

    # Ejemplo de ruta
    # ruta_instrucciones = "jsons_plantilla_modelo/instrucciones.txt"

    with open(ruta_instrucciones,"r",encoding="utf-8") as archivo:
        instrucciones = archivo.read()
    return instrucciones

