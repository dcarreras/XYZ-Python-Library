import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog

# Global variable to store the selected directory and file path
selected_directory = ""
selected_file_path = ""

def load_excel():
    global selected_file_path
    if selected_file_path:
        try:
            excel_data = pd.read_excel(selected_file_path)
            if 'Final File Name' not in excel_data.columns or 'CX' not in excel_data.columns:
                messagebox.showerror("Error", "Excel file must contain 'Final File Name' and 'CX' columns.")
                return None
            return excel_data
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Excel file: {e}")
            return None
    else:
        messagebox.showerror("Error", "No file selected")
        return None

def preview_and_group_files(excel_data):
    if not selected_directory:
        messagebox.showerror("Error", "No directory selected")
        return

    cx_files = []
    no_cx_files = []
    tbc_files = []
    for _, row in excel_data.iterrows():
        file_path = os.path.join(selected_directory, row['Final File Name'])
        if not os.path.exists(file_path):
            continue

        if row['CX'] == 'Yes':
            cx_files.append(row['Final File Name'])
        elif row['CX'] == 'No':
            no_cx_files.append(row['Final File Name'])
        elif row['CX'] == 'TBC':
            tbc_files.append(row['Final File Name'])

    preview_message = "CX Files:\n" + "\n".join(cx_files) + "\n\nNO-CX Files:\n" + "\n".join(no_cx_files) + "\n\nTBC Files:\n" + "\n".join(tbc_files)
    
    preview_window = tk.Toplevel(root)
    preview_window.title("Preview Grouping")
    tk.Label(preview_window, text=preview_message, justify=tk.LEFT).pack(padx=10, pady=10)
    tk.Button(preview_window, text="Confirm and Move Files", command=lambda: move_files(cx_files, no_cx_files, tbc_files)).pack(pady=10)
    tk.Button(preview_window, text="Close", command=preview_window.destroy).pack(pady=10)

def move_files(cx_files, no_cx_files, tbc_files):
    cx_dir = os.path.join(selected_directory, 'CX')
    no_cx_dir = os.path.join(selected_directory, 'NO-CX')
    tbc_dir = os.path.join(selected_directory, 'TBC')

    os.makedirs(cx_dir, exist_ok=True)
    os.makedirs(no_cx_dir, exist_ok=True)
    os.makedirs(tbc_dir, exist_ok=True)

    for file in cx_files:
        os.rename(os.path.join(selected_directory, file), os.path.join(cx_dir, file))
    for file in no_cx_files:
        os.rename(os.path.join(selected_directory, file), os.path.join(no_cx_dir, file))
    for file in tbc_files:
        os.rename(os.path.join(selected_directory, file), os.path.join(tbc_dir, file))

    messagebox.showinfo("Files Moved", "Files have been grouped and moved successfully.")

def select_directory():
    global selected_directory
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        dir_label.config(text=f"Selected Directory: {selected_directory}")

def select_excel_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if selected_file_path:
        file_label.config(text=f"Selected File: {selected_file_path}")

def on_group_files():
    excel_data = load_excel()
    if excel_data is not None:
        preview_and_group_files(excel_data)

# Create the main window
root = tk.Tk()
root.title("File Grouper")

# Create and place the directory selection button
select_dir_button = tk.Button(root, text="Select Directory", command=select_directory)
select_dir_button.pack(pady=10)

dir_label = tk.Label(root, text="No directory selected", justify=tk.LEFT)
dir_label.pack(pady=5)

# Create and place the file selection button
select_file_button = tk.Button(root, text="Select Excel File", command=select_excel_file)
select_file_button.pack(pady=10)

file_label = tk.Label(root, text="No file selected", justify=tk.LEFT)
file_label.pack(pady=5)

# Create and place the group files button
instructions = tk.Label(root, text="Step 1: Select Directory\nStep 2: Select Excel file\nStep 3: Preview Grouping\nStep 4: Confirm and Move Files", justify=tk.LEFT)
instructions.pack(pady=10)

group_files_button = tk.Button(root, text="Group Files", command=on_group_files)
group_files_button.pack(pady=10)

# Run the application
root.mainloop()
