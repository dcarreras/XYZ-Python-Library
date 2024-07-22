import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def duplicate_file(file_path, prefixes):
    try:
        directory, original_file = os.path.split(file_path)
        base_name, ext = os.path.splitext(original_file)
        
        for prefix in prefixes:
            new_file_name = prefix + base_name[2:] + ext
            new_file_path = os.path.join(directory, new_file_name)
            shutil.copyfile(file_path, new_file_path)
            print(f"File copied: {new_file_path}")
        
        messagebox.showinfo("Success", "Files duplicated successfully!")
    except Exception as e:
        print(f"Error duplicating files: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")
        
def select_file():
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Revit files", "*.rvt"), ("All files", "*.*")]
    )
    if file_path:
        entry_var.set(file_path)
        
def run_duplication():
    file_path = entry_var.get()
    if file_path:
        prefixes = ["CX-YT", "CX-GT", "CX-BT"]
        duplicate_file(file_path, prefixes)
    else:
        messagebox.showwarning("Warning", "Please select a file first.")


# Setup the GUI
root = tk.Tk()
root.title("File Duplicator")
root.geometry("500x200")

entry_var = tk.StringVar()

tk.Label(root, text="Select the file to duplicate:").pack(pady=10)
entry = tk.Entry(root, textvariable=entry_var, width=50)
entry.pack(pady=5)

tk.Button(root, text="Browse", command=select_file).pack(pady=5)
tk.Button(root, text="Duplicate Files", command=run_duplication).pack(pady=20)

root.mainloop()


