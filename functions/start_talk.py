import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import pyaudio
import pyttsx3
import webbrowser


def callback(url):
    webbrowser.open_new(url)

def get_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    return {voice.name: voice.id for voice in voices}

def start_talk_ai():
    mic_index = tk.IntVar()
    mic_index.set(0)
    voice_id = tk.StringVar()
    voice_id.set('')
    voice_dict = get_voices()
    def on_ok_audio_click():
        selected_model = model_var.get()
        selected_language = language.get()
        if selected_model and selected_language:
            start_web_sep_shell(selected_model, selected_language, mic_index.get(), voice_id.get())
            messagebox.showinfo("Start", f"Starting with the model : {selected_model}, Language : {selected_language}, Micro : {mic_index.get()}, Voice : {voice_id.get()}")
            dialog.destroy()
        elif not selected_model:
            messagebox.showwarning("No model included", "Please put a model before continuing.")
        elif not selected_language:
            messagebox.showwarning("No language included", "Please put a language before continuing.")
        else:
            messagebox.showwarning("No model and language included", "Please put a model and a language before continuing.")

    def start_web_sep_shell(model, language, mic_index, voice_id):
        command = f'python -c "from audio.audio_chat import start_talk_chatbot; start_talk_chatbot(\'{model}\', \'{language}\', {int(mic_index)}, \'{voice_id}\')"'
        subprocess.Popen(command, shell=True)

    def show_mic_list():
        p = pyaudio.PyAudio()
        mic_list = []
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                # Check if the device is available and active
                if device_info['hostApi'] == p.get_default_host_api_info()['index'] and device_info['maxInputChannels'] > 0:
                    mic_list.append(device_info['name'])
        p.terminate()

        mic_list_dialog = tk.Toplevel()
        mic_list_dialog.title("Microphone List")

        # Create a canvas inside the dialog
        canvas = tk.Canvas(mic_list_dialog, width=290, height=200, background='#ffffff')
        scrollbar = ttk.Scrollbar(mic_list_dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Bind the canvas's height to the scrollable frame's height
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for idx, mic_name in enumerate(mic_list):
            mic_button = tk.Button(scrollable_frame, text=mic_name, command=lambda idx=idx: select_mic(idx), font=("Inter", 12))
            mic_button.pack()

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def select_mic(index):
        # Selected mic_index
        mic_index.set(index)
        print(f"Selected Microphone Index: {index}")
        
    def show_voice_list():
        voice_list_dialog = tk.Toplevel()
        voice_list_dialog.title("Voice List")

        # Create a canvas inside the dialog
        canvas = tk.Canvas(voice_list_dialog, width=360, height=360, background='#ffffff')
        scrollbar = ttk.Scrollbar(voice_list_dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Bind the canvas's height to the scrollable frame's height
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for voice_name in voice_dict.keys():
            voice_button = tk.Button(scrollable_frame, text=voice_name, command=lambda voice_name=voice_name: select_voice(voice_name), font=("Inter", 12))
            voice_button.pack()

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def select_voice(voice_name):
        # Selected voice_id
        voice_id.set(voice_dict[voice_name])
        print(f"Selected Voice ID: {voice_dict[voice_name]}")

    dialog = tk.Toplevel()
    dialog.geometry("400x320")
    dialog.minsize(350, 310)
    dialog.maxsize(420, 330)

    dialog.update_idletasks()
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f'+{x}+{y}')
    
    font_style = ("Inter", 15)
    
    dialog.title("Build Audio Agent")

    dialog.option_add("*Font", font_style)

    dialog.configure(background="#384454")
    dialog.tk_setPalette(background="#384454", foreground="white")

    languages = ["fr-FR", "en-EN"]

    model_var = tk.StringVar()
    language = tk.StringVar()

    model_label = ttk.Label(dialog, text="Enter the model name:", foreground="white", background="#384454")
    model_label.pack()
    model_link = tk.Label(dialog, text="List of models", fg="blue", cursor="hand2", foreground="cyan", background="#384454")
    model_link.pack(pady=5)
    model_link.bind("<Button-1>", lambda e: callback("https://ollama.ai/library"))
    
    model_entry = ttk.Entry(dialog, textvariable=model_var)
    model_entry.pack()

    languages_label = ttk.Label(dialog, text="Select Language:", foreground="white", background="#384454")
    languages_label.pack(pady=(15, 1))
    languages_dropdown = ttk.Combobox(dialog, textvariable=language, values=languages, state="readonly")
    languages_dropdown.pack()

    mic_list_button = ttk.Button(dialog, text="Microphone List", command=show_mic_list)
    mic_list_button.pack(pady=5)
    
    voice_list_button = ttk.Button(dialog, text="Voice List", command=show_voice_list)
    voice_list_button.pack(pady=5)

    ok_button = ttk.Button(dialog, text="OK", command=on_ok_audio_click)
    ok_button.pack(pady=5)
    dialog.bind('<Return>', lambda event: on_ok_audio_click())
    dialog.mainloop()