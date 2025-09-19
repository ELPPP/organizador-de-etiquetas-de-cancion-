import os
import methods as cr
#from Extraccion import methods as cr
import openpyxl as op
import tinytag as tt
#comprobacion de existencia y creacion del archivo
def iniciador(ruta):
    #verificar si la base existe
    e= os.path.exists("DB.xlsx")
    if e== False:
        nombre="DB.xlsx"
        cr.creacion(nombre)
    else:
        print("La base Existe")

    #inicio del proceso
    h=os.walk(ruta)
    for f in h:
        F=f[2]
        for C in F:
            #creacion del diccionario
            cancion={"Titulo":"","Artista":"","Album":"","Numero de pista":"","Genero":"","Año":""}
            #llenado del titulo
            cancion["Titulo"] = C # type: ignore
            print(C)
            #creacion de la ruta de la cancion
            lnk = os.path.join(ruta, C) 
            print(lnk)
            #carga del link
            try:
                tag = tt.TinyTag.get(lnk)
            except:
                print("error al cargar archivo(omitiendo...)")    
            #extraccion de metadatos
            try:
                print("cancion añadida, leyendo metadatos...")
                dato=tag.artist or ""
                print("Artista: ",dato)
                cancion["Artista"]=dato# type: ignore

                dato=tag.album or ""
                print("Album: ",dato)
                cancion["Album"]=dato# type: ignore

                dato=tag.track or ""
                print("Numero De Pista: ",dato)
                cancion["Numero de pista"]=dato# type: ignore

                dato=tag.genre or ""
                print("Genero: ",dato)
                cancion["Genero"]=dato# type: ignore

                dato=tag.year or ""
                print("Año: ",dato)
                cancion["Año"]=dato# type: ignore
                #evidencia diccionario armado y rellenado    
                print("diccionario: ",cancion) 
            except:# type: ignore
                print("error al leer metadatos....   ->)",TypeError)

            #añadir diccionario a excel
            Archivo=op.load_workbook("DB.xlsx")
            Libro=Archivo['Sheet'] 
            P=Libro['A1']
            p=P.value
            print("variabilizando datos")
            p = str(p)
            e1 = "B" + p
            e2 = "C" + p
            e3 = "D" + p
            e4 = "E" + p
            e5 = "F" + p
            e6 = "G" + p
            p = int(p)
            print("Añadiendo...")

            Libro[e1]=cancion["Titulo"]
            Libro[e2]=cancion["Artista"]
            Libro[e3]=cancion["Album"]
            Libro[e4]=cancion["Numero de pista"]
            Libro[e5]=cancion["Genero"]
            Libro[e6]=cancion["Año"]            
            p=p+1
            Libro['A1']=p
            Archivo.save("DB.xlsx")
            print("Añadido con exito",cancion["Titulo"])
            print("###############################")
    print("Fin de La Creacion")
iniciador("S:\Musica\Musica\salvar\conservar 2")    
    