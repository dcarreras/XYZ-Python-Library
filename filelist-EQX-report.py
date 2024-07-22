import os
import csv
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import subprocess

# Función para seleccionar la carpeta
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)

# Función para obtener todos los archivos en el directorio y subdirectorios
def get_all_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append((file, os.path.basename(root)))
    return file_list

# Función para procesar los archivos y guardar en CSV
def process_files():
    folder_path = folder_entry.get()
    if not folder_path:
        result_label.config(text="Por favor seleccione una carpeta")
        return
    
    try:
        files = get_all_files(folder_path)
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_path = os.path.join(folder_path, f'file_names_{now}.csv')
        with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['File Name', 'Folder Name'])
            for file_name, folder_name in files:
                writer.writerow([file_name, folder_name])
        result_label.config(text=f"Archivo CSV guardado en: {csv_path}")
        # Abrir el archivo CSV
        subprocess.Popen(['notepad.exe', csv_path])
    except Exception as e:
        result_label.config(text=f"Error: {e}")

# Configuración de la interfaz tkinter
root = tk.Tk()
root.title("Procesador de Archivos a CSV")

# Elementos de la interfaz
tk.Label(root, text="Seleccione la carpeta:").pack(pady=5)
folder_entry = tk.Entry(root, width=50)
folder_entry.pack(pady=5)
tk.Button(root, text="Buscar", command=select_folder).pack(pady=5)
tk.Button(root, text="Procesar", command=process_files).pack(pady=10)
result_label = tk.Label(root, text="")
result_label.pack(pady=20)

# Ejecutar la interfaz
root.mainloop()
