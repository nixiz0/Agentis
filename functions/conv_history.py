import os
import sys
import subprocess


def conversation_history():
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        download_folder = os.path.expanduser("~") + "/Downloads"
        if os.path.isdir(download_folder):
            if sys.platform.startswith('linux'):
                # For Linux
                subprocess.Popen(['xdg-open', download_folder])  
            elif sys.platform.startswith('darwin'):
                # For MacOS
                subprocess.Popen(['open', download_folder])  
        else:
            print("Download folder not found.")
    elif sys.platform.startswith('win'):
        # For Windows
        subprocess.Popen(['explorer', os.path.join(os.path.expanduser("~"), "Downloads")])  
    else:
        print("Unsupported operating system.")