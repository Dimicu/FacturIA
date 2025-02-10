import json

import requests
from pyexpat.errors import messages

from database import BaseDatos

class ModeloGenerativo:
    def __init__(self, nombre, version):
        self._nombre = nombre
        self._version = version

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, valor):
        self._version = valor

    def cargar_modelo(self):
        # Código para cargar el modelo
        pass

    def generar_texto(self, prompt,role="Asistente de IA", modelo="gpt-3.5-turbo", max_tokens=50):
        pass
    def agregar_contexto(self,contexto,prompt):
        return f"{contexto}\n\n{prompt}"

    def limpiar_prompt(self, prompt):
        prompt = prompt.strip()
        prompt = prompt.capitalize()
        return prompt

    def formatear_prompt(self, plantilla, variables):
        try:
            prompt_formateado = plantilla.format(**variables)
            return prompt_formateado
        except KeyError as e:
            print(f"Error: Falta la variable {e} en el diccionario de variables.")
            return plantilla

class ModeloGPT(ModeloGenerativo):
    def __init__(self, nombre, version, api_key, db: BaseDatos):
        super().__init__(nombre, version)
        self.api_key = api_key
        self.url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.db = db

    def generar_contexto(self, prompt,contexto):
        prompt_con_contexto = self.agregar_contexto(prompt,contexto)
        return prompt_con_contexto

    def generar_texto(self, prompt, role="Eres un asistente de IA que ayuda a generar textos.",modelo="gpt-3.5-turbo", max_tokens=50):
        messages = [
            {"role": "system", "content": role},
            {"role": "user", "content": prompt},
        ]
        payload = {
            "model": modelo,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        import json
        print(json.dumps(payload, indent=5,ensure_ascii=False))


        response = requests.post(self.url, headers=self.headers, json=payload)
        if response.status_code == 200:
            texto_generado = response.json()["choices"][0]["message"]["content"].strip()
            self.db.guardar_interaccion(prompt, texto_generado)
            return texto_generado
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def generar_json(self, prompt, role="Eres un asistente de IA que ayuda a generar textos.",modelo="gpt-3.5-turbo", max_tokens=1500):


        messages = [
            {"role": "system", "content": role},
            {"role": "user", "content": prompt},
        ]
        payload = {
            "model": modelo,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        if response.status_code == 200:
            nombre = response.json()["created"]
            print(response.json())
            with open(f"{nombre}.json", "w", encoding="utf-8") as archivo_json:
                json.dump(response.json()["choices"][0]["message"]["content"].strip(), archivo_json, ensure_ascii=False, indent=4)

        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

