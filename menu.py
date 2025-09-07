import pygame

class Menu:
    def __init__(self,un_juego,ancho,alto,x,y,fondo_color,borde_color,grosor_borde,redondeo):
        self.pantalla = un_juego.pantalla
        self.ancho, self.alto = ancho, alto
        self.x, self.y = x, y
        self.menu = pygame.Rect(self.x,self.y,self.ancho,self.alto)
        self.fondo_color = fondo_color
        self.borde_color = borde_color
        self.grosor_borde = grosor_borde
        self.redondeo = redondeo 
        self.botones = []
        self.imagenes = []
        self.visible = False
    def mostrar(self):
        self.visible = True
    def ocultar(self):
        self.visible = False
    def agregar_imagen(self, imagen, posicion_relativa,scala):
        posicion_absoluta = (
            self.x + posicion_relativa[0],
            self.y + posicion_relativa[1]
        )
        w = imagen.get_width()
        h = imagen.get_height()
        tamano = (w*scala,h*scala)
        imagen = pygame.transform.scale(imagen, tamano)
        self.imagenes.append((imagen, posicion_absoluta))
    def dibujar_imagen(self):
        for imagen, posicion in self.imagenes:
            self.pantalla.blit(imagen, posicion)
    def crear_elemento(self, Clase, x,y, **kwargs):
        x,y = self.x + x, self.y + y
        kwargs["x"], kwargs["y"] = x,y
        nuevo_elemento = Clase(**kwargs)
        self.botones.append(nuevo_elemento)
    def dibujar_fondo(self):
        """Dibuja solo el fondo y el borde del menú"""
        pygame.draw.rect(self.pantalla, self.fondo_color, self.menu, border_radius=self.redondeo)
        if self.grosor_borde > 0 :
            pygame.draw.rect(self.pantalla, self.borde_color, self.menu, self.grosor_borde, border_radius=self.redondeo)

    def dibujar_botones(self):
        """Dibuja todos los botones del menú"""
        for boton in self.botones:
            boton.dibujar()

    def dibujar_imagenes(self):
        """Dibuja todas las imágenes del menú"""
        for imagen, posicion in self.imagenes:
            self.pantalla.blit(imagen, posicion)

    def dibujar_menu(self):
        """Método principal de dibujo del menú"""
        if not self.visible:
            return
        self.dibujar_fondo()
        self.dibujar_botones()
        self.dibujar_imagenes()
    def manejar_eventos(self, evento):
        if not self.visible:  # Solo procesar eventos si el menú es visible
            return
        
        for boton in self.botones:
            boton.manejar_evento(evento)

    def verificar_hovers(self, posicion_raton):
        if not self.visible:  # Solo verificar hovers si el menú es visible
            return
            
        for boton in self.botones:
            boton.verificar_hover(posicion_raton)