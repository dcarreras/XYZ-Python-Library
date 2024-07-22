import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.ttk import Progressbar
import traceback

def load_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            excel_data = pd.read_excel(file_path)
            if 'Model Name' not in excel_data.columns or 'Final File Name' not in excel_data.columns:
                messagebox.showerror("Error", "Excel file must contain 'Model Name' and 'Final File Name' columns.")
                return None
            rename_map = dict(zip(excel_data['Model Name'], excel_data['Final File Name']))
            return rename_map
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Excel file: {e}")
            return None
    else:
        messagebox.showerror("Error", "No file selected")
        return None

def rename_files(rename_map):
    directory = filedialog.askdirectory()
    if not directory:
        messagebox.showerror("Error", "No directory selected")
        return
    
    renamed_files = []
    skipped_files = []
    total_files = len(rename_map)
    progress_var.set(0)
    progress_step = 100 / total_files if total_files > 0 else 100

    for filename in os.listdir(directory):
        if filename in rename_map:
            try:
                current_file = os.path.join(directory, filename)
                new_file = os.path.join(directory, rename_map[filename])
                os.rename(current_file, new_file)
                renamed_files.append((filename, rename_map[filename]))
            except Exception as e:
                skipped_files.append((filename, str(e)))
            progress_var.set(progress_var.get() + progress_step)
            root.update_idletasks()

    result_message = "Renamed files:\n" + "\n".join([f'{old} -> {new}' for old, new in renamed_files])
    if skipped_files:
        result_message += "\n\nSkipped files:\n" + "\n".join([f'{file}: {error}' for file, error in skipped_files])
    
    messagebox.showinfo("Renaming Completed", result_message)

    # Log the results to a file
    with open(os.path.join(directory, "renaming_log.txt"), "w") as log_file:
        log_file.write(result_message)

def preview_changes(rename_map):
    directory = filedialog.askdirectory()
    if not directory:
        messagebox.showerror("Error", "No directory selected")
        return
    
    preview_message = "Preview of changes:\n"
    for filename in os.listdir(directory):
        if filename in rename_map:
            preview_message += f'{filename} -> {rename_map[filename]}\n'
    
    preview_messagebox = tk.Toplevel(root)
    preview_messagebox.title("Preview Changes")
    tk.Label(preview_messagebox, text=preview_message, justify=tk.LEFT).pack(padx=10, pady=10)
    tk.Button(preview_messagebox, text="Close", command=preview_messagebox.destroy).pack(pady=10)

def on_rename():
    rename_map = load_excel()
    if rename_map:
        preview_changes(rename_map)
        confirm = messagebox.askyesno("Confirm", "Do you want to rename the files as shown in the preview?")
        if confirm:
            rename_files(rename_map)

# Create the main window
root = tk.Tk()
root.title("File Renamer")

# Create and place the rename button
instructions = tk.Label(root, text="Step 1: Load Excel file\nStep 2: Preview Changes\nStep 3: Confirm and Rename", justify=tk.LEFT)
instructions.pack(pady=10)

rename_button = tk.Button(root, text="Rename Files", command=on_rename)
rename_button.pack(pady=10)

# Create a progress bar
progress_var = tk.DoubleVar()
progress_bar = Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, fill=tk.X, padx=10)

# Run the application
root.mainloop()
