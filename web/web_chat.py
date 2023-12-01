import csv
import os
import requests
import json 
import gradio as gr
from datetime import datetime


def start_web_ui(model, theme=None):
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': "application/json",}
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

    def download_html():
        html_content = """
        <html>
        <head><title>Conversation History</title></head>
        <body>
            <h2>Conversation History</h2>
            <table style="border-collapse: collapse; width: 100%;">
        """
        for i in range(0, len(conversation_history), 2):
            user = conversation_history[i] if i < len(conversation_history) else ""
            model = conversation_history[i + 1] if i + 1 < len(conversation_history) else ""
            
            html_content += f"""
            <tr>
                <td style="border: 1px solid black; padding: 8px;"><b>User:</b></td>
                <td style="border: 1px solid black; padding: 8px;">{user}</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 8px;"><b>Model:</b></td>
                <td style="border: 1px solid black; padding: 8px;">{model}</td>
            </tr>
            """
        html_content += """
            </table>
        </body>
        </html>
        """
        filename = f"conversation_history_{datetime.now().strftime('%d%m%Y_%H%M%S')}.html"
        with open(os.path.join(os.path.expanduser('~'), 'Downloads', filename), 'w', encoding='utf-8') as file:
            file.write(html_content)

    def download_csv():
        filename = f"chat_history_{datetime.now().strftime('%d%m%Y_%H%M%S')}.csv"
        with open(os.path.join(os.path.expanduser('~'), 'Downloads', filename), 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Model"])
            for index in range(0, len(conversation_history), 2):
                user = conversation_history[index]
                model = conversation_history[index + 1] if index + 1 < len(conversation_history) else ""
                writer.writerow([user, model])
                
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
    
    css = """ 
            .contain {margin-bottom: 3em !important;}
            footer {display: none !important;}
            gradio-app {background-color: #212121 !important;}
            #component-3 {width: 30% !important; margin: 0 auto !important; font-size: 1.25em !important;}
            #component-4 {width: 30% !important; margin: 0 auto !important; font-size: 1.25em !important;}
            #component-5 {width: 30% !important; margin: 0 auto !important; font-size: 1.25em !important;}
            #component-6 {width: 30% !important; margin: 0 auto !important; font-size: 1.25em !important;}
          """
    
    with gr.Blocks(title="Agentis", theme=theme, css=css) as agentis:
        chatbot = gr.Chatbot(label="Agent", height=700)
        msg = gr.Textbox(placeholder="User Prompt", label="Prompt")
        btn_submit = gr.Button(value="Submit", variant='primary')
        btn_submit.click(generate_response, [msg, chatbot], [msg, chatbot])
        clear = gr.ClearButton([msg, chatbot], variant='stop')
        btn_download_html = gr.Button(value="HTML History")
        btn_download_html.click(download_html)
        btn_download_csv = gr.Button(value="CSV History")
        btn_download_csv.click(download_csv)
        
        msg.submit(generate_response, [msg, chatbot], [msg, chatbot])
        
        agentis.launch(favicon_path="web/static/agentis_favicon.ico", inbrowser=True)
        