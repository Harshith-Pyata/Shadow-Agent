import os
from langchain_core.tools import tool
import pyautogui
import time



@tool
def copy(file_path:str):
    """Takes the input as filepath of required file and opens it,It will copy the text from opened file"""
    os.startfile(file_path)
    time.sleep(2)  # give you 2 seconds to switch window
    pyautogui.hotkey("ctrl", "a")
    time.sleep(2)
    pyautogui.hotkey("ctrl", "c")
    time.sleep(2)
    pyautogui.hotkey("ctrl", "w")
    time.sleep(2)




@tool
def save_text():
    """It will open default txt file  and pastes the copied code only if there is a copied text and saves it"""

    
    path = "C:\\Users\\harsh\Desktop\\Python\\Projects\\ShadowAI\\uploads\\infofile.txt"

    # Create file if it does not exist
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("This is a new file.\n")

    os.startfile(path)
    time.sleep(2)
    pyautogui.hotkey("ctrl", "a")
    time.sleep(2)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(2)
    pyautogui.hotkey("ctrl", "s")
    time.sleep(2)
    os.system("taskkill /f /im notepad.exe")

