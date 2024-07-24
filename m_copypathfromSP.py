import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

def seleccionar_archivos():
    archivos = filedialog.askopenfilenames(title="Seleccionar archivos")
    return root.tk.splitlist(archivos)

def generar_url_sharepoint(ruta_archivo):
    base_url = "https://xyzrealityltd.sharepoint.com/:b:/s/FieldApplications456/"
    nombre_archivo = os.path.basename(ruta_archivo)
    sharepoint_url = f"{base_url}{nombre_archivo}?e=eo2EXw"
    return sharepoint_url

def copiar_al_portapapeles():
    root.clipboard_clear()
    root.clipboard_append(text_area.get("1.0", tk.END))
    messagebox.showinfo("Copiar al portapapeles", "¡Texto copiado al portapapeles!")

def generar_urls():
    rutas_archivos = seleccionar_archivos()
    text_area.delete("1.0", tk.END)  # Limpiar el área de texto antes de agregar nuevas rutas
    for ruta in rutas_archivos:
        url_sharepoint = generar_url_sharepoint(ruta)
        text_area.insert(tk.END, f"{ruta}\n{url_sharepoint}\n\n")

root = tk.Tk()
root.title("Generador de URLs de SharePoint")

# Botón para seleccionar archivos
boton_seleccionar = tk.Button(root, text="Seleccionar Archivos", command=generar_urls)
boton_seleccionar.pack(pady=10)

# Área de texto para mostrar las rutas y URLs
text_area = scrolledtext.ScrolledText(root, width=100, height=20, wrap=tk.WORD)
text_area.pack(pady=10)

# Botón para copiar al portapapeles
boton_copiar = tk.Button(root, text="Copiar al Portapapeles", command=copiar_al_portapapeles)
boton_copiar.pack(pady=10)

root.mainloop()
