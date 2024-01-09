import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import webbrowser


def callback(url):
    webbrowser.open_new(url)

def start_chatbot():
    def on_ok_chat_click():
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

    ok_button = ttk.Button(dialog, text="OK", command=on_ok_chat_click)
    ok_button.pack(pady=15)
    dialog.bind('<Return>', lambda event: on_ok_chat_click())
    dialog.mainloop()