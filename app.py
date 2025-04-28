from flask import Flask, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

ORIGINAL_BASE_URL = "http://190.94.160.6:8081/hls"

@app.route('/stream.m3u8')
def stream_m3u8():
    url = f"{ORIGINAL_BASE_URL}/hd-live.m3u8"
    r = requests.get(url, stream=True)
    return Response(r.iter_content(chunk_size=1024), content_type=r.headers.get('Content-Type', 'application/vnd.apple.mpegurl'))

@app.route('/<path:filename>')
def stream_ts(filename):
    url = f"{ORIGINAL_BASE_URL}/{filename}"
    r = requests.get(url, stream=True)
    return Response(r.iter_content(chunk_size=1024), content_type=r.headers.get('Content-Type', 'video/MP2T'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)