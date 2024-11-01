import os
from PIL import Image
from tkinter import Tk, Label, Button, Listbox, END, filedialog, messagebox

def resize_image_maintain_ratio(image, target_width, target_height):
    img_ratio = image.width / image.height
    target_ratio = target_width / target_height

    if img_ratio > target_ratio:
        # Image is wider than the target ratio
        new_width = target_width
        new_height = int(new_width / img_ratio)
    else:
        # Image is taller than the target ratio
        new_height = target_height
        new_width = int(new_height * img_ratio)

    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def resize_image_if_large(image_path):
    min_width = 180
    min_height = 135
    max_file_size = 25 * 1024  # 25KB
    image_info = {}

    # Check if image size is larger than 25KB (25 * 1024 bytes)
    original_size = os.path.getsize(image_path) / 1024  # Convert to KB
    if original_size > 25:
        with Image.open(image_path) as img:
            original_width, original_height = img.size
            image_info["original_resolution"] = f"{original_width}x{original_height}"
            image_info["original_size"] = round(original_size, 2)

            # Resize image maintaining aspect ratio, trying to reduce size under 25KB
            resized_img = resize_image_maintain_ratio(img, img.width // 2, img.height // 2)
            
            # Save resized image to a temporary path and check if the size is under 25KB
            temp_path = image_path + ".temp.jpg"
            resized_img.save(temp_path, img.format)

            # Check if the new size is below 25KB, if not, continue resizing
            while os.path.getsize(temp_path) > max_file_size and resized_img.width > min_width and resized_img.height > min_height:
                resized_img = resize_image_maintain_ratio(resized_img, max(min_width, resized_img.width // 2), max(min_height, resized_img.height // 2))
                resized_img.save(temp_path, img.format)

            # Check if the resolution has not dropped below 180x135
            if resized_img.width < min_width or resized_img.height < min_height:
                messagebox.showwarning("Warning", f"Image {os.path.basename(image_path)} can't be resized below {min_width}x{min_height}. Skipping...")
                os.remove(temp_path)  # Delete the temporary file
            else:
                # Overwrite original image with resized image
                os.replace(temp_path, image_path)
                image_info["last_resolution"] = f"{resized_img.width}x{resized_img.height}"
                image_info["last_size"] = round(os.path.getsize(image_path) / 1024, 2)  # Convert to KB
                return image_info
    else:
        with Image.open(image_path) as img:
            image_info["original_resolution"] = f"{img.width}x{img.height}"
            image_info["original_size"] = round(original_size, 2)
            image_info["last_resolution"] = f"{img.width}x{img.height}"
            image_info["last_size"] = round(original_size, 2)

    return image_info

def resize_images_if_needed(image_paths, listbox):
    resized_images = []
    details = ""
    for image_path in image_paths:
        try:
            # Resize the image if it's larger than 25KB and not smaller than 180x135
            image_info = resize_image_if_large(image_path)
            if image_info:
                resized_images.append(os.path.basename(image_path))
                # Format the information for the dialog box
                details += f"File: {os.path.basename(image_path)}\n"
                details += f"Original Resolution: {image_info['original_resolution']}\n"
                details += f"Original Size: {image_info['original_size']} KB\n"
                details += f"Last Resolution: {image_info['last_resolution']}\n"
                details += f"Last Size: {image_info['last_size']} KB\n"
                details += "-"*40 + "\n"
        except Exception as e:
            messagebox.showerror("Error", f"Error processing {image_path}: {e}")
    
    # Update the listbox with the resized images
    for image_name in resized_images:
        listbox.insert(END, image_name)

    # Show final dialog box with the details of all resized images
    if resized_images:
        messagebox.showinfo("Resizing Details", details)
    else:
        messagebox.showwarning("No Images Resized", "No images were resized because they were all under 25KB or too small.")
    
    return resized_images

def select_images_and_resize():
    # Prompt user to select image files
    file_paths = filedialog.askopenfilenames(
        title="Select images to resize if larger than 25KB",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    
    if file_paths:
        # Clear the listbox before showing new results
        listbox.delete(0, END)
        # Call the resize function and pass the listbox for results
        resize_images_if_needed(file_paths, listbox)
    else:
        messagebox.showwarning("No Selection", "No files selected.")

# Set up the main application window
root = Tk()
root.title("Image Resizer (Reduce if over 25KB with Min Resolution 180x135)")
root.geometry("400x300")

# Create a label
label = Label(root, text="Resize Images if Larger than 25KB", font=("Helvetica", 14))
label.pack(pady=10)

# Create a listbox to display resized images
listbox = Listbox(root, width=50, height=10)
listbox.pack(pady=10)

# Create a button to select images
select_button = Button(root, text="Select Images", command=select_images_and_resize)
select_button.pack(pady=10)

# Start the tkinter loop
root.mainloop()
