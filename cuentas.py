#cuentas.py
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

def generar_datos_ficticios(cantidad=10, excluir=None, dominio_extra=None, usar_punto=True,
                            usar_numero=True, usar_anio=False):
    datos = []
    dominios = dominios_validos.copy()

    if excluir:
        dominios = [d for d in dominios if d not in excluir]

    if dominio_extra:
        dominios.append(dominio_extra.strip())

    if not dominios:
        dominios = ["gmail.com"]

    for _ in range(cantidad):
        nombre = quitar_tildes(fake.first_name().lower())
        apellido = quitar_tildes(fake.last_name().lower())
        separador = "." if usar_punto else ""

        # Generar sufijo (número y/o año) concatenados sin espacios
        partes_sufijo = []
        if usar_numero:
            partes_sufijo.append(str(random.randint(1, 999)))
        if usar_anio:
            partes_sufijo.append(str(random.choice(range(1980, 2024))))
        sufijo = "".join(partes_sufijo)

        correo = f"{nombre}{separador}{apellido}{sufijo}@{random.choice(dominios)}"

        longitud_pwd = random.randint(8, 12)
        caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(caracteres) for _ in range(longitud_pwd))

        datos.append((correo, password))
    return datos
