from flask import Flask, Response, send_file
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # <-- Esto permite CORS automáticamente

ORIGINAL_STREAM_URL = "http://190.94.160.6:8081/hls/hd-live.m3u8"

@app.route('/stream.m3u8')
def stream_m3u8():
    r = requests.get(ORIGINAL_STREAM_URL, stream=True)
    return Response(r.iter_content(chunk_size=1024), content_type=r.headers['Content-Type'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)