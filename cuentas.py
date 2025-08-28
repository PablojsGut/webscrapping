#cuentas.py
import os
import json
import random
import string
from faker import Faker
import unicodedata

fake = Faker('es_ES')

# Lista inicial de dominios válidos
dominios_validos = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]

def quitar_tildes(texto):
    nfkd = unicodedata.normalize('NFKD', texto)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])

def obtener_correos_existentes(local_id=None, local_nombre=None):
    """Lee cuentas.json y retorna un set de correos ya usados para ese local."""
    file_path = os.path.join(os.getcwd(), "cuentas.json")
    if not os.path.exists(file_path):
        return set()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return set()

    correos_existentes = set()
    for entrada in data:
        if local_id is not None and entrada.get("local_id") == local_id:
            for c in entrada.get("cuentas", []):
                correos_existentes.add(c["correo"])
    return correos_existentes

def generar_datos_ficticios(cantidad=10, excluir=None, dominio_extra=None, usar_punto=True,
                            usar_numero=True, usar_anio=False, local_id=None):
    datos = []
    dominios = dominios_validos.copy()

    if excluir:
        dominios = [d for d in dominios if d not in excluir]
    if dominio_extra:
        dominios.append(dominio_extra.strip())
    if not dominios:
        dominios = ["gmail.com"]

    # Obtener correos ya usados para este local
    correos_existentes = obtener_correos_existentes(local_id)

    for _ in range(cantidad):
        while True:
            nombre = quitar_tildes(fake.first_name().lower())
            apellido = quitar_tildes(fake.last_name().lower())
            separador = "." if usar_punto else ""

            partes_sufijo = []
            if usar_numero:
                partes_sufijo.append(str(random.randint(1, 999)))
            if usar_anio:
                partes_sufijo.append(str(random.choice(range(1980, 2024))))
            sufijo = "".join(partes_sufijo)

            correo = f"{nombre}{separador}{apellido}{sufijo}@{random.choice(dominios)}"

            # Verificar espacios y que no esté ya en cuentas.json para ese local
            if " " not in correo and correo not in correos_existentes:
                break  # correo válido y único

        longitud_pwd = random.randint(8, 12)
        caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(caracteres) for _ in range(longitud_pwd))

        datos.append((correo, password))
        correos_existentes.add(correo)  # para evitar duplicados en la misma generación
        
    return datos
