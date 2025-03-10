
import io
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import (
    get_openai_callback,
)  # Se instaló para llevar conteo de los tokens de las peticiones
from sqlalchemy.dialects.postgresql import JSONB


from backend.model.modelos import Factura
from backend.supabase_db import SupabaseDB
from fastapi import FastAPI, UploadFile
from dotenv import load_dotenv
from backend.modelo_generativo import ModeloGPT
import json
import os
from PIL import Image
import pytesseract
import platform


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
)


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
modelo = ModeloGPT("GPT-4", "v1.0", openai_api_key)
db = SupabaseDB()
app = FastAPI()


def srv_interpretar_factura(texto_factura):
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
        factura_extraida = chain.invoke({"query": texto_factura})

        # Guarda las métricas en variables
        total_tokens = cb.total_tokens
        total_cost = cb.total_cost

    serv_coste_guardar_fact_tabla(llm.model_name, total_tokens, total_cost)
    respuesta_JSON_Texto = factura_extraida.model_dump_json()
    respuesta_JSON_estructurado = json.loads(respuesta_JSON_Texto)
    print(respuesta_JSON_estructurado)
    return respuesta_JSON_estructurado

async def serv_guardar_datos_factura_json(datos_json, id):
    """
    Guarda los datos de la factura en json en la base de datos
    :param datos_json:
    :return:
    """

    await db.insertar_factura_db(datos_json, id)
    print("servicesGuardarFacturaDB")


def serv_coste_guardar_fact_tabla(modelo, tokens, tokens_cost):
    """
    Guarda el coste de hacer la peticion a la API en base de datos
    :param modelo:
    :param tokens:
    :param tokens_cost:
    :return:
    """

    db.coste_guardar_fact_tabla(modelo, tokens, tokens_cost)


async def serv_subir_imagen_factura(filedata, file, filename):
    """
    Sube archivo de imagen al storage de supabase
    :param filedata:
    :param file:
    :param filename:
    :return:
    """

    await db.sp_subir_imagen_factura(filedata, file, filename)

def serv_tomar_imagen_storage(nombre_imagen):
    try:
        url_imagen = db.sp_tomar_imagen_storage(nombre_imagen)

        if not url_imagen:
            return None  # Se manejará en el controller con un 404
        return url_imagen

    except Exception as e:
        print(f"Error en serv_tomar_imagen_storage: {str(e)}")
        return None


async def extraer_texto_imagen_subida(content:bytes):

    imagen = Image.open(io.BytesIO(content))
    custom_config = r"--psm 3 --oem 1"

    texto_extraido = pytesseract.image_to_string(imagen, config=custom_config, lang="spa")

    return texto_extraido



def factura_db_services(email):

    response = db.factura_db_supabase(email)
    print("resposefromservices")
    return response
