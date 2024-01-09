import tkinter as tk
from tkinter import ttk

from functions.guide import installation_guide
from functions.start_chatbot import start_chatbot
from functions.start_talk import start_talk_ai
from functions.conv_history import conversation_history


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
start_chat = ttk.Button(root, text="Start Chatbot", command=start_chatbot, style='TButton')
start_talk = ttk.Button(root, text="Start Talk", command=start_talk_ai, style='TButton')
create_button = ttk.Button(root, text="Open History", command=conversation_history, style='TButton')

# Applying styling to buttons
start_button.pack(pady=(20, 5))
start_chat.pack(pady=5)
start_talk.pack(pady=5)
create_button.pack(pady=5)

root.minsize(210, 300)
root.maxsize(260, 340)
root.geometry("250x330")

# Window centering
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
position_down = int(root.winfo_screenheight() / 2 - window_height / 1)
root.geometry("+{}+{}".format(position_right, position_down))

root.mainloop()