import re

# Ruta del log
log_path = "salida_completa.log"

# Expresión regular para capturar las peticiones GET a api.spotify.com
pattern = re.compile(r'GET (.*?) HTTP/1\.1" (\d+)')

peticiones = []

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        if "api.spotify.com" in line and "GET" in line:
            match = pattern.search(line)
            if match:
                url, status = match.groups()
                peticiones.append((url, status))

print(f"Total peticiones: {len(peticiones)}")
for i, (url, status) in enumerate(peticiones, 1):
    print(f"{i:03d} | Status {status} | {url}")
