from flask import Flask, jsonify, render_template, url_for, redirect, request, session
import requests
import os
from apis import run_apis_1
app = Flask(__name__)
db = []
def db_check(code, val):
    if db.__contains__(val):
        x = db.pop(db.index(val))
        db.append(x)
    else:
        if code != 0:
            db.append(val)


@app.route('/')
def index():
    # data = request.get_json()
    # name = data.get('sn')
    # art = data.get('sa')
    # lang = data.get('la')
    # lyric = data.get('ly')
    # ca = data.get('ca')

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
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    
    audio_file = request.files['audio']
    file_path = os.path.join('audio/', audio_file.filename)
    code = 0
    audio_file.save(file_path)
    try:
        
        print(f"Audio file saved at {file_path}")  
        
        code, song_name, song_artist, la, ret_val, coverart = run_apis_1('audio/recording.wav')
        db_check(code, [song_name, song_artist, la, ret_val, coverart])
        if code != 0:
            print("Ending loop based on code from API response") 
            return jsonify({"message": "Upload successful", 
                            "endLoop": True, 
                            "sn":f"{song_name}", 
                            "sa":f"{song_artist}", 
                            "la":f"{la}", 
                            "ly":f"{ret_val}", 
                            "ca":f"{coverart}"}), 200
        else:
            return jsonify({"message": "Upload successful"}), 200
    except Exception as e:
        print(f"Error saving or processing file: {e}")  
        return jsonify({"error": "Internal server error"}), 500