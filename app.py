from flask import Flask, Response, render_template, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

ORIGINAL_M3U8_URL = "http://190.94.160.6:8081/hls/hd-live.m3u8"  # Cambiá esta URL si querés usar otra

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream.m3u8')
def proxy_m3u8():
    try:
        resp = requests.get(ORIGINAL_M3U8_URL, timeout=5)
        resp.raise_for_status()
        content = resp.text
        base_url = ORIGINAL_M3U8_URL.rsplit('/', 1)[0]

        # Reescribir los paths para que apunten al proxy
        lines = content.splitlines()
        modified_lines = []
        for line in lines:
            if line.endswith(".ts"):
                modified_lines.append(f"/{line}")
            else:
                modified_lines.append(line)

        return Response("\n".join(modified_lines), content_type='application/vnd.apple.mpegurl')
    except Exception as e:
        return Response(f"# error fetching m3u8: {e}", content_type='application/vnd.apple.mpegurl')

@app.route('/<path:filename>')
def proxy_ts(filename):
    try:
        ts_url = f"{ORIGINAL_M3U8_URL.rsplit('/', 1)[0]}/{filename}"
        resp = requests.get(ts_url, timeout=5, stream=True)
        resp.raise_for_status()
        return Response(resp.iter_content(chunk_size=4096), content_type='video/mp2t')
    except Exception as e:
        return Response(f"# error fetching ts segment: {e}", content_type='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
    