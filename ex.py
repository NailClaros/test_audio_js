import os
import requests
import base64
key = os.getenv('SHAZ_API_KEY')
akey = os.getenv('alt_key')

def read_audio_file(file_path):
        with open(file_path, 'rb') as audio_file:
            return base64.b64encode(audio_file.read()).decode('utf-8')

url = "https://shazam.p.rapidapi.com/songs/v2/detect"

querystring = {"timezone":"America/Chicago","locale":"en-US"}

payload = read_audio_file('audio/recording.wav')
headers = {
	"x-rapidapi-key": "72f9da2729mshf2a00b78fd97380p1d0ce1jsned1c7263aa9e",
	"x-rapidapi-host": "shazam.p.rapidapi.com",
	"Content-Type": "text/plain"
}

response = requests.post(url, data=payload, headers=headers, params=querystring)

print(response.json())