from archivo_de_importaciones import importar_desde_carpeta
import pygame

Cartas = importar_desde_carpeta(
    nombre_archivo= "cartas.py",
    nombre_clase= "Cartas")


class Cartas_interfaz(Cartas):
    def __init__(self, *args, ruta_imagen=None,**kwargs):
        # Pasar todos los argumentos posicionales y nombrados al padre
        super().__init__(*args, **kwargs)

        self.ruta_imagen = ruta_imagen
        self.imagen = pygame.image.load(self.ruta_imagen)
    def imagen_asociada(self):
        return self.imagen



#Ejemplo de uso:
img_corazon_2 = importar_desde_carpeta(
    nombre_archivo="Imagenes/Cartas/Corazon (2).png",
    nombre_carpeta="assets")

carta1 = Cartas_interfaz(ruta_imagen=img_corazon_2,numero=2,figura="picas")
print(carta1)
print(carta1.imagen_asociada())