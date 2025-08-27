import requests
import base64
import time

# ==== CREDENCIALES ====
CLIENT_ID = "0c47184b4fce494ca51d97390a69fe4b"
CLIENT_SECRET = "388eb73a08164a0c93b332224383cd30"
# Variables globales para guardar el token y su vencimiento
access_token = None
expires_at = 0

def obtenerToken():
    token=get_token()
    if not token:
        print("Error al obtener el token de acceso.")
        token = _request_new_token()
    return token

def _request_new_token():
    """Solicita un nuevo token a Spotify."""
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    }
    data = {"grant_type": "client_credentials"}
    
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    token_info = response.json()
    
    # Guardamos token y tiempo de expiración
    global access_token, expires_at
    access_token = token_info["access_token"]
    expires_in = token_info["expires_in"]  # segundos
    expires_at = int(time.time()) + expires_in
    
    return access_token

def get_token():
    """Devuelve el token actual, refrescando si ya caducó."""
    global access_token, expires_at
    if access_token is None or time.time() >= expires_at:
        return _request_new_token()
    return access_token

def pruebarapida():# ==== Prueba rápida ====
    if __name__ == "__main__":
        print("Token:", get_token())

