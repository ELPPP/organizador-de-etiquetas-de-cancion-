import os
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

# Ruta al fondo (misma lógica que en inicio)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_fondo = os.path.join(BASE_DIR, "fondo.png")

Builder.load_string("""
<ProcesandoLayout>:
    orientation: "vertical"
    padding: [0, 200, 0, 200]                
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
            source: root.ruta_fondo

    Label:
        text: "Procesando..."
        font_size: 32
        size_hint_y: 1
        halign: "center"
        valign: "middle"
""")

class ProcesandoLayout(BoxLayout):
    ruta_fondo = StringProperty("")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ruta_fondo = ruta_fondo

class ProcesandoScreen(Screen):
    print("entrando a procesando")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(ProcesandoLayout())
