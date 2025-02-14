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

    def calcular_coste_peticion(self, prompt_tokens,completion_tokens):
        input_cost = 0.0005 / 1000
        output_cost = 0.0015 / 1000
        total_tokens_cost = round(input_cost + output_cost,6)
        return total_tokens_cost


    def generar_json(self, prompt,modelo="gpt-3.5-turbo", max_tokens=1500):

        carpeta = f"jsons_generados"
       
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
            cost = self.calcular_coste_peticion(input_tokens, output_tokens)

            print(response.json())
            #Crear la ruta de archivo
            ruta_archivo = os.path.join(carpeta, f"{nombre}.json")
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)

             # Guardamos los datos en un archivo JSON
            with open(ruta_archivo, "w", encoding="utf-8") as archivo_json:
                json.dump(message_gpt, archivo_json, ensure_ascii=False, indent=4)
            # Leemos el contenido del archivo
            with open(ruta_archivo, "r" ,encoding="utf-8" ) as factura_json_texto:
                factura_data = factura_json_texto.read()
                # Insertar los datos en Supabase
                db = SupabaseDB()  # Crea una instancia de SupabaseDB
                db.insertar_datos_coste(modelo,input_tokens,output_tokens, total_tokens, cost)
                insert_response = db.insertar_factura({"datos_factura": factura_data})

                if insert_response.data:
                    print("Factura insertada correctamente en la base de datos.")
                else:
                    print("Error al insertar la factura en la base de datos:", insert_response.error)

        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

