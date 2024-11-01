import os
from PIL import Image
from tkinter import Tk, Label, Button, Listbox, END, filedialog, messagebox

def resize_image_to_fixed_size(image_path, target_width=180, target_height=135):
    image_info = {}

    try:
        with Image.open(image_path) as img:
            original_width, original_height = img.size
            image_info["original_resolution"] = f"{original_width}x{original_height}"
            original_size_kb = os.path.getsize(image_path) / 1024  # Convert size to KB
            image_info["original_size"] = round(original_size_kb, 2)

            # Resize image to exactly 180x135
            resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Overwrite the original image with the resized one
            resized_img.save(image_path, img.format)

            # Get final size and resolution
            final_size_kb = os.path.getsize(image_path) / 1024  # Convert size to KB
            image_info["last_resolution"] = f"{target_width}x{target_height}"
            image_info["last_size"] = round(final_size_kb, 2)

    except Exception as e:
        messagebox.showerror("Error", f"Error processing {image_path}: {e}")
    
    return image_info

def resize_all_images(image_paths, listbox):
    resized_images = []
    details = ""

    for image_path in image_paths:
        # Resize the image to 180x135 no matter the original size
        image_info = resize_image_to_fixed_size(image_path)
        resized_images.append(os.path.basename(image_path))
        # Format the information for the final dialog box
        details += f"File: {os.path.basename(image_path)}\n"
        details += f"Original Resolution: {image_info['original_resolution']}\n"
        details += f"Original Size: {image_info['original_size']} KB\n"
        details += f"Last Resolution: {image_info['last_resolution']}\n"
        details += f"Last Size: {image_info['last_size']} KB\n"
        details += "-"*40 + "\n"

    # Update the listbox with resized images
    for image_name in resized_images:
        listbox.insert(END, image_name)

    # Show final dialog with the resizing details
    if resized_images:
        messagebox.showinfo("Resizing Details", details)
    else:
        messagebox.showwarning("No Images Resized", "No images were resized.")

def select_images_and_resize():
    # Prompt user to select image files
    file_paths = filedialog.askopenfilenames(
        title="Select images to resize to 180x135",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )

    if file_paths:
        # Clear the listbox before showing new results
        listbox.delete(0, END)
        # Call the resize function and pass the listbox for results
        resize_all_images(file_paths, listbox)
    else:
        messagebox.showwarning("No Selection", "No files selected.")

# Set up the main application window
root = Tk()
root.title("Image Resizer (Resize All to 180x135)")
root.geometry("400x300")

# Create a label
label = Label(root, text="Resize All Images to 180x135", font=("Helvetica", 14))
label.pack(pady=10)

# Create a listbox to display resized images
listbox = Listbox(root, width=50, height=10)
listbox.pack(pady=10)

# Create a button to select images
select_button = Button(root, text="Select Images", command=select_images_and_resize)
select_button.pack(pady=10)

# Start the tkinter loop
root.mainloop()
