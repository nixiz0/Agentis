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
            messagebox.showinfo("Lancement", f"Lancement avec modèle : {selected_model}, Thème : {selected_theme}")
            dialog.destroy()
        else:
            messagebox.showwarning("Aucun modèle sélectionné", "Veuillez sélectionner un modèle avant de continuer.")

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
    
    dialog.title("Sélection de modèle et thème")

    dialog.option_add("*Font", font_style)

    dialog.configure(background="#384454")
    dialog.tk_setPalette(background="#384454", foreground="white")

    themes = ["default", "base", "soft", "mono", "glass"]

    model_var = tk.StringVar()
    theme_var = tk.StringVar()

    model_label = ttk.Label(dialog, text="Entrez le nom du modèle:", foreground="white", background="#384454")
    model_label.pack()
    model_link = tk.Label(dialog, text="Liste des modèles", fg="blue", cursor="hand2", foreground="cyan", background="#384454")
    model_link.pack(pady=1)
    model_link.bind("<Button-1>", lambda e: callback("https://ollama.ai/library"))
    
    model_entry = ttk.Entry(dialog, textvariable=model_var)
    model_entry.pack()

    theme_label = ttk.Label(dialog, text="Sélectionnez le thème:", foreground="white", background="#384454")
    theme_label.pack(pady=(15, 1))
    theme_dropdown = ttk.Combobox(dialog, textvariable=theme_var, values=themes, state="readonly")
    theme_dropdown.pack()

    ok_button = ttk.Button(dialog, text="OK", command=on_ok_click)
    ok_button.pack(pady=15)
    dialog.mainloop()

def callback(url):
    webbrowser.open_new(url)

def create_action():
    print("Action du bouton Create")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Agentis")

# Configuration de l'arrière-plan de la fenêtre
root.configure(bg='#384454')

# Création d'un style pour les boutons
style = ttk.Style()

# Configuration du style pour la police et la taille de la police
style.configure('TButton', font=('Inter', 16), background='gray', foreground='black')

# Création de la frame pour l'image
image_frame = tk.Frame(root, bg='#384454')
image_frame.pack(pady=5)

# Charger l'image
img = tk.PhotoImage(file="ressources/agentis_logo.png")

# Création d'un label pour afficher l'image
image_label = tk.Label(image_frame, image=img, bg='#384454')
image_label.image = img 

# Placement de l'image
image_label.pack()

# Création des boutons
start_button = ttk.Button(root, text="Installation Guide", command=installation_guide, style='TButton')
list_button = ttk.Button(root, text="Start", command=start, style='TButton')
create_button = ttk.Button(root, text="Create", command=create_action, style='TButton')

# Application du style aux boutons
start_button.pack(pady=(20, 5))
list_button.pack(pady=5)
create_button.pack(pady=5)

# Configuration de la géométrie minimale et maximale de la fenêtre
root.minsize(210, 270)
root.maxsize(260, 300)

# Configuration de la géométrie par défaut de la fenêtre
root.geometry("250x300")

# Centrage de la fenêtre
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
position_down = int(root.winfo_screenheight() / 2 - window_height / 1)
root.geometry("+{}+{}".format(position_right, position_down))

# Lancement de la boucle principale
root.mainloop()