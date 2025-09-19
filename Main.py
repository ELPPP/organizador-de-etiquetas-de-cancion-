from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen


from interfaz.inicio import InicioScreen
from interfaz.procesando import ProcesandoScreen
from interfaz.gestor import GestorScreen

from Extraccion import creador
from kivy.clock import Clock
import threading

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
        


MetaData_Sorter().run()

if __name__ == "__main__":
    app = MetaData_Sorter()
    app.run()



def disparador():
    
    print("disparador")

def cargar():
    print("cargar")

def PedirDB():
    print("PedirDB")