from gtts import gTTS
import os

def generate_audio(text, filename="agentvoice.mp3"):
    # Get the full path to the upload folder based on current working directory
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Save the uploaded file  in that folder
    absfilename = os.path.join(UPLOAD_FOLDER, filename)
    tts = gTTS(text)
    tts.save(absfilename)
    return filename
