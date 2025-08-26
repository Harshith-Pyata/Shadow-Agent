import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AZURE_SPEECH_KEY")
ENDPOINT =os.getenv("AZURE_OPENAI_ENDPOINT2")
DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT_NAME2")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION2") 


def voice_to_text(file:str) -> str:

    AUDIO_FILE = f"./uploads/{file}"

    url = f"{ENDPOINT}/openai/deployments/{DEPLOYMENT}/audio/translations?api-version={API_VERSION}"

    headers = {
        "api-key": API_KEY,
    }
    files = {
        "file": ("uploads/recording1.wav", open(AUDIO_FILE, "rb"), "audio/wav"),
        "response_format": (None, "text"),
        "language": (None, "en")  
    }

    response = requests.post(url, headers=headers, files=files)

    if response.ok:
        print("Transcription result:")
        print(response.text.strip())
    else:
        print("Failed:", response.status_code)
        print(response.text)
    
    return response.text.strip()
