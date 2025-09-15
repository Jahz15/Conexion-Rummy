from archivo_de_importaciones import importar_desde_carpeta

Jugador = importar_desde_carpeta(
    "jugador.py", #Archivo
    "Jugador" #Clase
    )

Elemento_texto = importar_desde_carpeta(
    "elementos_de_interfaz_de_usuario.py", #Archivo
    "Elemento_texto", #Clase
    "recursos_graficos" #Nombre de la carpeta
    )

constantes = importar_desde_carpeta(
    nombre_archivo="constantes.py",
    nombre_carpeta="recursos_graficos"
    )

class Jugador_interfaz(Jugador):
    def __init__(self,*args,un_juego=None,x=0,y=0,ancho=0,alto=0,**kwargs):
        super().__init__(*args,**kwargs)
        self.un_juego = un_juego
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.usuario = self.elemento_usuario()
    def datos_jugador(self):
        return f'{self.nombre_jugador} j{self.nro_jugador}'
    def elemento_usuario(self):
        usuario = Elemento_texto(
            self.un_juego,
            self.datos_jugador(),
            self.ancho,
            self.alto,
            self.x,
            self.y,
            tamaño_fuente=constantes.F_PEQUENA,
            fuente=constantes.FUENTE_ESTANDAR,
            color=constantes.ELEMENTO_FONDO_PRINCIPAL,
            radio_borde=constantes.REDONDEO_INTERMEDIO,
            color_texto=constantes.COLOR_TEXTO_PRINCIPAL,
            color_borde=constantes.ELEMENTO_FONDO_SECUNDARIO,
            grosor_borde=constantes.BORDE_INTERMEDIO,
        )
        return usuario