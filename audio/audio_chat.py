import csv
import pyttsx3
import speech_recognition as sr
import pywhatkit
import requests
import json
import os
import datetime


def start_talk_chatbot(model='llama2', language="en-EN", mic_index=0, voice_id='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enGB_HazelM'):
    url = "http://localhost:11434/api/chat"
    headers = {'Content-Type': "application/json",}
    conversation_history = []
        
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
        
    # Set the selected voice
    engine.setProperty('voice', voice_id)

    # Initialize the voice recognizer
    recognizer = sr.Recognizer()

    def beforeSay(response):
        return response

    def say(response):
        if len(response) == 0:
            return
        engine.say(beforeSay(response))
        engine.runAndWait()

    def generate_response(prompt, chat_history):
        if len(prompt) == 0:
            return "", chat_history
        
        full_prompt = []
        for i in chat_history:
            full_prompt.append({
                "role": "user",
                "content": i[0]
            })
            full_prompt.append({
                "role": "assistant",
                "content": i[1]
            })
        full_prompt.append({
            "role": "user",
            "content": prompt
        })

        data = {
            "model": model,
            "stream": True,
            "messages": full_prompt,
        }

        response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)

        if response.status_code == 200:
            print('AI:', end='')
            all_response = ''
            this_response = ''
            for line in response.iter_lines():
                if line:
                    jsonData = json.loads(line)
                    this_response += jsonData["message"]['content']
                    if '.' in this_response or '?' in this_response or '!' in this_response:
                        print(f'{this_response}', end='')
                        say(this_response)
                        all_response += this_response
                        this_response = ''
            if len(this_response) > 0:
                print(f'{this_response}', end='')
                say(this_response)
                all_response += this_response
                this_response = ''
            chat_history.append((prompt, all_response))

            return "", chat_history
        else:
            return "Error: Unable to fetch response", chat_history

    def save_conversation(conversation_history):
        filename = f"conversation_history.csv"
        with open(os.path.join(os.path.expanduser('~'), 'Downloads', filename), 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Model"])
            for index in range(0, len(conversation_history), 2):
                user = conversation_history[index]
                model = conversation_history[index + 1] if index + 1 < len(conversation_history) else ""
                writer.writerow([user, model])

    while True:
        with sr.Microphone(device_index=mic_index) as source:
            print("Listening...")
            audio = recognizer.listen(source)

            try:
                # Recognize user voice
                user_input = recognizer.recognize_google(audio, language=language)
                print("User: " + user_input)
                
                # Check if the user wants to search in YouTube a video
                detect_youtube_keywords = ['recherche sur youtube', 'find on youtube', 'find in youtube']
                if any(keyword in user_input.lower() for keyword in detect_youtube_keywords):
                    ytb_command = user_input.replace('Open YouTube and find', '')
                    pywhatkit.playonyt(ytb_command)
                    continue
                
                # Check if the user wants to check the time
                detect_time_keywords = ['quelle heure est-il', 'l\'heure actuelle', 'what time is it']
                if any(keyword in user_input.lower() for keyword in detect_time_keywords):
                    engine.say(datetime.datetime.now().strftime('%H:%M:%S'))
                    engine.runAndWait()
                    continue
                
                # Check if the user wants to check the date
                detect_datetime_keywords = ['date actuelle', 'date d\'aujourd\'hui',
                                            'current date', 'today\'s date', 'date of today'
                                            ]
                if any(keyword in user_input.lower() for keyword in detect_datetime_keywords):
                    current_datetime = datetime.datetime.now()
                    formatted_datetime = current_datetime.strftime('%A %d %B %Y - %H:%M')
                    engine.say(formatted_datetime)
                    engine.runAndWait()
                    continue
                
                # Check if the user wants to save the conversation
                detect_save_keyords = ['sauvegarde notre discussion', 'sauvegarde notre conversation', 'sauvegarde la discussion', 'sauvegarde la conversation',
                                        'save our discussion', 'save our conversation', 'save the discussion', 'save the conversation',
                                        ]
                if any(keyword in user_input.lower() for keyword in detect_save_keyords):
                    save_conversation(conversation_history)
                    print("Conversation saved.")
                    continue

                # Check if the user wants to stop the conversation
                detect_stop_keyords = ['stoppe notre discussion', 'stoppe notre conversation', 'stoppe la discussion', 'stoppe la conversation',
                                       'stop our discussion', 'stop our conversation', 'stop the discussion', 'stop the conversation',
                                       ]
                if any(keyword in user_input.lower() for keyword in detect_stop_keyords):
                    engine.say("Okay Bye")
                    engine.runAndWait()
                    print("Stopping the conversation.")
                    break

                # Generate a response
                user_input_str = str(user_input)
                _, chat_history = generate_response(user_input_str, conversation_history)

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == '__main__':
    import tkinter as tk
    from tkinter import ttk, messagebox
    import pyaudio
    root = tk.Tk()
    mic_index = tk.IntVar()
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

        mic_list_dialog = root
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

        def select_mic(index):
            # Selected mic_index
            mic_index.set(index)
            print(f"Selected Microphone Index: {index}")
            mic_list_dialog.destroy()
            start_talk_chatbot(mic_index=mic_index.get())
        
        for idx, mic_name in enumerate(mic_list):
            mic_button = tk.Button(scrollable_frame, text=mic_name, command=lambda idx=idx: select_mic(idx), font=("Inter", 12))
            mic_button.pack()

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    show_mic_list()
    root.mainloop()