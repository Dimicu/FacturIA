import json
import requests
import os


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

    def generar_texto(self, prompt, modelo="gpt-3.5-turbo", max_tokens=50):
        pass

    def agregar_contexto(self,contexto,prompt):
        return f"{contexto}\n\n{prompt}"

    def limpiar_prompt(self, prompt):
        prompt = prompt.strip()
        return prompt

class ModeloGPT(ModeloGenerativo):
    def __init__(self, nombre, version, api_key):

        super().__init__(nombre, version)
        self.api_key = api_key
        self.url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def contextualizar(self,modelo="gpt-3.5-turbo",max_tokens=1000):

        prompt_usuario = ""
        prompt_asistente = ""

        with open("factura.txt", "r", encoding="utf-8") as datos_usuario:
            prompt_usuario = datos_usuario.read()
        with open("ejemplo_factura2.json", "r", encoding="utf-8") as datos_asistente:
            prompt_asistente = datos_asistente.read()

        messages = [
            {"role": "system", "content": "Actua como experto en facturación"},
            {"role": "user", "content": f"Estructura los datos que te envío en un json {prompt_usuario}"},
            {"role": "assistant", "content": f"Aqui tienes los datos en un formato json adecuado {prompt_asistente}"},
        ]
        payload = {
            "model": modelo,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        print(response)

#Nose usa demomento , queda de ejemplo
    def generar_texto(self, prompt,modelo="gpt-3.5-turbo", max_tokens=50):
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
        #Mostrar los datos dela respuesta
        print(json.dumps(payload, indent=5,ensure_ascii=False))


        response = requests.post(self.url, headers=self.headers, json=payload)
        if response.status_code == 200:
            texto_generado = response.json()["choices"][0]["message"]["content"].strip()
            self.db.guardar_interaccion(prompt, texto_generado)
            return texto_generado
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

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
        if response.status_code == 200:
            nombre = response.json()["created"]
            
            ruta_archivo = os.path.join(carpeta, f"{nombre}.json")
            if not os.path.exists(carpeta):
             os.makedirs(carpeta)
             print("has creado el json")
             
            with open(ruta_archivo, "w", encoding="utf-8") as archivo_json:
                json.dump(response.json()["choices"][0]["message"]["content"].strip(), archivo_json, ensure_ascii=False, indent=4)

        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

