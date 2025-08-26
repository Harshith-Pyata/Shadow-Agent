import os
from langchain_core.tools import tool
import pyautogui
import time

@tool
def search_files(file: str) -> str:
    """This tool helps to find the user required file or folder and send the file path to the user"""
    matches = []
    search_root = r"C:\Users\harsh\Desktop"

    for root, dirs, files in os.walk(search_root):
        for f in files:
            if file.lower() in f.lower():
                matches.append(os.path.join(root, f))

        # Search in folders
        for d in dirs:
            if file.lower() in d.lower():
                matches.append(os.path.join(root, d))
    
    if not matches:
        return "No matching files found."

    matches = [file.replace("/","\\") for file in matches]

    
    return "\n".join(matches[:1])  # limit results

@tool
def open_folder(filepath: str):
    """Open folder with system call"""
    os.system(f'explorer "{filepath}"')

@tool
def close_folder(filepath:str):
    """It will close the required folder based on the given folder path"""
    time.sleep(2)
    pyautogui.hotkey("alt","f4")


@tool
def create_folder(name:str):
    """This will create the folder on the desktop and gives the user defined name"""

    time.sleep(2)
    pyautogui.hotkey("win","d")
    time.sleep(2)
    pyautogui.moveTo(2031, 447)

    pyautogui.click(button="right")
    time.sleep(2)

    pyautogui.hotkey("shift","F10")
    time.sleep(2)

    pyautogui.hotkey("w","1")
    time.sleep(1)

    pyautogui.press("f")

    pyautogui.write(name,interval=0.1)
    pyautogui.press("enter")

    return "Folder created"