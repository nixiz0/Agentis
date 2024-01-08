import pyttsx3
import speech_recognition as sr
import requests
import json
import os


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

    while True:
        with sr.Microphone(device_index=mic_index) as source:
            print("Listening...")
            audio = recognizer.listen(source)

            try:
                # Recognize user voice
                user_input = recognizer.recognize_google(audio, language=language)
                print("User: " + user_input)

                # Check if the user wants to stop the conversation
                detect_stop_keyords = ['stoppe notre discussion', 'stoppe notre conversation', 'stoppe la discussion', 'stoppe la conversation',
                                       'stop our discussion', 'stop our conversation', 'stop the discussion', 'stop the conversation',
                                       ]
                if any(keyword in user_input.lower() for keyword in detect_stop_keyords):
                    engine.say("Bye")
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