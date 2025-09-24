# --- FULL LOGGING SETUP: captures prints, logging, exceptions (main+threads), warnings, urllib3) ---
import sys
import logging
import traceback
import threading
import warnings

# Logger básico: archivo + consola (stdout)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("salida_completa.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Redirige stdout -> logger (para capturar print())
class StreamToLogger:
    def __init__(self, logger, level=logging.INFO):
        self.logger = logger
        self.level = level
    def write(self, message):
        if message and message.strip():
            for line in message.rstrip().splitlines():
                # use logger.log to preserve level
                self.logger.log(self.level, line)
    def flush(self):
        pass

sys.stdout = StreamToLogger(logging.getLogger("STDOUT"), logging.INFO)
# IMPORTANT: do NOT redirect sys.stderr to logger (would cause recursion).

# Capture warnings module into logging
logging.captureWarnings(True)
warnings.simplefilter("default")  # show warnings

# Unhandled exceptions in main thread -> log full traceback
def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logging.getLogger("EXCEPTIONS").error("Uncaught exception:\n%s", tb)

sys.excepthook = excepthook

# Unhandled exceptions in threads (Python 3.8+)
def thread_excepthook(args):
    # args: threading.ExceptHookArgs(thread, exc_type, exc_value, exc_traceback)
    tb = "".join(traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback))
    logging.getLogger("THREAD_EXCEPTIONS").error("Uncaught thread exception in %s:\n%s", args.thread.name, tb)

# safety: if running Python version that has threading.excepthook
if hasattr(threading, "excepthook"):
    threading.excepthook = thread_excepthook

# Optional: increase verbosity of HTTP libs to see request/response detail
# WARNING: this is noisy; enable if you want to debug 429 and headers.
logging.getLogger("urllib3").setLevel(logging.DEBUG)
logging.getLogger("requests").setLevel(logging.DEBUG)

# Short helper to log response details when you catch a non-200:
def log_http_response(resp, note="HTTP Response"):
    try:
        headers = dict(resp.headers)
        body = resp.text
        logging.getLogger("HTTP").warning(
            "%s status=%s reason=%s\nHeaders: %s\nBody: %s",
            note, resp.status_code, getattr(resp, "reason", ""), headers, body[:2000]  # limit body length
        )
    except Exception:
        logging.getLogger("HTTP").exception("Failed to log HTTP response")
# ----------------------------------------------------------------------------------------------



from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import threading
import openpyxl as opnx

from interfaz.inicio import InicioScreen
from interfaz.procesando import ProcesandoScreen
from interfaz.gestor import GestorScreen
from I_API import submain
from Extraccion import creador




class MetaData_Sorter(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(InicioScreen(on_ruta_seleccionada=self.procesar_ruta, name="inicio"))
        self.sm.add_widget(ProcesandoScreen(name='procesando'))
        self.sm.add_widget(GestorScreen(name='gestor'))
        return self.sm

    

    def procesar_ruta(self, ruta):
        self.ruta = ruta
    # Mostrar procesando en la UI
        self.sm.current = "procesando"
    
    # Crear y lanzar hilo para trabajo pesado
        hilo =threading.Thread(target=self._ejecutar_creador, args=(ruta,), daemon=True)
        hilo.start()

    def _ejecutar_creador(self, ruta):
        # Esto corre en segundo plano
        creador.iniciador(ruta)  # bloquea, pero no la UI

        # Cuando termina, volvemos al hilo principal para cambiar pantalla
        Clock.schedule_once(lambda dt: self._mostrar_gestor(), 0)
    
    def _mostrar_gestor(self):
        self.sm.current = "gestor"
        Clock.schedule_once(lambda dt: self._iniciar_hilo(), 0)

    def _iniciar_hilo(self):
        hilo = threading.Thread(
            target=submain.disparador,
            kwargs={'pedir_db_func': PedirDB, 'cargar_func': cargar, 'rellDER': GestorScreen.rellena_derecha, 'rellIZQ': GestorScreen.rellena_izquierda},
            daemon=True
        )
        hilo.start()

        


def PedirDB(C_Entrada):
        #print("Iniciando pedido a la DB")
        Archivo=opnx.load_workbook("DB.xlsx")
        Libro=Archivo['Sheet'] 
        P=Libro['P2']
        p=P.value
        #print("ultimo Extraido: ",p)
        for u in range(50):
            R=p+u
            if R >= Libro['A2'].value:
                print("No hay mas canciones por procesar")
                break
            T=Libro[f'B{R}']
            if not T.value:
                print("Cancion vacia, saltando") 
                T=None
                continue
            A=Libro[f'C{R}']
            al=Libro[f'D{R}']
            Ao=Libro[f'G{R}']
            G= Libro[f'F{R}']
            Cancion = {"Titulo":T.value ,"Artista": A.value,"Album": al.value,"Año": Ao.value,"Genero":G.value,"ID":R,"Estado":"PEND"}
            #print("cancion pedida: ",Cancion)
            C_Entrada.put(Cancion)
            Clock.schedule_once(lambda dt: GestorScreen.rellena_izquierda(self,Cancion))#PENDIENTE, ARREGLAR, DEBE LLAMARSE RELLENA DERECHA, OJO, SE TOCARON LAS FUNCIONES QUE SE LLAMAN(REQCUERDE ARREGLAR)

        #print("cola de entrada actual:", list(C_Entrada.queue))

        #print("ultima Cancion pedida: ",R)
        Libro["P2"]=R+1
        #print("Fin del añadido")
        Archivo.save("DB.xlsx")


def cargar(C_Salida,):
    print("iniciando extraccion de la cola de salida")
    Archivo=opnx.load_workbook("DB.xlsx")
    Libro=Archivo['Sheet'] 
    P=Libro['P3']
    p=P.value
    while not C_Salida.empty():
        cancion=C_Salida.get()
        print("cancion extraida: ",cancion)
        #envia a la interfaz
        Clock.schedule_once(lambda dt: GestorScreen.rellena_derecha(GestorScreen(),cancion))
        #comienza a guardar en la DB
        Libro[f'i{p}']=cancion["Titulo"]
        Libro[f'j{p}']=cancion["Artista"]
        Libro[f'k{p}']=cancion["Album"]
        #Libro[f'l{p}']=cancion["Numero de pista"]
        Libro[f'n{p}']=cancion["Año"]
        Libro[f'q{p}']=cancion["Estado"]
        p+=1#avanza de fila
    #actualiza el parametro de ultimo guardado y guarda
    Libro['P3']=p
    Archivo.save("DB.xlsx")

if __name__ == "__main__":

    app = MetaData_Sorter()
    app.run()
