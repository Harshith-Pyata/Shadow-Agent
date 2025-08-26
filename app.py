from flask import Flask, render_template, request,send_from_directory
from flask import Flask, request, redirect, url_for, send_file, render_template_string,after_this_request
import os
from models.voice_model import voice_to_text
from agent import action
import base64
import io


app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")


@app.route('/')
def index():
    filepath = os.path.join(UPLOAD_FOLDER, 'agentvoice.mp3')  
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
        
        # Delete after preparing response
        # os.remove(OUTPUT_FILE)
        # print("✅ Deleted agent voice after sending.")

        return render_template('upload.html',b64=b64)

    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio_data' not in request.files:
        print("❌ 'audio_data' not in request.files")
        return "No audio file", 400

    audio = request.files['audio_data']
    print("📥 Received file:", audio.filename)


    # Get the full path to the upload folder based on current working directory
    # UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    print("📁 Upload folder:", UPLOAD_FOLDER)

    # Save the uploaded file as recording1.wav in that folder
    filename = os.path.join(UPLOAD_FOLDER, "uservoice.wav")
    audio.save(filename)
    print("✅ File saved to:", filename)


    # print("✅ File saved to:", filename)
    text = voice_to_text("uservoice.wav")
    action(text)

    return redirect(url_for('index'))

@app.route('/delete_audio', methods=['POST'])
def delete_audio():
    filepath = os.path.join(UPLOAD_FOLDER, 'agentvoice.mp3')  
    if os.path.exists(filepath):
        os.remove(filepath)
        print("🗑️ Deleted audio:", filepath)
        return "Deleted", 200
    else:
        print("⚠️ File not found:", filepath)
        return "File not found", 404

@app.route("/check-file")
def check_file():
    FILE_PATH = os.path.join(UPLOAD_FOLDER, "infofile.txt")
    if os.path.exists(FILE_PATH):
        return "true"
    else:
        return "false"


@app.route("/download-file")
def download_file():
    FILE_PATH = os.path.join(UPLOAD_FOLDER, "infofile.txt")
    if not os.path.exists(FILE_PATH):
        return "File not found", 404

    with open(FILE_PATH, "rb") as f:
        file_data = f.read()

    os.remove(FILE_PATH)  # ✅ safe to delete immediately

    return send_file(
        io.BytesIO(file_data),
        as_attachment=True,
        download_name="infofile.txt"
    )

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000, debug=True)
