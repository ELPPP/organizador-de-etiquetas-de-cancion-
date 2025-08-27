import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Autorizacion import BuscarToken as bt
import requests
import base64
import re
import time

cancion= {'Titulo': 'DnB_ - Tristam & Braken -track Frame of Mind _Monstercat Release_.mp3', 'Artista': 'Monstercat Uncaged', 'Album': '', 'Numero de  pista': '', 'Genero': '', 'Año': '', 'Numero de pista': ''}
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
        r"\bRelease\b"
        
    ]

    for word in stopwords:
        titulo_limpio = re.sub(word, "", titulo_limpio)

    # 6. Eliminar espacios extra
    titulo_limpio = re.sub(r"\s+", " ", titulo_limpio).strip()

    # 7. Eliminar extensión de archivo (.mp3, .flac, .wav, etc.)
    titulo_limpio = re.sub(r"\.(mp3|flac|wav|aac|ogg)$", "", titulo_limpio)

    

    return titulo_limpio



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
    data = response.json()

      # diccionario para almacenar los resultados
    encontrado=0
    i=0

    print("arreglo antes de comenzar el while: ",cancion)

    while encontrado == 0:
        t=titulo_limpio
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
            print(Bcancion)
            print("-" * 40)
        print("arreglo formado :)")

        for APICan in busqueda.values():
            print("analizando valor: ", APICan)

            print("comprobando si todo coincide:")
            if (APICan["Titulo"] in titulo_limpio and APICan["Artistas"] in titulo_limpio) or (APICan["Titulo"] in titulo_limpio and APICan["Artistas"] in cancion["Artista"]):
                print("Canción encontrada:",APICan["numero"])
                cancion["Titulo"] = APICan["Titulo"]
                cancion["Artista"] = APICan["Artistas"] 
                cancion["Album"] = APICan["Album"]
                cancion["Año"] = APICan["Año"]
                cancion["Numero de pista"] = APICan["numero"]
                print(cancion)
                encontrado = 1
                break
        
            else:
                print("no coincide, analizando artistas...")
                print( re.sub(r"[^\w\s]", " ", APICan["Artistas"]),"    ",cancion["Titulo"])

                if( re.sub(r"[^\w\s]", " ", APICan["Artistas"]) in cancion["Titulo"]):

                    print("artistas coinciden",APICan["Artistas"],"reemplazando....")
                    cancion["Artista"] = APICan["Artistas"]
                    print("nuevo arreglo: ",cancion)


                    print("limpiando titulo....")
                    cancion["Titulo"]=re.sub( re.sub(r"[^\w\s]", " ", APICan["Artistas"]),"", cancion["Titulo"])

                    print("nuevo titulo: ",cancion["Titulo"])

                print("analizando album...")

                if(APICan["Album"] in titulo_limpio):
                    print("Album coinciden",APICan["Album"]," reemplazando....")
                    cancion["Album"] = APICan["Album"]
                    print("nuevo arreglo: ",cancion)

                    print("limpiando Album....")
                    cancion["Titulo"]=re.sub(APICan["Album"],"", cancion["Titulo"])
                    print("nuevo titulo: ",cancion["Titulo"])

                    print("cambios finalizados, siguiente cancion...")

        print("no hay coincidencias totales, buscando mas canciones...") 

        q_parts=[]
        # Construcción dinámica de la consulta usando mapeo  # siempre incluir título limpio
        for campo, valor in cancion.items():
            if valor and campo in mapeo:  # Si hay valor y está en el mapeo
                if campo == "Artista" and "," in valor:  # Verificar si el campo Artista tiene múltiples valores separados por comas
            # Dividir el valor en una lista de artistas
                    artistas = [artista.strip() for artista in valor.split(",")]
            # Crear una entrada separada para cada artista en la consulta
                    for artista in artistas:
                        q_parts.append(f'{mapeo[campo]}:"{artista}"')
                else:
            # Para otros campos, agregar el valor directamente
                    q_parts.append(f'{mapeo[campo]}:"{valor}"')
        
        
        
        
        #print("arreglo: ",cancion)
        #for campo, valor in cancion.items():
        #    if valor and campo in mapeo:  # si hay valor y está en el mapeo
        #        q_parts.append(f"{mapeo[campo]}:\"{valor}\"")

            q = " ".join(q_parts)

        print("Nueva consulta:", q) 
        params = {
        "q": q,
        "type":"track",
        "limit": 5,  # por ejemplo, cuántos resultados traer
        "offset":i
        }
        
        print("original: ",t,"     nuevo: ",cancion["Titulo"])
        if t!= cancion["Titulo"]:
            print("Titulo cambiado, reiniciando consulta...")
            i=0


        print("iniciando consulta al servidor...")
        while True:
            try:
                print("Realizando solicitud al servidor...")




                response = requests.get(url, headers=headers, params=params, timeout=10)
                response.raise_for_status()  # Verifica si la respuesta es válida (código 200)
                print("Respuesta recibida.")
                break  # Sal del bucle si la respuesta es válida
            except requests.exceptions.Timeout:
                print("El servidor tardó demasiado en responder. Reintentando en 5 segundos...")
                time.sleep(5)  # Espera 5 segundos antes de reintentar
            except requests.exceptions.RequestException as e:
                print(f"Error al realizar la solicitud: {e}")
                break  # Sal del bucle si ocurre otro error#<--aaqui quiero agregar una pausa hasta que el server responda
            
        print("consulta terminada, reiniciando bucle")
        print("#####################################################################################")
        data = response.json()
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(data)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        
    #i=0
    #for track in data["tracks"]["items"]:
    #    i+=1
    #    print("numero de resultado: ",i)
    #    print("Titulo:", track["name"])
    #
    ## Recorrer todos los artistas del track
    #    artistas = [artist["name"] for artist in track["artists"]]
    #    print("Artistas:", ", ".join(artistas))  # imprime separados por coma
    #
    ## Artista principal del álbum
    #    print("Album:", track["album"]["artists"][0]["name"])
    #    print("Año:", track["album"]["release_date"])
    #    print("-" * 40)

  # Imprime la respuesta completa para depuración
    #return response




    

search_song(cancion)