import json
import os
import requests
import webbrowser
import subprocess


def open_html_file(file_path):
    webbrowser.open(f"file://{os.path.realpath(file_path)}")

def guide():
    html_file_path = "functions/html_guide/guide.html"
    try:
        # Vérifie si WSL est installé
        wsl_install = subprocess.run(["wsl", "-l"], capture_output=True, text=True)
        if wsl_install.returncode != 0:
            # Télécharge et installe WSL si ce n'est pas déjà fait
            subprocess.run(["wsl", "--install"], check=True)
            subprocess.run(["wsl", "sudo", "apt", "update", "&&", "sudo", "apt", "upgrade"], check=True)
            open_html_file(html_file_path)
        else:
            print("WSL est déjà installé.")
            open_html_file(html_file_path)

    except subprocess.CalledProcessError as e:
        print(f"Une erreur s'est produite : {e}")
        
    