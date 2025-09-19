import os
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
import tkinter as tk
from tkinter import filedialog
from Extraccion.creador import iniciador as ini
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager


# Obtener la carpeta donde está este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta absoluta a la imagen
ruta_fondo = os.path.join(BASE_DIR, "fondo.png")


def seleccionar_carpeta():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    carpeta = filedialog.askdirectory()
    root.destroy()   # Cierra la ventana oculta
    return carpeta




Builder.load_string("""
<kivySquare>:
    orientation: "vertical"
    padding: [0, 50, 0, 150]  # [izq, arriba, der, abajo]                
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
            source: root.ruta_fondo

    Label:
        text: "Metadata Sorter"
        font_size: 32
        size_hint_y: 0.3   # 👆 Ocupa 30% de la altura

    Label:
        text: "Selecciona Tu Carpeta De Musica"
        font_size: 24
        size_hint_y: 0.3   # 👆 Otro 30%

    Button:
        text: "Buscar Archivos"
        font_size: 20
        size_hint:(None,None)  
        size_hint_x: None
        size:(200, 50)
        pos_hint: {"center_x": 0.5}
        on_release: root.open_buscar_archivos()
    
""")

class kivySquare(BoxLayout):
    ruta_fondo = StringProperty("") 
    def __init__(self,on_ruta_seleccionada, **kwargs):
        super().__init__(**kwargs)
        self.ruta_fondo = ruta_fondo
        self.on_ruta_seleccionada = on_ruta_seleccionada  # asignamos la ruta como atributo de la instancia

    def open_buscar_archivos(self):
        path= seleccionar_carpeta()
        if path:
            print(f"Carpeta seleccionada: {path}")
            self.on_ruta_seleccionada(path)  # guardar en el manager
            # ejecutamos el creador en otro thread para no bloquear la GUI
            
        else:
            print("No se seleccionó ninguna carpeta.")
            


class InicioScreen(Screen):
    def __init__(self, on_ruta_seleccionada, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(kivySquare(on_ruta_seleccionada, ruta_fondo=ruta_fondo))



