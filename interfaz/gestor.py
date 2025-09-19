import os
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout  # """"" cambio: FloatLayout para usar pos_hint
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout  # """"" FloatLayout permite pos_hint exacto
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView  

# Ruta al fondo (misma lógica que en inicio)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_fondo = os.path.join(BASE_DIR, "fondo.png")

Builder.load_string("""
<GestorLayout>:                
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
            source: root.ruta_fondo
                    
    ProgressBar:
        id: progress
        max: 100
        value: 30
        size_hint_x: 0.8
        size_hint_y: None
        height: 20
        pos_hint: {"center_x": 0.5, "top": 0.95}  
                    
    BoxLayout:
        size_hint: 0.9, None
        height: 30
        pos_hint: {"center_x": 0.5, "top": 0.88}
        canvas.before:
            Color:
                rgba: 0, 0, 0, 1   # negro para debug
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: "Metadatos Actuales"
        Label:
            text: "Metadatos Organizados"

    
    ScrollView:
        size_hint: 0.9, 0.55
        pos_hint: {"center_x": 0.5, "center_y": 0.55}

        BoxLayout:
            id: contenedor_tablas
            orientation: "horizontal"
            size_hint_y: None
            height: self.minimum_height
            spacing: 10
            

            # Tabla izquierda
            GridLayout:
                id: tabla_izquierda
                cols: 1
                size_hint_x: 0.5
                size_hint_y: None
                height: self.minimum_height
                spacing: 5
                canvas.before:
                    Color:
                        rgba: 1, 0, 0, 0.3   # rojo semitransparente
                    Rectangle:
                        pos: self.pos
                        size: self.size

            # Tabla derecha
            GridLayout:
                id: tabla_derecha
                cols: 1
                size_hint_x: 0.5
                size_hint_y: None
                height: self.minimum_height
                spacing: 5
                canvas.before:
                    Color:
                        rgba: 1, 0, 0, 0.3   # rojo semitransparente
                    Rectangle:
                        pos: self.pos
                        size: self.size
                
    Button:
        text: "Elegir Otra Carpeta"
        font_size: 20
        size_hint:(None,None)  
        size_hint_x: None
        size:(200, 50)
        pos_hint: {"center_x": 0.2,"center_y": 0.2}
        disabled: True
                    
    Button:
        text: "Reemplazar datos"
        font_size: 20
        size_hint: None, None
        size: 200, 50
        pos_hint: {"center_x": 0.8, "center_y": 0.2}
        disabled: True
""")

class GestorLayout(FloatLayout):
    ruta_fondo = StringProperty(ruta_fondo)



llave={'Titulo': 'Frame of Mind', 'Artista': 'Tristam,Braken', 'Album': 'Tristam', 'Numero de  pista': '', 'Genero': '', 'Año': '2014-04-25', 'Numero de pista': 2}


class GestorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GestorLayout()
        self.add_widget(self.layout)

    #""""" Método público: rellena tabla izquierda
    def rellena_izquierda(self, llave: dict):
        fila = self._crear_fila(llave)
        self.layout.ids.tabla_izquierda.add_widget(fila)

    #""""" Método público: rellena tabla derecha
    def rellena_derecha(self, llave: dict):
        fila = self._crear_fila(llave)
        self.layout.ids.tabla_derecha.add_widget(fila)

    #""""" Método privado: construye el widget de una fila
    def _crear_fila(self, llave: dict):
        fila = BoxLayout(orientation="vertical", padding=5, spacing=5,
                         size_hint_y=None, height=100)

        # fondo morado para debug
        with fila.canvas.before:
            Color(0.5, 0, 0.5, 0.3)
            rect = Rectangle(pos=fila.pos, size=fila.size)
            fila.bind(pos=lambda _, __: setattr(rect, "pos", fila.pos))
            fila.bind(size=lambda _, __: setattr(rect, "size", fila.size))

        # título
        fila.add_widget(Label(
            text=f"Título: {llave.get('Titulo', '')}",
            size_hint_y=None, height=30, halign="left"
        ))

        # grid con metadatos
        grid = GridLayout(cols=2, size_hint_y=None, height=60)
        grid.add_widget(Label(text=f"Artista: {llave.get('Artista','')}"))
        grid.add_widget(Label(text=f"Género: {llave.get('Genero','')}"))
        grid.add_widget(Label(text=f"Álbum: {llave.get('Album','')}"))
        grid.add_widget(Label(text=f"Año: {llave.get('Año','')}"))
        fila.add_widget(grid)

        return fila


#metodo disparador....
##class TestApp(App):
#    def build(self):
#        screen = ProcesandoScreen(name="procesando")
#        llave = {
#            'Titulo': 'Frame of Mind',
#            'Artista': 'Tristam,Braken',
#            'Album': 'Tristam',
#            'Genero': '',
#            'Año': '2014-04-25',
#            'Numero de pista': 2
#        }
#
#        # Simulación: usar métodos públicos
#        for i in range(10):
#            screen.rellena_izquierda(llave)
#        for i in range(10):
#            screen.rellena_derecha(llave)
#
#        return screen
##def disparador():
#    TestApp().run()

#if __name__ == "__main__":
#    disparador()
