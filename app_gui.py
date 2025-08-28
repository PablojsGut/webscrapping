import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json
import csv
import os
from datetime import datetime
from cuentas import generar_datos_ficticios, dominios_validos
from scrapping import votar_cupon

# --- Variables globales ---
cuentas_generadas = []
vars_seleccion = []
locales = []

# --- Leer CSV de locales ---
with open("locales.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    locales = [(row["id"], row["local"]) for row in reader]

# --- Funciones ---
def generar_cuentas():
    global cuentas_generadas, vars_seleccion
    for widget in frame_lista.winfo_children():
        widget.destroy()
    vars_seleccion = []

    try:
        cantidad = int(entry_cantidad.get() or 5)
    except ValueError:
        cantidad = 5

    excluir = [dom for dom, var in vars_dominios.items() if var.get()]
    dominio_extra = entry_extra.get().strip() or None
    usar_punto = var_usar_punto.get()

    valor_sufijo = opcion_sufijo.get()
    usar_numero = valor_sufijo in ("numero", "ambos")
    usar_anio = valor_sufijo in ("anio", "ambos")

    cuentas_generadas = generar_datos_ficticios(
        cantidad=cantidad,
        excluir=excluir,
        dominio_extra=dominio_extra,
        usar_punto=usar_punto,
        usar_numero=usar_numero,
        usar_anio=usar_anio
    )

    tk.Label(frame_lista, text="Sel.", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
    tk.Label(frame_lista, text="Correo", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=10, pady=5)
    tk.Label(frame_lista, text="Contraseña", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=10, pady=5)

    for i, (correo, pwd) in enumerate(cuentas_generadas, start=1):
        var = tk.BooleanVar()
        vars_seleccion.append(var)
        chk = tk.Checkbutton(frame_lista, variable=var)
        chk.grid(row=i, column=0, padx=5, pady=2)
        tk.Label(frame_lista, text=correo).grid(row=i, column=1, sticky="w", padx=10, pady=2)
        tk.Label(frame_lista, text=pwd).grid(row=i, column=2, sticky="w", padx=10, pady=2)

def guardar_y_votar():
    # --- Obtener cuentas seleccionadas ---
    seleccionadas = [
        {"correo": c, "password": p}
        for (c, p), var in zip(cuentas_generadas, vars_seleccion)
        if var.get()
    ]
    if not seleccionadas:
        messagebox.showwarning("Atención", "No hay filas seleccionadas.")
        return

    try:
        # --- Información del local y parámetros ---
        local_text = combo_locales.get()
        local_id, local_nombre = local_text.split(" - ", 1)
        local_id = int(local_id)
        estrellas = int(entry_estrellas.get())
        codigo = entry_codigo.get().strip()

        # --- Archivo JSON ---
        file_path = os.path.join(os.getcwd(), "cuentas.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        if not isinstance(data, list):
            data = []

        # --- Obtener todos los correos existentes para este local_id ---
        correos_existentes = set()
        for entrada in data:
            if entrada.get("local_id") == local_id:
                for cuenta in entrada.get("cuentas", []):
                    correos_existentes.add(cuenta["correo"])

        # --- Filtrar cuentas duplicadas ---
        nuevas_cuentas = [c for c in seleccionadas if c["correo"] not in correos_existentes]

        if not nuevas_cuentas:
            messagebox.showinfo("Aviso", "Todos los correos seleccionados ya existen para este local.")
            return

        # --- Crear entrada nueva ---
        nueva_entrada = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "local_id": local_id,
            "local_nombre": local_nombre,
            "estrellas": estrellas,
            "codigo": codigo,
            "cuentas": nuevas_cuentas
        }

        data.append(nueva_entrada)

        # --- Guardar JSON ---
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        messagebox.showinfo("Éxito", f"Se guardaron {len(nuevas_cuentas)} cuentas en cuentas.json")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")
        return

    # --- Votar con las cuentas guardadas ---
    for cuenta in nuevas_cuentas:
        correo = cuenta["correo"]
        pwd = cuenta["password"]
        try:
            votar_cupon(correo, pwd, local_id, estrellas, codigo)
        except Exception as e:
            messagebox.showerror("Error", f"Error votando con {correo}: {e}")

    messagebox.showinfo("Éxito", f"Se votó con {len(nuevas_cuentas)} cuentas seleccionadas")

# --- Interfaz ---
root = tk.Tk()
root.title("Gestor de cuentas y cupones")
root.geometry("900x700")

frame_controles = tk.Frame(root)
frame_controles.pack(pady=10)

tk.Label(frame_controles, text="Cantidad de cuentas:").grid(row=0, column=0, padx=5)
entry_cantidad = tk.Entry(frame_controles, width=5)
entry_cantidad.grid(row=0, column=1, padx=5)
entry_cantidad.insert(0, "5")

# --- Locales desde CSV ---
tk.Label(frame_controles, text="Local:").grid(row=0, column=2, padx=5)
combo_locales = ttk.Combobox(frame_controles, width=30, state="readonly")
combo_locales["values"] = [f"{id} - {nombre}" for id, nombre in locales]
combo_locales.grid(row=0, column=3, padx=5)
combo_locales.current(0)  # Selecciona el primero por defecto

# --- Estrellas y código ---
tk.Label(frame_controles, text="Estrellas:").grid(row=0, column=4, padx=5)
entry_estrellas = tk.Entry(frame_controles, width=5)
entry_estrellas.grid(row=0, column=5, padx=5)
entry_estrellas.insert(0, "7")

tk.Label(frame_controles, text="Código:").grid(row=0, column=6, padx=5)
entry_codigo = tk.Entry(frame_controles, width=10)
entry_codigo.grid(row=0, column=7, padx=5)
entry_codigo.insert(0, "the1one")

# --- Checkboxes para excluir dominios ---
tk.Label(frame_controles, text="Excluir dominios:").grid(row=1, column=0, padx=5, sticky="nw")
vars_dominios = {}
frame_checks = tk.Frame(frame_controles)
frame_checks.grid(row=1, column=1, padx=5, sticky="w")
for dom in dominios_validos:
    var = tk.BooleanVar(value=False)
    chk = tk.Checkbutton(frame_checks, text=dom, variable=var)
    chk.pack(anchor="w")
    vars_dominios[dom] = var

# --- Dominio extra ---
tk.Label(frame_controles, text="Dominio extra:").grid(row=2, column=0, padx=5, sticky="w")
entry_extra = tk.Entry(frame_controles, width=20)
entry_extra.grid(row=2, column=1, padx=5, sticky="w")
entry_extra.insert(0, "umayor.cl")

# --- Opción de usar punto ---
var_usar_punto = tk.BooleanVar(value=True)
chk_punto = tk.Checkbutton(frame_controles, text="Usar punto entre nombre y apellido", variable=var_usar_punto)
chk_punto.grid(row=3, column=0, columnspan=2, pady=2, sticky="w")

# --- Radio buttons para sufijo ---
tk.Label(frame_controles, text="Sufijo en correo:").grid(row=4, column=0, padx=5, sticky="w")
opcion_sufijo = tk.StringVar(value="numero")

frame_sufijo = tk.Frame(frame_controles)
frame_sufijo.grid(row=4, column=1, padx=5, sticky="w")
tk.Radiobutton(frame_sufijo, text="Ninguno", variable=opcion_sufijo, value="ninguno").pack(anchor="w")
tk.Radiobutton(frame_sufijo, text="Número aleatorio", variable=opcion_sufijo, value="numero").pack(anchor="w")
tk.Radiobutton(frame_sufijo, text="Año aleatorio", variable=opcion_sufijo, value="anio").pack(anchor="w")
tk.Radiobutton(frame_sufijo, text="Número y Año", variable=opcion_sufijo, value="ambos").pack(anchor="w")

# --- Botones ---
btn_generar = tk.Button(frame_controles, text="Generar cuentas", command=generar_cuentas)
btn_generar.grid(row=5, column=0, padx=10, pady=10)

btn_guardar_y_votar = tk.Button(frame_controles, text="Guardar y Votar", command=guardar_y_votar)
btn_guardar_y_votar.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

frame_lista = tk.Frame(root)
frame_lista.pack(pady=20, fill="both", expand=True)

root.mainloop()
