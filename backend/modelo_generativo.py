import os
import json
import requests
from supabase_db import SupabaseDB


class ModeloGPT:
    def __init__(self, nombre, version, api_key):
        self.nombre= nombre
        self.version = version
        self.api_key = api_key

        self.url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def agregar_contexto(self,prompt,contexto):
        return f"{contexto}\n\n{prompt}"

    def limpiar_prompt(self, prompt):
        prompt = prompt.strip()
        return prompt

    def calcular_coste_peticion(self, prompt_tokens,completion_tokens, modelo):

        OPENAI_PRICING = {
            'gpt-4o': {'input': 0.005 / 1000, 'output': 0.015 / 1000},
            'gpt-4-turbo': {'input': 0.01 / 1000, 'output': 0.03 / 1000},
            'gpt-3.5-turbo': {'input': 0.0005 / 1000, 'output': 0.0015 / 1000}
        }
        if (modelo in OPENAI_PRICING):
            input_costs = prompt_tokens * OPENAI_PRICING[modelo]["input"]
            output_costs = completion_tokens * OPENAI_PRICING[modelo]["output"]


        total_tokens_cost = input_costs + output_costs
        return total_tokens_cost


    def generar_json(self, prompt,modelo="gpt-4-turbo", max_tokens=1500):

        carpeta = f"backend/jsons_generados"
       
        messages = [
            {"role": "system", "content": "Actua como experto en facturación"},
            {"role": "user", "content": prompt},
        ]
        payload = {
            "model": modelo,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        print(requests.post(self.url, headers=self.headers, json=payload))
        if response.status_code == 200:

            data = response.json()
            nombre = data["created"]
            message_gpt = response.json()["choices"][0]["message"]["content"].strip()
            input_tokens = response.json()["usage"]["prompt_tokens"]
            output_tokens = response.json()["usage"]["completion_tokens"]
            total_tokens = response.json()["usage"]["total_tokens"]
            cost = self.calcular_coste_peticion(input_tokens, output_tokens,modelo)

            print(response.json())
            #Crear la ruta de archivo
            ruta_archivo = os.path.join(carpeta, f"{nombre}.json")
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)

             # Guardamos los datos en un archivo JSON
            with open(ruta_archivo, "w", encoding="utf-8") as archivo_json:
                datos = json.loads(message_gpt)
                json.dump(datos, archivo_json, ensure_ascii=False, indent=4)
            # Leemos el contenido del archivo
            with open(ruta_archivo, "r" ,encoding="utf-8" ) as factura_json_texto:
                factura_data = factura_json_texto.read()

                # Insertar los datos en Supabase
                db = SupabaseDB()  # Crea una instancia de SupabaseDB
                """print("Tipo de factura_data:", type(factura_data))
                print("Datos RAW de gpt " + factura_data)"""

                # Convertimos el string JSON a un objeto Python
                try:
                    datos_formateados = json.loads(factura_data)  # Convierte el texto JSON a un diccionario
                    """print("Datos formateados:", datos_formateados)  # Ahora es un diccionario o lista de Python"""
                except json.JSONDecodeError as e:
                    """print("Error al decodificar JSON:", e)"""

                db.insertar_datos_coste(modelo,input_tokens,output_tokens, total_tokens, cost)
                db.insertar_factura(datos_formateados)
                print("Insercion factura correcta")
                print("Insercion datos costes correctos")

        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

