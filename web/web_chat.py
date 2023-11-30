import requests
import json 
import gradio as gr


def start_web_ui(model, theme=None):
    url = "http://localhost:11434/api/generate"
    headers = {
        'Content-Type': "application/json",
    }

    conversation_history = []

    def generate_response(prompt, chat_history):
        conversation_history.append(prompt)
        full_prompt = "\n".join(conversation_history)
        
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
            conversation_history.append(actual_response)
            chat_history.append((prompt, actual_response))
            return "", chat_history
        else:
            return "Error: Unable to fetch response", chat_history

    if theme == "soft":
        theme = gr.themes.Soft() 
    elif theme == "base":
        theme = gr.themes.Base()
    elif theme == "mono":
        theme = gr.themes.Monochrome()
    elif theme == "glass":
        theme = gr.themes.Glass()
    else: 
        theme = None
        
    with gr.Blocks(title="Agentis", theme=theme) as agentis:
        chatbot = gr.Chatbot(label="Agent", height=700)
        msg = gr.Textbox(placeholder="User Prompt", label="Prompt")
        btn_submit = gr.Button(value="Submit", variant='primary')
        btn_submit.click(generate_response, [msg, chatbot], [msg, chatbot])
        clear = gr.ClearButton([msg, chatbot], variant='stop')

        msg.submit(generate_response, [msg, chatbot], [msg, chatbot])
        
        agentis.launch(favicon_path="web/static/agentis_favicon.ico", inbrowser=True)
