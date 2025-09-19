
import os
import openpyxl as ox

def creacion(nombre):
    archivo=ox.Workbook()
    archivo.save(nombre)
    archivoo=ox.load_workbook(nombre)
    Libro=archivoo['Sheet']
    Libro['B1']="Titulo"
    Libro['C1']="Artista"
    Libro['D1']="Album"
    Libro['E1']="Numero De Pista"
    Libro['F1']="Genero"
    Libro['G1']="Año"
    Libro['A1']=2
    archivoo.save(nombre)
    print("Archivo ",nombre," creado UWU")

def conversion_asky(palabra):
    cadascii=""
    infrm=[]
    print(palabra,"<--- palabra")
    try:
        for s in palabra:
            codigo_ascii = ord(s)
            if s==" " or s=="-" or s=="_":
                cadascii+=" "
            else:
                codigo_ascii=str(codigo_ascii)
                cadascii+=codigo_ascii
                inf=codigo_ascii+"-"+s
                infrm.append(inf)
    except:
        print("no se paso ningun parametro")
        return("N/E")
    print("El Codigo Ascii de la palabra es: ",infrm)
    print(cadascii)
    return cadascii

def traductor(nn):
    import string
    #nn=int(nn)
    abc=string.ascii_lowercase
    abd=[]
    mnn=[]
    #fase de conversion a sist 27
    while nn>0:
        if nn>27:
            rrnn=nn%27
            mnn.append(rrnn)
            #print("añadido ", rrnn)
            nn=nn/27
            #print("dividido ",nn)
            nn=int(nn)
            #print("reinicio ",nn,"H")
        else:
            #print("insertando ultimo")
            mnn.append(nn)
            nn=nn-nn
            #print("reinicio ",nn,"j")
    #print("terminado")
    #print(mnn)
#fase de conversion a letras
    j=""
    for n in reversed(mnn):
        n-=1
       # print(abc[3])
       # print("buscando letra ",n)

        j=j+abc[n]
        #print("concatenado ",j)
    return(j)

    
    #print(abc)
    #q=nn
    #k=1
    #l=0
    #print(type(nn)," ",type(l))
    #while l<q:
    #    l=26**k
    #    print("tengo ",q,"  ","exponente ",l," ",k)
    #    k+=1
    #k-=1
    #while k>0:
    #    print("exponente ",k)
    #    k-=1
    #    l=26**k
    #    y=0
    #    while q>0:
    #        print("restare:",l, " a ",q)
    #        q-=l #resta la base con el numero
    #        if q<l:  
    #           abd.append(y)
    #           
    #           print("rompi :) ",abd)
    #           break
    #        y+=1#contador de ciclos
    #    abd.append(l)
    #print(" ",q,"cantidad de cargas",y)          
    #print(abd,"matriz")
    #resultado=""
    #for f in abd:
    #    resultado+=abc[f]
    #return(resultado)