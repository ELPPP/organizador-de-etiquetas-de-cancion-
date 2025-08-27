import openpyxl as op
import os
import methods as cr
#columnas a extraer
ld=[]
q=2
while q > 1:
    qu=input("desea agregar y traducir ptra columna?  ")
    if qu =="si":
        print(qu,"  elegido")
        lt=input("que columna desea agregar y traducir?  ")
        ld.append(lt)
    elif qu=="no":
        q-=2
    else:
        print("¿SI O NO?")
print (ld)
#creacion del nuevo excel
name=input("como quiere llamar el nuevo archivo?  ")
name+=".xlsx"
e= os.path.exists(name)
if e== False:
    cr.creacion(name)
else:
    a=print("el archivo existe uWu")
p=1280
#archvo proveedor
#archivoo=op.load_workbook("Canciones UWUreestructurada.xlsx")
#archivo=archivoo['Sheet']
#p=archivo['A1']
#p=p.value
#extraccion de datos y añadir al nuevo excel
for k in range(1,p):
    for d in ld:
        k=str(k)
        name=d+k
        #c1=archivo[name]
        print(name) 