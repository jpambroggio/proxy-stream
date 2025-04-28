from flask import Flask, Response, request
import requests

app = Flask(__name__)

# URL del stream original (CAMBIÁLO si querés otro)
ORIGINAL_URL = "http://190.94.160.6:8081/hls/hd-live.m3u8"

@app.route('/')
def home():
    return "🚀 Servidor Proxy funcionando para el Stream."

@app.route('/stream.m3u8')
def stream_m3u8():
    r = requests.get(ORIGINAL_URL)
    modified_content = r.text

    # Opcional: Podríamos reescribir las rutas si el m3u8 fuera relativo
    return Response(modified_content, content_type='application/vnd.apple.mpegurl', headers={
        'Access-Control-Allow-Origin': '*',
    })

@app.route('/<path:path>')
def proxy_ts(path):
    # Reenviar las peticiones .ts o lo que sea
    upstream_url = ORIGINAL_URL.rsplit('/', 1)[0] + '/' + path
    upstream_response = requests.get(upstream_url, stream=True)

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': upstream_response.headers.get('Content-Type', 'video/MP2T')
    }

    return Response(
        upstream_response.iter_content(chunk_size=1024),
        headers=headers,
        status=upstream_response.status_code
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)