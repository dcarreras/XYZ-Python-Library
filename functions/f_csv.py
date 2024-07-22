# Función para procesar los archivos y guardar en CSV
def process_files():
    folder_path = folder_entry.get()
    if not folder_path:
        result_label.config(text="Por favor seleccione una carpeta")
        return