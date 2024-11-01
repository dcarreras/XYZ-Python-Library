import os
from PIL import Image
from tkinter import Tk, Label, Button, Listbox, END, filedialog, messagebox

def resize_images_to_2560x1920(image_paths, listbox):
    resized_images = []
    for image_path in image_paths:
        try:
            with Image.open(image_path) as img:
                # Calculate the aspect ratio
                img_ratio = img.width / img.height
                target_ratio = 2560 / 1920
                
                # Determine if resizing should prioritize width or height
                if img_ratio > target_ratio:
                    new_width = 2560
                    new_height = int(new_width / img_ratio)
                else:
                    new_height = 1920
                    new_width = int(new_height * img_ratio)
                
                # Resize image while preserving aspect ratio
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                # Overwrite the original image with correct format
                resized_img.save(image_path, img.format)
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
        resized_images = resize_images_to_2560x1920(file_paths, listbox)
        
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
label = Label(root, text="Resize Images to 2560x1920", font=("Helvetica", 14))
label.pack(pady=10)

# Create a listbox to display resized images
listbox = Listbox(root, width=50, height=10)
listbox.pack(pady=10)

# Create a button to select images
select_button = Button(root, text="Select Images", command=select_images_and_resize)
select_button.pack(pady=10)

# Start the tkinter loop
root.mainloop()
