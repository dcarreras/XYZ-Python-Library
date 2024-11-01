import os
from PIL import Image
from tkinter import Tk, Label, Button, Listbox, END, filedialog, messagebox

def resize_image_with_aspect_ratio(image_path, target_width, target_height):
    with Image.open(image_path) as img:
        # Obtener las dimensiones originales
        original_width, original_height = img.size
        
        # Mantener la relación de aspecto
        aspect_ratio = original_width / original_height
        
        if aspect_ratio > 1:
            # Imagen apaisada, ajustar el ancho al objetivo
            new_width = target_width
            new_height = int(target_width / aspect_ratio)
        else:
            # Imagen vertical o cuadrada, ajustar la altura al objetivo
            new_height = target_height
            new_width = int(target_height * aspect_ratio)

        # Redimensionar la imagen con alta calidad (antialias)
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        return resized_img

def resize_images(image_paths, listbox, target_width=1920, target_height=1440):
    resized_images = []
    for image_path in image_paths:
        try:
            # Redimensionar manteniendo la relación de aspecto
            resized_img = resize_image_with_aspect_ratio(image_path, target_width, target_height)
            # Sobrescribir la imagen original
            resized_img.save(image_path)
            resized_images.append(os.path.basename(image_path))
        except Exception as e:
            messagebox.showerror("Error", f"Error processing {image_path}: {e}")
    
    # Actualizar el listbox con las imágenes redimensionadas
    for image_name in resized_images:
        listbox.insert(END, image_name)
    return resized_images

def select_images_and_resize():
    # Pedir al usuario que seleccione los archivos de imagen
    file_paths = filedialog.askopenfilenames(
        title="Select images to resize",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    
    if file_paths:
        # Preguntar al usuario si desea continuar
        proceed = messagebox.askyesno("Confirm Resize", "Are you sure you want to resize and overwrite the selected images?")
        
        if proceed:
            # Limpiar la lista antes de mostrar nuevos resultados
            listbox.delete(0, END)
            # Redimensionar las imágenes y actualizar la interfaz
            resized_images = resize_images(file_paths, listbox)
            
            if resized_images:
                messagebox.showinfo("Success", "Images resized and saved successfully.")
            else:
                messagebox.showwarning("No Images Resized", "No images were resized.")
        else:
            messagebox.showinfo("Cancelled", "The operation was cancelled.")
    else:
        messagebox.showwarning("No Selection", "No files selected.")

# Configuración de la ventana principal
root = Tk()
root.title("Image Resizer with Aspect Ratio")
root.geometry("400x300")

# Crear etiqueta
label = Label(root, text="Resize Images (Maintain Aspect Ratio)", font=("Helvetica", 14))
label.pack(pady=10)

# Crear un listbox para mostrar las imágenes procesadas
listbox = Listbox(root, width=50, height=10)
listbox.pack(pady=10)

# Botón para seleccionar las imágenes
select_button = Button(root, text="Select Images", command=select_images_and_resize)
select_button.pack(pady=10)

# Iniciar el loop principal de tkinter
root.mainloop()
