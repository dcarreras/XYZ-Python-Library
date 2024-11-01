import os
from PIL import Image
from tkinter import Tk, Label, Button, Listbox, END, filedialog, messagebox

def resize_images_to_1920x1440(image_paths, listbox):
    resized_images = []
    for image_path in image_paths:
        try:
            with Image.open(image_path) as img:
                # Resize image to 1920x1440
                resized_img = img.resize((1920, 1440))
                # Overwrite the original image
                resized_img.save(image_path)
                resized_images.append(os.path.basename(image_path))
        except Exception as e:
            messagebox.showerror("Error", f"Error processing {image_path}: {e}")
    
    # Update the listbox with the resized images
    for image_name in resized_images:
        listbox.insert(END, image_name)
    return resized_images

def select_images_and_resize():
    # Prompt user to select image files
    file_paths = filedialog.askopenfilenames(
        title="Select images to resize",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    
    if file_paths:
        # Clear the listbox before showing new results
        listbox.delete(0, END)
        # Call the resize function and pass the listbox for results
        resized_images = resize_images_to_1920x1440(file_paths, listbox)
        
        if resized_images:
            messagebox.showinfo("Success", "Images resized and saved successfully.")
        else:
            messagebox.showwarning("No Images Resized", "No images were resized.")
    else:
        messagebox.showwarning("No Selection", "No files selected.")

# Set up the main application window
root = Tk()
root.title("Image Resizer")
root.geometry("400x300")

# Create a label
label = Label(root, text="Resize Images to 1920x1440", font=("Helvetica", 14))
label.pack(pady=10)

# Create a listbox to display resized images
listbox = Listbox(root, width=50, height=10)
listbox.pack(pady=10)

# Create a button to select images
select_button = Button(root, text="Select Images", command=select_images_and_resize)
select_button.pack(pady=10)

# Start the tkinter loop
root.mainloop()
