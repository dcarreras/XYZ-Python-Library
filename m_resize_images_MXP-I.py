import os
from PIL import Image
import tkinter as tk
from tkinter import messagebox

# Define the specific folders to be processed, including the root folder
folders = [
    r'C:\Users\DavidCarrerasAlbacet\Documents\Desktop\PLOT\COM_MXP I-I',
    r'C:\Users\DavidCarrerasAlbacet\Documents\Desktop\PLOT\COM_MXP I-I\1',
    r'C:\Users\DavidCarrerasAlbacet\Documents\Desktop\PLOT\COM_MXP I-I\2',
    r'C:\Users\DavidCarrerasAlbacet\Documents\Desktop\PLOT\COM_MXP I-I\3',
    r'C:\Users\DavidCarrerasAlbacet\Documents\Desktop\PLOT\COM_MXP I-I\4'
]

# Define the target file size (25KB)
target_size_kb = 25

# To keep track of changes
changes_made = []

def resize_image(file_path, target_size_kb):
    img = Image.open(file_path)
    img_format = img.format

    # Check the initial file size
    file_size_kb = os.path.getsize(file_path) / 1024
    
    # If the image is smaller than the target size, do not modify it
    if file_size_kb <= target_size_kb:
        print(f'Skipped {file_path} as it is already {file_size_kb:.2f}KB')
        return
    
    # Initial quality setting
    quality = 100
    
    while True:
        # Save the image to a temporary file
        temp_file_path = file_path.replace(f".{img_format.lower()}", f"_temp.{img_format.lower()}")
        img.save(temp_file_path, format=img_format, quality=quality)
        
        # Check the file size
        file_size_kb = os.path.getsize(temp_file_path) / 1024
        
        if file_size_kb <= target_size_kb or quality <= 5:
            break
        
        # Reduce quality for next iteration
        quality -= 5
    
    if file_size_kb > target_size_kb:
        # Resize image while maintaining aspect ratio
        aspect_ratio = img.width / img.height
        new_width = img.width
        new_height = img.height
        
        while file_size_kb > target_size_kb:
            new_width = int(new_width * 0.9)
            new_height = int(new_width / aspect_ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img.save(temp_file_path, format=img_format, quality=quality)
            file_size_kb = os.path.getsize(temp_file_path) / 1024
        
    # Replace original file with resized file
    os.replace(temp_file_path, file_path)
    changes_made.append(f'{os.path.basename(file_path)}: {file_size_kb:.2f}KB with quality={quality}')
    print(f'Resized {file_path} to {file_size_kb:.2f}KB with quality={quality}')

def process_images_in_folders(folders, target_size_kb):
    for folder in folders:
        for file_name in os.listdir(folder):
            if file_name.lower().endswith(('.jpg', '.png')):
                file_path = os.path.join(folder, file_name)
                resize_image(file_path, target_size_kb)
    
    # Show summary of changes made
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    if changes_made:
        summary = "\n".join(changes_made)
        messagebox.showinfo("Summary of Changes", summary)
    else:
        messagebox.showinfo("Summary of Changes", "No images were modified.")

# Process all images in the specified folders
process_images_in_folders(folders, target_size_kb)
