from archivo_de_importaciones import importar_desde_carpeta
import pygame
Mazo = importar_desde_carpeta("mazo.py","Mazo")
Menu = importar_desde_carpeta("menu.py","Menu","recursos_graficos")

CartelAlerta = importar_desde_carpeta(
    nombre_archivo="elementos_de_interfaz_de_usuario.py",
    nombre_clase="CartelAlerta",
    nombre_carpeta="recursos_grafico",
)

class Mazo_interfaz(Mazo):
    def __init__(self, *args, un_juego=None,ruta_imagen_mazo, **kwargs):
        super().__init__(*args, **kwargs)
        self.un_juego = un_juego
        self.ruta_imagen_mazo = ruta_imagen_mazo
        self.imagen_mazo = pygame.image.load(ruta_imagen_mazo)

    def MensajeAlerta(self, mensaje, ancho=500, alto=300):
        """
        Crea un cartel de alerta en el centro de la pantalla
        con el mensaje recibido.
        """
        # Instanciar el cartel
        cartel = CartelAlerta(
            pantalla=self.un_juego.pantalla,
            mensaje=mensaje,
            x=0,  # se recalcula en centrar_en_pantalla
            y=0,
            ancho=ancho,
            alto=alto
        )

        # Centrar y mostrar
        cartel.centrar_en_pantalla()
        return cartel
    def reparticion_visual_cartas(self):
        self.MensajeAlerta("Repartiendo cartas")


# class Mazo:
#     def __init__(self):
#         self.cartas = []
#     def agregar_cartas(self,carta):
#         self.cartas.append(carta)
#     def calcular_nro_mazos(self,numero_de_jugadores):
        
#         resultado = numero_de_jugadores // 3  
#         if numero_de_jugadores % 3 != 0:
#             resultado += 1
#         return resultado
#     def revolver_mazo(self):
#         shuffle(self.cartas)

#     def mostrar_cartas(self,mensaje):
#         print(mensaje)
#         for carta in self.cartas:
#             print(carta)
#     def mostrar_numero_cartas(self,mensaje):
#         print(str(mensaje) + str(len(self.cartas)))

#     def repartir_cartas(self, lista_de_jugadores):    #solo para pruebass de interfaz
#         num_jugadores = len(lista_de_jugadores)
#         print(f"Número de jugadores: {num_jugadores}")
#         print(f"Cartas a repartir: {10 * num_jugadores}")
#         print(f"Cartas disponibles en el mazo: {len(self.cartas)}")

#         if 10 * num_jugadores > len(self.cartas):
#             raise ValueError("¡Error! No hay suficientes cartas en el mazo para repartir a los jugadores.")

#         cartas_indice_repartidas = sample(list(enumerate(self.cartas)), 10 * num_jugadores)
#         cartas_repartidas = []
#         indice_de_cartas_eliminar = []
#         for x in cartas_indice_repartidas:
#             cartas_repartidas.append(x[1])
#             indice_de_cartas_eliminar.append(x[0])
#         jugadores = [[] for _ in range(num_jugadores)]
#         for index, carta in enumerate(cartas_repartidas):
#             indice_de_jugador = index % num_jugadores
#             jugadores[indice_de_jugador].append(carta)

#         for indice in sorted(indice_de_cartas_eliminar, reverse=True):
#             self.cartas.pop(indice)

#         return jugadores