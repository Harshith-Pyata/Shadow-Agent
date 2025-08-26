import pyautogui
import pytesseract
import time
from PIL import ImageGrab,Image
import os

from models.llm_model import llm, work
from langchain_core.tools import tool
from models.voice_model import voice_to_text
from models.text_voice import generate_audio
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def normalize(text):
    return text.replace(" ", "").replace("\n", "").strip().lower()

def remove_num(text):
    result = re.sub(r'\d+(\.\d+)?', '', text)
    return result

@tool
def open_whatsapp()->str:
    """It will just open the whatsapp"""

    # Step 1: Open WhatsApp Desktop
    os.system("start whatsapp:")  # Launch WhatsApp
    time.sleep(7)  # Wait for it to fully load

    return "Opened whatsapp"

@tool
def whatsapp_search(name:str) -> str:
    """It will search for the given contact and points the cursor on this chat"""
    # Move mouse to the WhatsApp input box
    pyautogui.click(x=660, y=294) # Replace with real coordinates

    # Now type
    pyautogui.write(name, interval=0.1)
    time.sleep(2)

    pyautogui.click(x=764,y=367)

    time.sleep(3)
    return "opened the required Chat"

@tool
def starts_conversation(text:str)->str:
    """It will chat with the contact opened by whatsapp_search tool and send messages of user input and chats with the opened chat"""

    pyautogui.write(text, interval=0.1)
    pyautogui.press("enter")

    time.sleep(2)

    screenshot1 = ImageGrab.grab(bbox=(1390, 1550, 2775, 1730))  # Customize region
    screenshot1.save("chat1.png")
    img1 = Image.open("chat1.png").convert("L")  # Convert to grayscale
    # screenshot = screenshot1
    # Step 2: Extract text
    text1 = pytesseract.image_to_string(img1)

    text1 = remove_num(text1)

    print("Extracted message1:", text1)


    while True:
        
        time.sleep(10)
        screenshot2 = ImageGrab.grab(bbox=(1390, 1550, 2775, 1730))  # Customize region
        screenshot2.save("chat2.png")
        # Load and preprocess the image
        img2 = Image.open("chat2.png").convert("L")  # Convert to grayscale
        # screenshot = screenshot1
        # Step 2: Extract text
        text2 = pytesseract.image_to_string(img2)
        text2 = remove_num(text2)
        print("Extracted message2:", text2)


        # Split into line sets, strip each line
        lines1 = set(line.strip() for line in text1.splitlines() if line.strip())
        lines2 = set(line.strip() for line in text2.splitlines() if line.strip())

        # New lines = lines in text2 not in text1
        new_lines = lines2 - lines1
        text = "\n".join(new_lines).strip()


        # Only act if new text was actually found
        if text:
            print("Extracted message3:", text)
            generate_audio(text)
            pyautogui.write(work(text), interval=0.1)
            pyautogui.press("enter")
        else:
            print("No new message detected")
            generate_audio("No new message detected.")
            break

        screenshot2 = ImageGrab.grab(bbox=(1390, 1550, 2775, 1730))  # Customize region
        screenshot2.save("chat2.png")
        screenshot1 = screenshot2

    return "chat completed"

# @tool
# def chat(text:str):
#     """chat with the """

@tool
def sending_files(filepath: str)->str:
    """This tool help to send or share the files to the person of opened chat by fetching the path file from search_files tool and sends the file """
    pyautogui.click(1447, 1809)
    time.sleep(2)
    # pyautogui.click(1421, 1561)
    pyautogui.press("tab")
    time.sleep(1)
    pyautogui.press("down")
    time.sleep(1)
    pyautogui.press("down")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(5)
    pyautogui.write(filepath,interval=0.1)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.press("enter")

    return "File sent"
    
@tool
def close_whatsapp():
    """Closes the only whatsapp window not any folder"""
    # Close WhatsApp Desktop (works regardless of how it was opened)
    os.system("taskkill /f /im WhatsApp.exe")