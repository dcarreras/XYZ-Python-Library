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