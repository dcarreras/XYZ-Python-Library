# Función para seleccionar una carpeta
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