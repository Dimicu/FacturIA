import json
import os
import requests

class VerificadorJSON:
    @staticmethod
    def Validador(response_formated,max_tokens,modelo):
        from modelo_generativo import ModeloGPT
        modelo2 = ModeloGPT("GPT-4", "v1.0", os.getenv("OPENAI_API_KEY"))

        prompt = f"Verifica linea a linea si existen las claves emisor, cliente, factura, productos, impuestos y total en {response_formated}. En caso de que no estén las claves ¿Cuales faltan?. Ignora mayusculas y minusculas a la hora de comparar las claves."
        messages = [
            {"role": "system", "content": "Actua como experto en facturación"},
            {"role": "user", "content": prompt},
        ]
        payload = {
            "model": modelo,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0
        }
        # Mostrar los datos dela respuesta
        # print(json.dumps(payload, indent=5, ensure_ascii=False))

        response = requests.post(modelo2.url, headers=modelo2.headers, json=payload)

        return response.json()["choices"][0]["message"]["content"].strip()

