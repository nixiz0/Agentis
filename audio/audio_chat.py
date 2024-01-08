import csv
import pyttsx3
import speech_recognition as sr
import pywhatkit
import requests
import json
import os
import datetime


def start_talk_chatbot(model, language="en-EN", mic_index=0, voice_id='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enGB_HazelM'):
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': "application/json",}
    conversation_history = []
        
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
        
    # Set the selected voice
    engine.setProperty('voice', voice_id)

    # Initialize the voice recognizer
    recognizer = sr.Recognizer()

    def generate_response(prompt, chat_history):
        conversation_history.append(prompt)
        full_prompt = "\n".join(map(str, conversation_history))

        data = {
            "model": model,
            "stream": False,
            "prompt": full_prompt,
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            response_text = response.text
            data = json.loads(response_text)
            actual_response = data["response"]
            chat_history.append((prompt, actual_response))

            # Read response to user
            engine.say(actual_response)
            engine.runAndWait()

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