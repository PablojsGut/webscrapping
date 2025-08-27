# main.py
from cuentas import generar_datos_ficticios
from scrapping import votar_cupon

# --- Parámetros de generación ---
cantidad_cuentas = 5  # Número de cuentas a generar
local = 6             # Posición de la tarjeta
estrellas = 7         # Cantidad de estrellas a votar
cod = "the1one"       # Código a validar

# Opciones de generación de correos
excluir_dominios = []        # Dominios a excluir
dominio_extra = None          # Dominio adicional
usar_punto = True
usar_numero = True
usar_anio = False

# Generar cuentas
cuentas = generar_datos_ficticios(
    cantidad=cantidad_cuentas,
    excluir=excluir_dominios,
    dominio_extra=dominio_extra,
    usar_punto=usar_punto,
    usar_numero=usar_numero,
    usar_anio=usar_anio
)

# Iterar sobre las cuentas y usar votar_cupon
for i, (mail, psw) in enumerate(cuentas, start=1):
    print(f"\n=== Procesando cuenta {i} ===")
    print(f"Correo: {mail} | Contraseña: {psw}")
    try:
        votar_cupon(mail, psw, local, estrellas, cod)
    except Exception as e:
        print(f"Error con la cuenta {mail}: {e}")
