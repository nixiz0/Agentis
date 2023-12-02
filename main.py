import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import webbrowser

from functions.guide import guide


def installation_guide():
    guide()
    
def start():
    def on_ok_click():
        selected_model = model_var.get()
        selected_theme = theme_var.get()
        if selected_model:
            start_web_sep_shell(selected_model, selected_theme)
            messagebox.showinfo("Start", f"Starting with the model : {selected_model}, Theme : {selected_theme}")
            dialog.destroy()
        else:
            messagebox.showwarning("No model included", "Please put a model before continuing.")

    def start_web_sep_shell(model, theme):
        command = f'python -c "from web.web_chat import start_web_ui; start_web_ui(\'{model}\', \'{theme}\')"'
        subprocess.Popen(command, shell=True)

    dialog = tk.Toplevel()
    dialog.geometry("400x250")
    dialog.minsize(350, 240)
    dialog.maxsize(420, 280)

    dialog.update_idletasks()
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f'+{x}+{y}')
    
    font_style = ("Inter", 16)
    
    dialog.title("Build Web Agent")

    dialog.option_add("*Font", font_style)

    dialog.configure(background="#384454")
    dialog.tk_setPalette(background="#384454", foreground="white")

    themes = ["default", "base", "soft", "mono", "glass"]

    model_var = tk.StringVar()
    theme_var = tk.StringVar()

    model_label = ttk.Label(dialog, text="Enter the model name:", foreground="white", background="#384454")
    model_label.pack()
    model_link = tk.Label(dialog, text="List of models", fg="blue", cursor="hand2", foreground="cyan", background="#384454")
    model_link.pack(pady=1)
    model_link.bind("<Button-1>", lambda e: callback("https://ollama.ai/library"))
    
    model_entry = ttk.Entry(dialog, textvariable=model_var)
    model_entry.pack()

    theme_label = ttk.Label(dialog, text="Select theme:", foreground="white", background="#384454")
    theme_label.pack(pady=(15, 1))
    theme_dropdown = ttk.Combobox(dialog, textvariable=theme_var, values=themes, state="readonly")
    theme_dropdown.pack()

    ok_button = ttk.Button(dialog, text="OK", command=on_ok_click)
    ok_button.pack(pady=15)
    dialog.mainloop()

def callback(url):
    webbrowser.open_new(url)

def conversation_history():
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        download_folder = os.path.expanduser("~") + "/Downloads"
        if os.path.isdir(download_folder):
            if sys.platform.startswith('linux'):
                # Pour Linux
                subprocess.Popen(['xdg-open', download_folder])  
            elif sys.platform.startswith('darwin'):
                # Pour MacOS
                subprocess.Popen(['open', download_folder])  
        else:
            print("Download folder not found.")
    elif sys.platform.startswith('win'):
        # Pour Windows
        subprocess.Popen(['explorer', os.path.join(os.path.expanduser("~"), "Downloads")])  
    else:
        print("Unsupported operating system.")

# Creation of the main window
root = tk.Tk()
root.title("Agentis")
root.configure(bg='#384454')

# Creating a style for the buttons
style = ttk.Style()
style.configure('TButton', font=('Inter', 16), background='gray', foreground='black')

# Creation of the frame for the image
image_frame = tk.Frame(root, bg='#384454')
image_frame.pack(pady=5)
img = tk.PhotoImage(file="ressources/agentis_logo.png")

image_label = tk.Label(image_frame, image=img, bg='#384454')
image_label.image = img 
image_label.pack()

# Creation of buttons
start_button = ttk.Button(root, text="Installation Guide", command=installation_guide, style='TButton')
list_button = ttk.Button(root, text="Start", command=start, style='TButton')
create_button = ttk.Button(root, text="Open History", command=conversation_history, style='TButton')

# Applying styling to buttons
start_button.pack(pady=(20, 5))
list_button.pack(pady=5)
create_button.pack(pady=5)

root.minsize(210, 270)
root.maxsize(260, 300)
root.geometry("250x300")

# Window centering
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
position_down = int(root.winfo_screenheight() / 2 - window_height / 1)
root.geometry("+{}+{}".format(position_right, position_down))

root.mainloop()