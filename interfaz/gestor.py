import os
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

# Ruta al fondo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_fondo = os.path.join(BASE_DIR, "fondo.png")

class GestorLayout(FloatLayout):
    ruta_fondo = StringProperty(ruta_fondo)

class TablaWidget(BoxLayout):  # contenedor para el RecycleView
    pass

class Fila(BoxLayout):  # cada fila de la tabla
    idx=NumericProperty(None)
    UTitulo = StringProperty("")
    UGenero = StringProperty("")
    UAnio = StringProperty("")
    UArtista = StringProperty("")
    UAlbum = StringProperty("")
    
    OTitulo = StringProperty("")
    OGenero = StringProperty("")
    OAnio = StringProperty("")
    OArtista = StringProperty("")
    OAlbum = StringProperty("")
    on_left_pressed = ObjectProperty(None)
    on_right_pressed = ObjectProperty(None)


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
                rgba: 0, 0, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: "Metadatos Actuales"
        Label:
            text: "Metadatos Organizados"

    TablaWidget:   # aquí va el contenedor del RV
        id: tabla
        size_hint: 0.9, 0.6
        pos_hint: {"center_x": 0.5, "top": 0.85}
        viewclass: "Fila"

    Button:
        text: "Elegir Otra Carpeta"
        font_size: 20
        size_hint: None, None  
        size: 200, 50
        pos_hint: {"center_x": 0.2, "center_y": 0.2}
        disabled: True
                    
    Button:
        text: "Reemplazar datos"
        font_size: 20
        size_hint: None, None
        size: 200, 50
        pos_hint: {"center_x": 0.8, "center_y": 0.2}
        disabled: True
                

<TablaWidget>:
    orientation: "vertical"
    padding: dp(8)
    RecycleView:
        id: rv
        viewclass: "Fila"
        size_hint: 1, 1
        RecycleBoxLayout:
            id: rv_layout
            orientation: "vertical"
            default_size: None, dp(100)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            spacing: dp(6)
            padding: dp(4) 

<Fila>:
    orientation: "horizontal"
    size_hint_x: 1
    size_hint_y: None
    height: dp(100)
    padding: dp(4)
    spacing: dp(4)

    BoxLayout:#indice
        orientation: "vertical"
        size_hint_x:None
        width: 15
        canvas.before:
            Color:
                rgba: 0, 0, 0, 0.6
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: str(root.idx)
            font_size: 20
            bold: True
            color: 1, 1, 1, 1
            size_hint_y: None
            halign: "center"
            valign: "middle"
            text_size: self.width, self.height
    #tabla izquierda                
    Button:
        id: left_btn
        size_hint_x: 0.5
        size_hint_y: 1
        background_normal: ""            
        background_color: 0, 0, 0.6, 1   # azul oscuro      
        on_release: root.on_left_pressed(root.idx, root)
          
                            
        #contenedor de columnas
        BoxLayout: 
            size: self.parent.size   # fuerza a ocupar todo el botón
            pos: self.parent.pos
            orientation: "horizontal"
            
                    
            #contenedor de etiquetas
            BoxLayout:
                orientation:"vertical"
                size_hint_x:None
                width: dp(50)
                size_hint_y:1
                padding: dp(2)
                spacing: dp(2)
                
                        
                Label:
                    text: "Titulo: "
                    font_size: 14
                    halign: "left"
                    spacing: dp(2)
                    
                Label:
                    text: "Artista: "
                    font_size: 14
                    halign: "left"
                    valign: "middle"
                Label:
                    text: "Album: "
                    font_size: 14
                    halign: "left"
                    valign: "middle"
                Label:
                    text: "Genero: "
                    font_size: 14
                    halign: "left"
                    valign: "middle"
                Label:
                    text: "Año: "
                    font_size: 14
                    halign: "left"
                    valign: "middle"
                        
            BoxLayout:
                orientation:"vertical"
                size_hint_x:1
                    
                Label:
                    text: root.UTitulo
                    font_size: 14
                    halign: "left"
                    spacing: dp(2)
                    
                Label:
                    text: root.UArtista
                    font_size: 14
                    halign: "left"
                    valign: "middle"
                Label:
                    text: root.UAlbum
                    font_size: 14
                    halign: "left"
                    valign: "middle"
                Label:
                    text: root.UGenero
                    font_size: 14
                    halign: "left"
                    valign: "middle"
                Label:
                    text: root.UAnio
                    font_size: 14
                    halign: "left"
                    valign: "middle"    

    #tabla derecha
    Button:
        id: right_btn
        size_hint_x: 0.5
        size_hint_y: 1
        background_normal: ""
        background_color: 0.55, 0.3, 0, 1  # marrón
        on_release: root.on_right_pressed(root.idx, root)
        
        #contenedor de columnas
        BoxLayout: 
            size: self.parent.size   # fuerza a ocupar todo el botón
            pos: self.parent.pos
            orientation: "horizontal"
            
                    
            #contenedor de etiquetas
            BoxLayout:
                orientation:"vertical"
                size_hint_x:None
                width: dp(50)
                size_hint_y:1
                padding: dp(2)
                spacing: dp(2)
                
                        
                Label:
                    text: "Titulo: "
                    font_size: 14
                    halign: "left"
                    spacing: dp(2)
                    
                Label:
                    text: "Artista: "
                    font_size: 14
                    halign: "left"
                    valign: "middle"
                Label:
                    text: "Album: "
                    font_size: 14
                    halign: "left"
                    valign: "middle"
                Label:
                    text: "Genero: "
                    font_size: 14
                    halign: "left"
                    valign: "middle"
                Label:
                    text: "Año: "
                    font_size: 14
                    halign: "left"
                    valign: "middle"
                        
            BoxLayout:
                orientation:"vertical"
                size_hint_x:1
                
                    
                Label:
                    text: root.OTitulo
                    font_size: 14
                    halign: "left"
                    spacing: dp(2)
                    
                Label:
                    text: root.OArtista
                    font_size: 14
                    halign: "left"
                    valign: "middle"
                Label:
                    text: root.OAlbum
                    font_size: 14
                    halign: "left"
                    valign: "middle"
                Label:
                    text: root.OGenero
                    font_size: 14
                    halign: "left"
                    valign: "middle"
                Label:
                    text: root.OAnio
                    font_size: 14
                    halign: "left"
                    valign: "middle"
   
""")

class GestorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GestorLayout()
        self.add_widget(self.layout)
        self.rv = self.layout.ids.tabla.ids.rv
        self.campos = ["Titulo", "Artista", "Album", "Año", "Genero"]
    def safe_str(self,valor):
        return "" if valor is None else str(valor)

    def _normalizar_item(self, cancion, prefijo="U"):
        return {f"{prefijo}{campo}": self.safe_str(cancion.get(campo)) for campo in self.campos}


    def agregar_cancion(self, cancion):
    # Crear un nuevo item con los datos "sucios"
        nuevo_item = {
            "idx": cancion["ID"],
            **self._normalizar_item(cancion, "U"),  # datos originales
            **self._normalizar_item({}, "O"),       # datos organizados vacíos
            "on_left_pressed": self.on_left_pressed,
            "on_right_pressed": self.on_right_pressed
        }
        self.rv.data.append(nuevo_item)
        self.rv.refresh_from_data()
        


    def actualizar(self,datos):
    
        cid = datos.get("ID")
        if cid is None:
            print("No hay ID, no se puede actualizar")
            return

        pos = cid - 1  # posición directa según el ID

        # Verificación mínima de rango
        if pos < 0 or pos >= len(self.rv.data):
            print(f" ID {cid} fuera de rango (posición {pos})")
            return

        item = self.rv.data[pos]
        item.update(self._normalizar_item(datos, "O"))
        self.rv.refresh_from_data()

    #botnones de las tablas  
    def on_left_pressed(self, idx, fila_view):
        print(f"Se presionó un widget de la tabla IZQUIERDA, fila idx={idx}")
        

    def on_right_pressed(self, idx, fila_view):
        print(f"Se presionó un widget de la tabla DERECHA, fila idx={idx}")



#estructua de datos de ejemplo
#data = {
#    150: {
#        "sucio": {
#            "titulo": "Título sucio 150",
#            "artista": "Artista sucio 150",
#            "genero": "Género sucio 150",
#            "anio": "Año sucio 150",
#            "album": "Álbum sucio 150"
#        },
#        "limpio": {
#            "titulo": "Título limpio 150",
#            "artista": "Artista limpio 150",
#            "genero": "Género limpio 150",
#            "anio": "Año limpio 150",
#            "album": "Álbum limpio 150"
#        },
#        "pos": 149
#    }
#    151: {
#        "sucio": {
#            "titulo": "Título sucio 150",
#            "artista": "Artista sucio 150",
#            "genero": "Género sucio 150",
#            "anio": "Año sucio 150",
#            "album": "Álbum sucio 150"
#        },
#        "limpio": {
#            "titulo": "Título limpio 150",
#            "artista": "Artista limpio 150",
#            "genero": "Género limpio 150",
#            "anio": "Año limpio 150",
#            "album": "Álbum limpio 150"
#        },
#        "pos": 150
#    }
#}

#{
#            "idx": i,
#            "UTitulo": f"Título sucio{i}",
#            "UGenero": f"Genero sucio{i}",
#            "UAnio": f"Año sucio{i}",
#            "UArtista": f"Artista Sucio{i}",
#            "UAlbum": f"Album Sucio{i}",
#
#            "OTitulo": f"Título limpio{i}",
#            "OGenero": f"Genero Limpio{i}",
#            "OAnio": "Año Limpio",
#            "OArtista": f"Artista Limpio{i}",
#            "OAlbum": f"Album Limpio{i}"
#        }