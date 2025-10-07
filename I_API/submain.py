from queue import Queue
import threading
from I_API.BuscaAPI import gestor
import time
def disparador(pedir_db_func,cargar_func):

    C_Entrada=Queue(maxsize=50)
    C_Salida=Queue()
    print("colas Creadas :)")
    for u in range(1):
        t=threading.Thread(target=gestor,name=f"hilo {u}",args=(C_Entrada,C_Salida), daemon=True)
        t.start()
        print("hilo ",u," creado")
    t=threading.Thread(target=Ver_Cola,name="Ver_cola",args=(C_Entrada,C_Salida,pedir_db_func,cargar_func), daemon=True)
    t.start()

def Ver_Cola(C_Entrada,C_Salida,PedirDB,cargar):
    print("verificando colas...")
    while True:
        print("Verificando cola de entrada...")
        if C_Entrada.qsize()<10:
            print("pidiendo a la DB")
            PedirDB(C_Entrada)
        print("Verificando cola de salida...")
        if C_Salida.empty()==False:
            print("cargando")
            cargar(C_Salida)
        time.sleep(1)