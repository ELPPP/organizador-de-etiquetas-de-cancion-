#from Main import log_http_response  # insertado para ver errores
#import sys
#import os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Autorizacion import BuscarToken as bt
import requests
import base64
import re
import time
import unicodedata

#''# 
def limpiar_campo(titulo: str) -> str:

    
    # 1. Normalizar a minúsculas
    titulo_limpio = titulo#.lower()
    # 2. Reemplazar guiones bajos con espacios
    titulo_limpio = re.sub(r"[_\uFF3F]+", "  ", titulo_limpio)
    titulo_limpio = re.sub(r"[-\u2013\u2014\u2212]+", " ", titulo_limpio)
    # 3. Reemplazar caracteres especiales
    titulo_limpio = titulo_limpio.replace("&", " ")
    titulo_limpio = titulo_limpio.replace("y", " ")

    # 4. Eliminar contenido entre paréntesis o corchetes
    titulo_limpio = re.sub(r"\(.*?\)|\[.*?\]", "", titulo_limpio)

    # 5. Eliminar palabras irrelevantes
    stopwords = [
        r"\bfeat\b", 
        r"\bft\b", 
        r"\bfeaturing\b",
        r"\brelease\b", 
        r"\bremaster(ed)?\b",
        r"\bextended mix\b", 
        r"\bofficial video\b",
        r"\baudio\b", 
        r"\btrack\b", 
        r"\bOfficial Video\b",
        r"\bEn Vivo\b", 
        r"\bRemix\b", 
        r"\bAcoustic\b", 
        r"\bInstrumental\b"
        r"\bLive\b", 
        r"\bLyric Video\b", 
        r"\bmusic Video\b",
        r"\bSingle\b", 
        r"\bAlbum\b", 
        r"\bEP\b", 
        r"\boffficial-video\b",
        r"\bOfficial-Video\b",
        r"\bMusic-Video\b",
        r"\bLyric-Video\b",
        r"\bdnb\b",
        r"\bDnB\b",
        r"\bRelease\b",
        r"\bcon\b",
        
    ]
        

    for word in stopwords:
        titulo_limpio = re.sub(word, "", titulo_limpio)

    # 6. Eliminar espacios extra
    titulo_limpio = re.sub(r"\s+", " ", titulo_limpio).strip()

    # 7. Eliminar extensión de archivo (.mp3, .flac, .wav, etc.)
    titulo_limpio = re.sub(r"\.(mp3|flac|wav|aac|ogg)$", "", titulo_limpio)

    

    return titulo_limpio


def normalizar_match(s: str) -> str:
    if not s:
        return ""
    # bajar todo a minúsculas
    s = s.lower()
    # quitar comillas simples y dobles
    s = s.replace('"', "").replace("'", "")
    # normalizar a forma NFD (descomponer acentos)
    s = unicodedata.normalize("NFD", s)
    # filtrar los caracteres que son marcas diacríticas (Mn)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s

def search_song(cancion):
#    print("arreglo al comenzar todo: ",cancion)
    #obtener token
    token = bt.obtenerToken()
    #preparar header
    headers = {
    "Authorization": f"Bearer {token}"
    }
    #url base:
    url = "https://api.spotify.com/v1/search"
    #armado
    #traduccion de campos desde lo que definimos a lo que admite spotify
    mapeo = {
    "Titulo": "track",
    "Artista": "artist",
    "Album": "album",
    "Año": "year",
    "Genero": "genre"
    }
    #se añade al arreglo "q" solo con lo que no esta vacio
    # Usamos solo el título limpio
    titulo_limpio = limpiar_campo(cancion["Titulo"])
    cancion["Titulo"] = limpiar_campo(cancion["Titulo"])

    #print(cancion["Titulo"])
    q = f"{cancion['Titulo']}"

    
    params = {
    "q": q,
    "type":"track",
    "limit": 15  # por ejemplo, cuántos resultados traer
    }
    #request arma la url, la envia al servidor y trae la respuesta a la consulta en la variable "response"
    response = requests.get(url, headers=headers, params=params)
    #log_http_response(response, note=f"Primera búsqueda: {cancion['Titulo']}")#insertado para ver errores
    data = response.json()
    I=cancion["ID"]
      # diccionario para almacenar los resultados
    encontrado=0
    i=0
    t=cancion
    #print("arreglo antes de comenzar el while: ",t)
    B=0
    while B<3 and encontrado==0: #intentos de busqueda
        h=cancion["Titulo"]
        H=cancion
        busqueda = {}
        for track in data["tracks"]["items"]:
            i += 1
            Bcancion = {}  # diccionario por cada canción
            Bcancion["numero"] = i
            Bcancion["Titulo"] = track["name"]
            artistas = [artist["name"] for artist in track["artists"]]
            Bcancion["Artistas"] = ",".join(artistas)
            Bcancion["Album"] = track["album"]["artists"][0]["name"]
            Bcancion["Año"] = track["album"]["release_date"]
            
            # guardamos en el diccionario principal usando el numero como clave
            busqueda[i] = Bcancion
            
        
        #print("iterando resultados recibidos")
        for APICan in busqueda.values():
            #encontrado perfecto
            if (APICan["Titulo"] in titulo_limpio and APICan["Artistas"] in titulo_limpio) or (APICan["Titulo"] in titulo_limpio and APICan["Artistas"] in cancion["Artista"]):
                #print("Canción encontrada:",APICan["numero"])
                cancion["Titulo"] = APICan["Titulo"]
                cancion["Artista"] = APICan["Artistas"] 
                cancion["Album"] = APICan["Album"]
                cancion["Año"] = APICan["Año"]
                cancion["Numero de pista"] = APICan["numero"]
                cancion["Estado"]="MATCH_EXACT"
                
                #print(cancion)
                encontrado = 1
                return cancion
                break
        
            else:
                #encontrado pero por difusion
                if (normalizar_match(APICan["Titulo"]) in normalizar_match(titulo_limpio)and normalizar_match(APICan["Artistas"]) in normalizar_match(titulo_limpio)) or (normalizar_match(APICan["Titulo"]) in normalizar_match(titulo_limpio)and normalizar_match(APICan["Artistas"]) in normalizar_match(cancion["Artista"])):
                    #print("Canción encontrada pero difusa:", APICan["numero"])
                    cancion["Titulo"] = APICan["Titulo"]
                    cancion["Artista"] = APICan["Artistas"]
                    cancion["Album"] = APICan["Album"]
                    cancion["Año"] = APICan["Año"]
                    cancion["Numero de pista"] = APICan["numero"]
                    encontrado = 1
                    cancion["Estado"]="MATCH_FUZZY"
                    return cancion
                else:
                    #print("no coincide, analizando...")

                    #verificar campo artistas
                    if( re.sub(r"[^\w\s]", " ", APICan["Artistas"]) in cancion["Titulo"]):
                        cancion["Artista"] = APICan["Artistas"]
                        cancion["Titulo"]=re.sub( re.sub(r"[^\w\s]", " ", APICan["Artistas"]),"", cancion["Titulo"])
                    #verificar campo album
                    if(APICan["Album"] in titulo_limpio):
                        cancion["Album"] = APICan["Album"]
                        cancion["Titulo"]=re.sub(APICan["Album"],"", cancion["Titulo"])

        #print("no hay coincidencias totales, buscando mas canciones...") 
        #print("cancion: ",cancion)
        q_parts=[]
        #separacion de artistas en el parametro "artistas"
        for campo, valor in cancion.items():
            if valor and campo in mapeo: 
                if campo == "Artista" and "," in valor:  
                    artistas = [artista.strip() for artista in valor.split(",")]
                    for artista in artistas:
                        q_parts.append(f'{mapeo[campo]}:"{artista}"')
                else:
                    q_parts.append(f'{mapeo[campo]}:"{valor}"')
            q = " ".join(q_parts)

        #armar nueva consulta
        #print("Nueva consulta:", q) 
        params = {
        "q": q,
        "type":"track",
        "limit": 5,  # por ejemplo, cuántos resultados traer
        "offset":20*i
        }
        #print("original: ",t,)
        #print("nuevo: ",cancion)

        if h!= cancion["Titulo"]:
            #print("Titulo cambiado, reiniciando consulta...")
            i=0
        else:
            if cancion["Artista"]!=None or cancion["Album"]!=None:
                #print("No encontrado pero hubo limpieza")
                cancion["Estado"]="CLEAN_ONLY"
                return cancion
            #print("Titulo sin cambios,finalizando busqueda...")#final de bucle si no hay cambios
            cancion["Estado"]="FAIL_STATIC"
            return cancion

        if B<3:#intentos de busqueda
            #print("iniciando consulta al servidor...")
            while True:
                try:
                    #print("Realizando solicitud al servidor...")
                    response = requests.get(url, headers=headers, params=params, timeout=10)
                    #log_http_response(response, note=f"Reintento búsqueda: {cancion['Titulo']}")#añadido para revisar errores
                    response.raise_for_status()  # Verifica si la respuesta es válida (código 200)
                    #print("Respuesta recibida.")
                    B+=1
                    break  # Sal del bucle si la respuesta es válida
                except requests.exceptions.Timeout:
                    #print("El servidor tardó demasiado en responder. Reintentando en 5 segundos...")
                    time.sleep(5)  # Espera 5 segundos antes de reintentar
                except requests.exceptions.RequestException as e:
                    #print(f"Error al realizar la solicitud: {e}")
                    break  # Sal del bucle si ocurre otro error#<--aaqui quiero agregar una pausa hasta que el server responda
            #print("#####################################################################################")
        else:
            #print("Se alcanzó el número máximo de intentos. Terminando búsqueda.")
            cancion["Estado"]="FAIL_LIMIT"#fail limit
            return cancion
        #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        #print("respuesta del servidor obtenida:")
        data = response.json()
        #print(data)
        #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        #print("consulta terminada, reiniciando bucle")
        
def gestor(cola_in, cola_out):
    while True:
        cancion = cola_in.get()  
        print("cancion extraida: ",cancion)      # bloquea hasta que haya algo
        resultado = search_song(cancion)
        print("cancion procesada: ",resultado)
        cola_out.put(resultado)
        cola_in.task_done()
        print("cola de salida actual:", list(cola_out.queue))

        print()
        print("cancion enviada a la cola de salida")