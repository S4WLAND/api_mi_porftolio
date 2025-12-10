from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

WS_PROTOCOL = os.getenv("WS_PROTOCOL", "ws")

@app.get("/")
def read_root():
    return {"message": "API funcionando!", "status": "ok"}

@app.get("/test")
def test():
    return HTMLResponse(f"""
    <html>
        <body>
            <h1>Test WebSocket</h1>
            <button onclick="testWS()">Probar WebSocket</button>
            <div id="output"></div>
            <script>
                function testWS() {{
                    const ws = new WebSocket('{WS_PROTOCOL}://' + location.host + '/ws');
                    ws.onopen = () => {{
                        ws.send('Hello!');
                        document.getElementById('output').innerHTML = 'Enviado!';
                    }};
                    ws.onmessage = (e) => {{
                        document.getElementById('output').innerHTML = 'Recibido: ' + e.data;
                    }};
                    ws.onerror = (e) => {{
                        document.getElementById('output').innerHTML = 'ERROR: WebSockets no funcionan';
                    }};
                }}
            </script>
        </body>
    </html>
    """)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    await websocket.send_text(f"Echo: {data}")
    await websocket.close()