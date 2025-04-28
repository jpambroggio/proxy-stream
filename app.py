from flask import Flask, Response, request
import requests

app = Flask(__name__)

# URL ORIGINAL DEL STREAM
ORIGINAL_STREAM_BASE = 'http://190.94.160.6:8081/hls/'  # <- ajustalo si cambia

@app.route('/')
def home():
    return "Servidor Proxy funcionando para el Stream."

@app.route('/stream.m3u8')
def stream_m3u8():
    url = ORIGINAL_STREAM_BASE + 'hd-live.m3u8'
    r = requests.get(url)
    return Response(r.content, content_type='application/vnd.apple.mpegurl')

@app.route('/<path:filename>')
def stream_ts(filename):
    url = ORIGINAL_STREAM_BASE + filename
    r = requests.get(url, stream=True)
    return Response(r.raw, content_type='video/MP2T')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')