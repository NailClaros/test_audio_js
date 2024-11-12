from flask import Flask, jsonify, render_template, url_for, redirect, request, session
import requests
import os
import glob
from apis import run_apis
app = Flask(__name__)
db = []

def clear_files():
    files = glob.glob('audio_stream/clips/*')
    for f in files:
        os.remove(f)

def db_check(code, val):
    if db.__contains__(val):
        x = db.pop(db.index(val))
        db.append(x)
    else:
        if code != 0:
            db.append(val)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/found')
def found():
    name = request.args.get('sn')
    art = request.args.get('sa')
    lang = request.args.get('la')
    lyric = request.args.get('ly')
    ca = request.args.get('ca')
    return render_template('found.html', name=name, art=art, lang=lang, lyric=lyric, ca=ca)

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    clear_files()

    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    if 'audio' in request.files:
        audio_file = request.files['audio']
        print("Audio file details:")
        print("Filename:", audio_file.filename)
        print("Content type:", audio_file.content_type)
        print("Size (bytes):", len(audio_file.read()))  # Read to get the file size in bytes
        audio_file.seek(0) 

    audio_file = request.files['audio']

    try:
        
        
        code, song_name, song_artist, la, ret_val, coverart = run_apis(audio_file)
        clear_files()
        db_check(code, [song_name, song_artist, la, ret_val, coverart])
        if code != 0:
            clear_files()
            print("Ending loop based on code from API response") 
            return jsonify({'message': 'Upload successful', 
                            'endLoop': True, 
                            'sn':f'{song_name}', 
                            'sa':f'{song_artist}', 
                            'la':f"{la}", 
                            'ly':f'{ret_val}', 
                            'ca':f'{coverart}'}), 200
        else:
            clear_files()
            return jsonify({'message': 'Upload successful', 'endLoop': False}), 200
    except Exception as e:
        clear_files()
        print(f"Error saving or processing file: {e}")  
        return jsonify({"error": "Internal server error"}), 500