import os
from PIL import Image

# Definir la ruta de la carpeta
folder_path = r'C:\Users\DavidCarrerasAlbacet\Documents\Desktop\PLOT\MD4'

# Tamaño máximo en bytes (25KB)
max_size = 25 * 1024

# Función para redimensionar la imagen manteniendo la proporción de aspecto
def resize_image(file_path, max_size):
    img = Image.open(file_path)
    original_size = os.path.getsize(file_path)
    
    if original_size <= max_size:
        print(f'La imagen {file_path} ya es menor de 25KB.')
        return
    
    width, height = img.size
    aspect_ratio = width / height
    
    # Calcular el tamaño inicial de redimensionado
    target_width = int(min(250, width))
    target_height = int(target_width / aspect_ratio)
    
    img = img.resize((target_width, target_height), Image.LANCZOS)
    
    # Intentar guardar la imagen con diferentes calidades hasta que sea menor que el tamaño máximo
    quality = 95
    while True:
        img.save(file_path, quality=quality)
        if os.path.getsize(file_path) <= max_size or quality <= 10:
            break
        quality -= 5
    
    print(f'Redimensionada {file_path} a {img.size} píxeles con calidad {quality}.')

# Procesar todas las imágenes en la carpeta
def process_images_in_folder(folder_path, max_size):
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.jpg'):
            file_path = os.path.join(folder_path, file_name)
            resize_image(file_path, max_size)

# Procesar todas las imágenes en la carpeta
process_images_in_folder(folder_path, max_size)
