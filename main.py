from flask import Flask, render_template, request, redirect, url_for
import assemblyai as aai
import os
from dotenv import load_dotenv
from gevent.pywsgi import WSGIServer

load_dotenv()
app = Flask(__name__)

def transcribe():
    aai.settings.api_key = os.getenv("AAI_API_KEY")
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe("media/audio.wav")
    return transcript.text

@app.route('/transcript')
def transcript():
    content = transcribe()
    return render_template('transcript.html', content=content)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        audio = request.files['audio']
        audio.save("media/audio.wav")
        return redirect(url_for('transcript'))
    return render_template('index.html', title='Home')


http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()