
import webbrowser
import sys
import argparse
from os.path import join, realpath
from flask import Flask, render_template, jsonify


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('demo.html')


@app.route("/start_asr")
def start():
    return jsonify("speechrecognition start success!")


@app.route("/get_audio")
def get_audio():
    with open('/tmp/transcript.txt', 'r') as f:
        transcript = f.read()
    return jsonify(transcript)


if __name__ == "__main__":
    webbrowser.open_new('http://127.0.0.1:3000/')
    app.run(port=3000)
