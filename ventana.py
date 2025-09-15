"""En la parte donde está def obtener_salas_disponibles(self), se coloco como ejemplo un arreglo de salas, puedes cambiarlo por la logica propia de redes para obtener la lista de salas disponibles desde la red."""

import pygame
import sys



from recursos_graficos import constantes
# Importaciones absolutas
from recursos_graficos.elementos_de_interfaz_de_usuario import Elemento_texto, Boton, BotonRadio, EntradaTexto, CartelAlerta
from recursos_graficos.menu import Menu
from redes_interfaz import acciones


"""Clase ventana donde estaran todos los diseños e interacciones"""
class Ventana:
    """Inicializar pygame, fuentes, crear pantalla, nombre de la misma, cargar imagenes, crear menus y botones"""
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.pantalla = pygame.display.set_mode((constantes.ANCHO_VENTANA,constantes.ALTO_VENTANA))
        self.cartel_alerta = CartelAlerta(self.pantalla, "", 0, 0)
        pygame.display.set_caption("Rummy500")
        # Datos de juego
        self.lista_elementos = {
            "nombre_creador": "",
            "nombre_sala": "",
            "cantidad_jugadores":0,
            "ip_sala":"",
            "lista_jugadores": [],
            "nombre_unirse": "",
            "salas_disponibles" : []
        }


        self.elementos_creados = []

        # Logo
        self.logo_rummy = pygame.image.load("assets//Imagenes//Logos//Logo(1).png")

        # Menús iniciales
        self.menu_instrucciones = self.Menu_instrucciones()
        self.menu_seleccion_sala = self.Menu_seleccion_sala()
        self.menu_inicio = self.Menu_inicio()
        self.boton_jugar = self.Boton_jugar()
        self.menu_Cantidad_Jugadores = self.Menu_Cantidad_Jugadores()
        self.menu_mesa_espera = self.Menu_mesa_espera()
        Buscar_salas = acciones.Buscar_salas(self)

        #Temporizador
        self.clock = pygame.time.Clock()


    # --- NUEVO: métodos para mostrar los menús de nombre ---

    """Funcion para centrar en la ventana"""
    def centrar(self,ancho_elemento,alto_elemento):
        x = (constantes.ANCHO_VENTANA - ancho_elemento)/2
        y = (constantes.ALTO_VENTANA - alto_elemento)/2
        return (x,y)

    """Funcion que crea el boton Jugar, se pasa por parametros las constantes, las posiciones se definen manualemente"""
    def Boton_jugar(self):
        x,y = self.centrar(constantes.ELEMENTO_MEDIANO_ANCHO,constantes.ELEMENTO_MEDIANO_ALTO)
        boton_jugar = Boton(
            un_juego= self,
            texto= "JUGAR",
            ancho= constantes.ELEMENTO_MEDIANO_ANCHO,
            alto= constantes.ELEMENTO_MEDIANO_ALTO,
            x= x,
            y= y,
            tamaño_fuente= constantes.F_MEDIANA,
            fuente= constantes.FUENTE_LLAMATIVA,
            color= constantes.ELEMENTO_FONDO_PRINCIPAL,
            radio_borde= constantes.REDONDEO_NORMAL,
            color_texto= constantes.COLOR_TEXTO_PRINCIPAL,
            color_borde= constantes.ELEMENTO_BORDE_PRINCIPAL,
            grosor_borde= constantes.BORDE_PRONUNCIADO,
            color_borde_hover= constantes.ELEMENTO_HOVER_PRINCIPAL,
            color_borde_clicado= constantes.ELEMENTO_CLICADO_PRINCIPAL,
            accion= lambda: acciones.Mostrar_seccion(self,self.menu_inicio)
            )
        self.elementos_creados.append(boton_jugar)
        return boton_jugar

    """Funciones que crean el menu de instrucciones usan ElementoTexto, y Boton"""
    def Menu_instrucciones(self):
        x_menu, y_menu = self.centrar(constantes.ANCHO_MENU_INSTRUCCIONES,constantes.ALTO_MENU_INSTRUCCIONES)

        menu_instrucciones = Menu(
            un_juego=self,
            ancho=constantes.ANCHO_MENU_INSTRUCCIONES,
            alto=constantes.ALTO_MENU_INSTRUCCIONES,
            x=x_menu,
            y=y_menu,
            fondo_color=constantes.ELEMENTO_FONDO_PRINCIPAL,
            borde_color=constantes.ELEMENTO_BORDE_PRINCIPAL,
            grosor_borde=constantes.BORDE_PRONUNCIADO,
            redondeo=constantes.REDONDEO_PRONUNCIADO
        )

        self.crear_elementos_instrucciones(menu_instrucciones)

        self.crear_elementos_control_instrucciones(menu_instrucciones)

        self.elementos_creados.append(menu_instrucciones)
        return menu_instrucciones
    def crear_elementos_instrucciones(self,menu_instrucciones):
        # Texto ocupa casi todo el ancho y 70% de la altura
        menu_instrucciones.crear_elemento(
            Clase=Elemento_texto,
            x=constantes.BORDE_PRONUNCIADO,
            y=constantes.ALTO_MENU_INSTRUCCIONES * 0.10,
            un_juego=self,
            texto=constantes.TEXTO_DE_INSTRUCCIONES,
            ancho=constantes.ANCHO_MENU_INSTRUCCIONES - (constantes.BORDE_PRONUNCIADO * 2),
            alto=constantes.ALTO_MENU_INSTRUCCIONES * 0.70,
            tamaño_fuente=constantes.F_MEDIANA,
            fuente=constantes.FUENTE_ESTANDAR,
            color=constantes.ELEMENTO_FONDO_PRINCIPAL,
            radio_borde=constantes.REDONDEO_INTERMEDIO,
            color_texto=constantes.COLOR_TEXTO_PRINCIPAL,
            color_borde=constantes.BLANCO,
            grosor_borde=constantes.BORDE_LIGERO,
            alineacion_vertical="arriba",
            alineacion="izquierda"
        )
    def crear_elementos_control_instrucciones(self,menu_instrucciones):
        
        # Botón volver ocupa ancho pequeño y se ubica centrado abajo
        menu_instrucciones.crear_elemento(
            Clase=Boton,
            x=(constantes.ANCHO_MENU_INSTRUCCIONES - constantes.ELEMENTO_PEQUENO_ANCHO) / 2,
            y=constantes.ALTO_MENU_INSTRUCCIONES - constantes.ELEMENTO_PEQUENO_ALTO * 1.2,
            un_juego=self,
            texto="VOLVER",
            ancho=constantes.ELEMENTO_PEQUENO_ANCHO,
            alto=constantes.ELEMENTO_PEQUENO_ALTO,
            tamaño_fuente=constantes.F_MEDIANA,
            fuente=constantes.FUENTE_LLAMATIVA,
            color=constantes.ELEMENTO_FONDO_PRINCIPAL,
            radio_borde=constantes.REDONDEO_NORMAL,
            color_texto=constantes.COLOR_TEXTO_PRINCIPAL,
            color_borde=constantes.ELEMENTO_BORDE_PRINCIPAL,
            grosor_borde=constantes.BORDE_INTERMEDIO,
            color_borde_hover=constantes.ELEMENTO_HOVER_PRINCIPAL,
            color_borde_clicado=constantes.ELEMENTO_CLICADO_PRINCIPAL,
            accion=lambda: acciones.Mostrar_seccion(self, self.menu_inicio)
        )
    """Fin de las funciones que crean el menu de instrucciones"""

    """Se define las funciones para el menu nombre de usuario, depende de si es el creador o es solamente un participante ejecuta una cosa u otra"""
    def Menu_nombre_usuario(self,creador_sala):
        
        x_menu,y_menu = self.centrar(constantes.ANCHO_MENU_NOM_USUARIO,constantes.ALTO_MENU_NOM_USUARIO)
        
        menu_nombre_usuario = Menu(
            self,
            constantes.ANCHO_MENU_NOM_USUARIO,
            constantes.ALTO_MENU_NOM_USUARIO,
            x_menu,
            y_menu,
            constantes.ELEMENTO_FONDO_SECUNDARO,
            constantes.ELEMENTO_BORDE_SECUNDARIO,
            constantes.BORDE_PRONUNCIADO,
            constantes.REDONDEO_PRONUNCIADO
        )
        
        self.crear_elementos_usuario(menu_nombre_usuario,creador_sala)
        
        self.crear_elementos_control_usuario(menu_nombre_usuario,creador_sala)
        
        self.elementos_creados.append(menu_nombre_usuario)
        return menu_nombre_usuario
    def crear_elementos_usuario(self,menu_nombre_usuario,creador_sala):
        textos = ("DATOS DE LA PARTIDA Y USUARIO","INGRESA TU NOMBRE","NOMBRE DE LA SALA","nombre","nombre sala")
        grupos_elementos_entrada = []
        posiciones_x = [0.06, 0.94] #ubicacion de cada columna
        if not creador_sala:
            textos =("INGRESA TU NOMBRE","nombre")
        for i,texto in enumerate(textos):
            columna = (i-1) % 2
            fila = (i-1) // 2
            posicion_x = posiciones_x[columna]
            posicion_y = 0.35 + (0.23 * fila)
            clase = Elemento_texto if texto in (textos[0:3]) else EntradaTexto
            
            ancho = constantes.ELEMENTO_GRANDE_ANCHO*1.05
            alto = constantes.ELEMENTO_MEDIANO_ALTO*0.95


            if(texto == textos[0]):
                posicion_x = 0.5
                posicion_y = 0.1
                ancho = constantes.ELEMENTO_GRANDE_ANCHO*2
                
            if not creador_sala:
                clase = Elemento_texto if texto in (textos[0]) else EntradaTexto
                if texto == "INGRESA TU NOMBRE":
                    posicion_x, posicion_y = 0.5, 0.1
                    ancho = constantes.ELEMENTO_GRANDE_ANCHO*1.7
                else:
                    posicion_x, posicion_y = 0.5, 0.5
                    ancho = constantes.ELEMENTO_GRANDE_ANCHO*1.5

            x = (constantes.ANCHO_MENU_NOM_USUARIO - ancho)*posicion_x
            y = (constantes.ALTO_MENU_NOM_USUARIO - alto)*posicion_y
            if clase == Elemento_texto:
                menu_nombre_usuario.crear_elemento(
                    Clase=clase,
                    x=x,
                    y=y,
                    un_juego=self,
                    texto=texto,
                    ancho=ancho,
                    alto=alto,
                    tamaño_fuente=constantes.F_GRANDE,
                    fuente=constantes.FUENTE_ESTANDAR,
                    color=constantes.ELEMENTO_FONDO_PRINCIPAL,
                    radio_borde=constantes.REDONDEO_NORMAL,
                    color_texto=constantes.COLOR_TEXTO_PRINCIPAL,
                    color_borde=constantes.ELEMENTO_BORDE_SECUNDARIO,
                    grosor_borde=constantes.BORDE_INTERMEDIO
                )
            elif clase == EntradaTexto:
                permitir_espacios = False
                permitir_numeros = False
                menu_nombre_usuario.crear_elemento(
                    Clase=clase,
                    x=x,
                    y=y,
                    un_juego=self,
                    limite_caracteres = 20,
                    texto = texto,
                    ancho = ancho,
                    alto = alto,
                    tamaño_fuente = constantes.F_MEDIANA,
                    fuente = constantes.FUENTE_ESTANDAR,
                    color = constantes.ELEMENTO_FONDO_PRINCIPAL,
                    radio_borde=constantes.REDONDEO_NORMAL,
                    color_texto=constantes.COLOR_TEXTO_PRINCIPAL,
                    grupo=grupos_elementos_entrada,
                    permitir_espacios=permitir_espacios,
                    permitir_numeros=permitir_numeros,
                    permitir_especiales = False,
                    cartel_alerta = self.cartel_alerta
                )
                grupos_elementos_entrada.append(menu_nombre_usuario.botones[-1])
    def crear_elementos_control_usuario(self,menu_nombre_usuario,creador_sala):
        texto_botones = ("VOLVER","CONFIRMAR")
        crear_sevidor = None
        if not creador_sala: 
            mostrar = self.menu_inicio
            unirse_servidor = lambda: (acciones.validar_y_unirse_sala(self,menu_nombre_usuario))
            accion_confirmar = unirse_servidor
        else:
            mostrar = self.menu_Cantidad_Jugadores
            crear_sevidor = lambda: (acciones.validar_y_crear_servidor(self,menu_nombre_usuario))
            accion_confirmar = crear_sevidor

        accion_por_boton = (lambda: acciones.Mostrar_seccion(self,mostrar),accion_confirmar)
        incrementar_x = 0
        for i,texto_boton in enumerate(texto_botones):
            x =(constantes.ANCHO_MENU_NOM_USUARIO - constantes.ELEMENTO_MEDIANO_ANCHO)*(0.25+incrementar_x)
            y= (constantes.ALTO_MENU_NOM_USUARIO - constantes.ELEMENTO_MEDIANO_ALTO) * (0.85)
            menu_nombre_usuario.crear_elemento(
                Clase=Boton,
                x=x,
                y=y,
                un_juego=self,
                texto = texto_boton,
                ancho=constantes.ELEMENTO_MEDIANO_ANCHO,
                alto=constantes.ELEMENTO_MEDIANO_ALTO,
                tamaño_fuente=constantes.F_MEDIANA,
                fuente=constantes.FUENTE_LLAMATIVA,
                color=constantes.ELEMENTO_FONDO_PRINCIPAL,
                radio_borde=constantes.REDONDEO_NORMAL,
                color_texto=constantes.COLOR_TEXTO_PRINCIPAL,
                color_borde=constantes.ELEMENTO_BORDE_SECUNDARIO,
                grosor_borde=constantes.BORDE_PRONUNCIADO,
                color_borde_hover=constantes.ELEMENTO_HOVER_PRINCIPAL,
                color_borde_clicado=constantes.ELEMENTO_CLICADO_PRINCIPAL,
                accion=accion_por_boton[i]
            )
            incrementar_x = 0.55
    """Fin de las fucniones del menu de usuario"""

    """Funcion Menu de inicio define un menu con sus parametros, y se crean los botones necesarios."""
    def Menu_inicio(self):
        x,y = self.centrar(constantes.ANCHO_MENU_I,constantes.ALTO_MENU_I)
        menu_inicio = Menu(
            un_juego= self,
            ancho= constantes.ANCHO_MENU_I,
            alto= constantes.ALTO_MENU_I,
            x= x,
            y= y,
            fondo_color= constantes.FONDO_VENTANA,
            borde_color= constantes.SIN_COLOR,
            grosor_borde= constantes.SIN_BORDE,
            redondeo= constantes.REDONDEO_PRONUNCIADO
            )
        
        self.crear_elementos_control_inicio(menu_inicio)
        
        posicion_logo = (constantes.ANCHO_MENU_I*0.05,constantes.ALTO_MENU_I*0.1)
        menu_inicio.agregar_imagen(self.logo_rummy,posicion_logo,constantes.SCALA)
        self.elementos_creados.append(menu_inicio)
        return menu_inicio
    def crear_elementos_control_inicio(self,menu_inicio):
        #Creacion de cada boton por cada elemento de texto_menu_inicio(acompañado de sus acciones)
        texto_menu_inicio = ("CREAR SALA","UNIRSE A LA SALA","COMO JUGAR","SALIR DEL JUEGO")
        funciones_menu_inicio = (
            lambda: acciones.Mostrar_seccion(self, self.menu_Cantidad_Jugadores), 
            lambda: acciones.mostrar_menu_nombre_usuario(self,False),   # ← unirse
            lambda: acciones.Mostrar_seccion(self, self.menu_instrucciones),
            self.salir
        )

        incremetar_y = 0
        for i,t in enumerate(texto_menu_inicio):
            x,y = (constantes.ANCHO_MENU_I-constantes.ELEMENTO_GRANDE_ANCHO)*0.9,(constantes.ALTO_MENU_I-constantes.ELEMENTO_GRANDE_ALTO)*(0.17+incremetar_y)
            menu_inicio.crear_elemento(
                Clase=Boton,
                x=x,
                y=y,
                un_juego=self,
                texto=t,
                ancho=constantes.ELEMENTO_GRANDE_ANCHO,
                alto=constantes.ELEMENTO_GRANDE_ALTO,
                tamaño_fuente=constantes.F_MEDIANA,
                fuente=constantes.FUENTE_LLAMATIVA,
                color=constantes.ELEMENTO_FONDO_PRINCIPAL,
                radio_borde=constantes.REDONDEO_NORMAL,
                color_texto=constantes.COLOR_TEXTO_PRINCIPAL,
                color_borde=constantes.ELEMENTO_BORDE_PRINCIPAL,
                grosor_borde=constantes.BORDE_PRONUNCIADO,
                color_borde_hover=constantes.ELEMENTO_HOVER_PRINCIPAL,
                color_borde_clicado=constantes.ELEMENTO_CLICADO_PRINCIPAL,
                accion=funciones_menu_inicio[i]
            )
            incremetar_y += 0.25
    """Fin de las funciones para el menu de inicio"""


    """funciones para el menu cantidad de jugadores, pide los jugadores(6 botones tipo radio,2 botones normales)"""
    def Menu_Cantidad_Jugadores(self):
        x_menu,y_menu = self.centrar(constantes.ANCHO_MENU_CNT_J,constantes.ALTO_MENU_CNT_J)
        
        menu_cantidad = Menu(
            self,
            constantes.ANCHO_MENU_CNT_J,
            constantes.ALTO_MENU_CNT_J,
            x_menu,
            y_menu,
            constantes.ELEMENTO_FONDO_SECUNDARO,
            constantes.ELEMENTO_BORDE_SECUNDARIO,
            constantes.BORDE_PRONUNCIADO,
            constantes.REDONDEO_PRONUNCIADO
        )

        posicion_y = self.crear_elementos_cantidad_jugadores(menu_cantidad)
        
        self.crear_elementos_control_cantidad_jugadores(menu_cantidad,posicion_y)
        
        self.elementos_creados.append(menu_cantidad)
        return menu_cantidad
    def crear_elementos_cantidad_jugadores(self,menu_cantidad):
        ancho_seleccion = constantes.ELEMENTO_GRANDE_ANCHO*2
        alto_seleccion = constantes.ELEMENTO_MEDIANO_ALTO*0.95
        x_seleccion = (constantes.ANCHO_MENU_CNT_J - ancho_seleccion)*(0.5)
        y_seleccion = (constantes.ALTO_MENU_CNT_J - alto_seleccion)*(0.10)
        menu_cantidad
        menu_cantidad.crear_elemento(
            Clase=Elemento_texto,
            x=x_seleccion,
            y=y_seleccion,
            un_juego=self,
            texto="SELECCIONE EL NUMERO DE JUGADORES",
            ancho=ancho_seleccion,
            alto=alto_seleccion,
            tamaño_fuente=constantes.F_GRANDE,
            fuente=constantes.FUENTE_ESTANDAR,
            color=constantes.ELEMENTO_FONDO_PRINCIPAL,
            radio_borde=constantes.REDONDEO_NORMAL,
            color_texto=constantes.COLOR_TEXTO_PRINCIPAL,
            color_borde=constantes.ELEMENTO_BORDE_SECUNDARIO,
            grosor_borde=constantes.BORDE_INTERMEDIO,
        )

        # Generador de textos para cada boton
        texto_menu = (f"{i} JUGADORES" for i in range(2, 8))
        # Lista de botones para el grupo de radio

        botones_radio = []
        posiciones_x = [0.04, 0.50, 0.96] #ubicacion de cada columna
        for i, texto in enumerate(texto_menu):
            columna = i % 3
            fila = i // 3
            posicion_x = posiciones_x[columna]
            posicion_y = 0.30 + (0.30 * fila)
            
            menu_cantidad.crear_elemento(
                Clase=BotonRadio,
                x=(constantes.ANCHO_MENU_CNT_J-constantes.ELEMENTO_PEQUENO_ANCHO) * posicion_x,
                y=(constantes.ALTO_MENU_CNT_J-constantes.ELEMENTO_PEQUENO_ALTO)* posicion_y,
                un_juego=self,
                texto=texto,
                ancho=constantes.ELEMENTO_PEQUENO_ANCHO,
                alto=constantes.ELEMENTO_PEQUENO_ALTO,
                tamaño_fuente=constantes.F_GRANDE,
                fuente=constantes.FUENTE_ESTANDAR,
                color=constantes.ELEMENTO_FONDO_PRINCIPAL,
                radio_borde=constantes.REDONDEO_NORMAL,
                color_texto=constantes.COLOR_TEXTO_PRINCIPAL,
                color_borde=constantes.ELEMENTO_BORDE_SECUNDARIO,
                grosor_borde=constantes.BORDE_LIGERO,
                color_borde_hover=constantes.ELEMENTO_HOVER_PRINCIPAL,
                color_borde_clicado=constantes.ELEMENTO_CLICADO_PRINCIPAL,
                grupo=botones_radio,  # para que funcionen como boton tipo radio
                valor=(i+2),
                deshabilitado=False
            )
            # Agregamos el ultimo boton creado al grupo
            botones_radio.append(menu_cantidad.botones[-1])
        return posicion_y
    def crear_elementos_control_cantidad_jugadores(self,menu_cantidad,posicion_y):
        # Boton de Volver a Inicio
        x_boton_volver = (constantes.ELEMENTO_MEDIANO_ANCHO) / 3
        y_boton_volver = (constantes.ALTO_MENU_CNT_J - constantes.ELEMENTO_MEDIANO_ALTO) * (posicion_y+0.3)
        menu_cantidad.crear_elemento(
                Clase=Boton,
                x=x_boton_volver,
                y=y_boton_volver,
                un_juego=self,
                texto="VOLVER",
                ancho=constantes.ELEMENTO_MEDIANO_ANCHO,
                alto=constantes.ELEMENTO_MEDIANO_ALTO,
                tamaño_fuente=constantes.F_MEDIANA,
                fuente=constantes.FUENTE_LLAMATIVA,
                color=constantes.ELEMENTO_FONDO_PRINCIPAL,
                radio_borde=constantes.REDONDEO_NORMAL,
                color_texto=constantes.COLOR_TEXTO_PRINCIPAL,
                color_borde=constantes.ELEMENTO_BORDE_SECUNDARIO,
                grosor_borde=constantes.BORDE_PRONUNCIADO,
                color_borde_hover=constantes.ELEMENTO_HOVER_PRINCIPAL,
                color_borde_clicado=constantes.ELEMENTO_CLICADO_PRINCIPAL,
                accion=lambda: acciones.Mostrar_seccion(self,self.menu_inicio)
        )

        # Boton de confirmar
        x_boton_confirmar = (constantes.ANCHO_MENU_CNT_J - constantes.ELEMENTO_MEDIANO_ANCHO) * 0.8
        y_boton_confirmar = (constantes.ALTO_MENU_CNT_J - constantes.ELEMENTO_MEDIANO_ALTO) * (posicion_y+0.3)
        menu_cantidad.crear_elemento(
                Clase=Boton,
                x=x_boton_confirmar,
                y=y_boton_confirmar,
                un_juego=self,
                texto="CONFIRMAR",
                ancho=constantes.ELEMENTO_MEDIANO_ANCHO,
                alto=constantes.ELEMENTO_MEDIANO_ALTO,
                tamaño_fuente=constantes.F_MEDIANA,
                fuente=constantes.FUENTE_LLAMATIVA,
                color=constantes.ELEMENTO_FONDO_PRINCIPAL,
                radio_borde=constantes.REDONDEO_NORMAL,
                color_texto=constantes.COLOR_TEXTO_PRINCIPAL,
                color_borde=constantes.ELEMENTO_BORDE_SECUNDARIO,
                grosor_borde=constantes.BORDE_PRONUNCIADO,
                color_borde_hover=constantes.ELEMENTO_HOVER_PRINCIPAL,
                color_borde_clicado=constantes.ELEMENTO_CLICADO_PRINCIPAL,
                accion=lambda: acciones.mostrar_menu_nombre_usuario(self,True)
        )
    """fin de las funciones para cantidad jugadores"""

    """funciones para el menu mesa de espera"""
    def Menu_mesa_espera(self):
        x_menu,y_menu = self.centrar(constantes.ANCHO_MENU_MESA_ESPERA,constantes.ALTO_MENU_MESA_ESPERA)
        menu_mesa_espera = Menu(
            self,
            constantes.ANCHO_MENU_MESA_ESPERA,
            constantes.ALTO_MENU_MESA_ESPERA,
            x_menu,
            y_menu,
            constantes.ELEMENTO_FONDO_TERCIARIO,
            constantes.ELEMENTO_BORDE_TERCIARIO,
            constantes.BORDE_PRONUNCIADO,
            constantes.REDONDEO_NORMAL
        )
        
        elemento_texto = self.crear_elementos_mesa_espera(menu_mesa_espera)
        
        # Guardar referencia al elemento de texto para poder actualizarlo
        menu_mesa_espera.elemento_texto_espera = elemento_texto
        self.elementos_creados.append(menu_mesa_espera)
        return menu_mesa_espera
    def crear_elementos_mesa_espera(self,menu_mesa_espera):
        ancho_txt_esperando = constantes.ELEMENTO_GRANDE_ANCHO*1.6
        alto_txt_esperando = constantes.ELEMENTO_MEDIANO_ALTO*2.6
        x_txt_esperando = (constantes.ANCHO_MENU_MESA_ESPERA - ancho_txt_esperando)*(0.5)
        y_txt_esperando = (constantes.ALTO_MENU_MESA_ESPERA - alto_txt_esperando)*(0.5)
        elemento_texto = menu_mesa_espera.crear_elemento(
            Clase=Elemento_texto,
            x=x_txt_esperando,
            y=y_txt_esperando,
            un_juego=self,
            texto=self.texto_menu_mesa_espera(),
            ancho=ancho_txt_esperando,
            alto=alto_txt_esperando,
            tamaño_fuente=constantes.F_GRANDE,
            fuente=constantes.FUENTE_LLAMATIVA,
            color=constantes.ELEMENTO_FONDO_TERCIARIO,
            radio_borde=constantes.REDONDEO_NORMAL,
            color_texto=constantes.COLOR_TEXTO_SECUNDARIO,
            color_borde=constantes.SIN_COLOR,
            grosor_borde=constantes.SIN_BORDE,
            alineacion="izquierda"
        )
        return elemento_texto

    def texto_menu_mesa_espera(self):
        """Genera el texto actualizado para la mesa de espera"""
        jugadores_actuales = len(self.lista_elementos.get("lista_jugadores", []))
        max_esperados = self.lista_elementos.get("cantidad_jugadores", 0)
        nombre_sala = self.lista_elementos.get("nombre_sala", "No definido")
        nombre_creador = self.lista_elementos.get("nombre_creador", "No definido")

        faltan = max(0, max_esperados - jugadores_actuales)
    
        texto = (
            f"NOMBRE DE LA SALA: {nombre_sala}\n"
            f"CREADOR DE LA SALA: {nombre_creador}\n"
            f"JUGADORES CONECTADOS: {jugadores_actuales}/{max_esperados}\n"
            f"ESPERANDO JUGADORES...\nFALTAN: {faltan}"
        )
    
        print(f"Generando texto para mesa de espera:")
        print(f"- Sala: {nombre_sala}")
        print(f"- Creador: {nombre_creador}")
        print(f"- Jugadores: {jugadores_actuales}/{max_esperados}")
        print(f"- Faltan: {faltan}")
    
        return texto

    def actualizar_mesa_espera(self):
        """Actualiza la mesa de espera"""
        print("Actualizando mesa de espera...")
    
        if hasattr(self, "menu_mesa_espera") and self.menu_mesa_espera in self.elementos_creados:
            # Actualizar el texto del elemento existente en lugar de recrear todo
            texto_actualizado = self.texto_menu_mesa_espera()
            print(f"Texto actualizado: {texto_actualizado}")
        
            # Si el menú tiene un elemento de texto, actualizarlo
            if hasattr(self.menu_mesa_espera, 'elemento_texto_espera'):
                self.menu_mesa_espera.elemento_texto_espera.texto = texto_actualizado
                self.menu_mesa_espera.elemento_texto_espera.prepar_texto()  # Re-preparar el texto
                print("✓ Texto del elemento actualizado")
            else:
                # Buscar el elemento de texto en los botones del menú
                for boton in self.menu_mesa_espera.botones:
                    if isinstance(boton, Elemento_texto):
                        boton.texto = texto_actualizado
                        boton.prepar_texto()  # Re-preparar el texto
                        print("✓ Texto del elemento encontrado y actualizado")
                        break
        else:
            print("Menú de mesa de espera no encontrado, creando nuevo...")
            # Crear nuevo menú si no existe
            self.menu_mesa_espera = self.Menu_mesa_espera()
            self.elementos_creados.append(self.menu_mesa_espera)
            acciones.Mostrar_seccion(self, self.menu_mesa_espera)
    """fin de las funciones para la mesa de espera"""
    
    """funciones para el menu de seleccion de salas"""
    def Menu_seleccion_sala(self):
        x_menu, y_menu = self.centrar(constantes.ANCHO_MENU_SELECCION_SALA, constantes.ALTO_MENU_SELECCION_SALA)
    
        menu_seleccion_sala = Menu(
        self,
        constantes.ANCHO_MENU_SELECCION_SALA,
        constantes.ALTO_MENU_SELECCION_SALA,
        x_menu,
        y_menu,
        constantes.ELEMENTO_FONDO_SECUNDARO,
        constantes.ELEMENTO_BORDE_SECUNDARIO,
        constantes.BORDE_PRONUNCIADO,
        constantes.REDONDEO_PRONUNCIADO
        )
    
    # Título del menú
        menu_seleccion_sala.crear_elemento(
        Clase=Elemento_texto,
        x=(constantes.ANCHO_MENU_SELECCION_SALA - constantes.ELEMENTO_GRANDE_ANCHO*1.5) * 0.5,
        y=(constantes.ALTO_MENU_SELECCION_SALA - constantes.ELEMENTO_MEDIANO_ALTO) * 0.05,
        un_juego=self,
        texto="ELIJA LA SALA",
        ancho=constantes.ELEMENTO_GRANDE_ANCHO*1.5,
        alto=constantes.ELEMENTO_MEDIANO_ALTO,
        tamaño_fuente=constantes.F_GRANDE,
        fuente=constantes.FUENTE_LLAMATIVA,
        color=constantes.ELEMENTO_FONDO_PRINCIPAL,
        radio_borde=constantes.REDONDEO_NORMAL,
        color_texto=constantes.COLOR_TEXTO_PRINCIPAL,
        color_borde=constantes.ELEMENTO_BORDE_SECUNDARIO,
        grosor_borde=constantes.BORDE_INTERMEDIO,
    )
    
    # Obtener salas disponibles
        salas_disponibles = self.lista_elementos["salas_disponibles"]
    
    # Si no hay salas disponibles, mostrar mensaje
        if not salas_disponibles:
            menu_seleccion_sala.crear_elemento(
            Clase=Elemento_texto,
            x=(constantes.ANCHO_MENU_SELECCION_SALA - constantes.ELEMENTO_GRANDE_ANCHO) * 0.5,
            y=(constantes.ALTO_MENU_SELECCION_SALA - constantes.ELEMENTO_MEDIANO_ALTO) * 0.5,
            un_juego=self,
            texto="No hay salas disponibles\nVuelva a intentar más tarde",
            ancho=constantes.ELEMENTO_GRANDE_ANCHO,
            alto=constantes.ELEMENTO_MEDIANO_ALTO,
            tamaño_fuente=constantes.F_MEDIANA,
            fuente=constantes.FUENTE_ESTANDAR,
            color=constantes.ELEMENTO_FONDO_PRINCIPAL,
            radio_borde=constantes.REDONDEO_NORMAL,
            color_texto=constantes.COLOR_TEXTO_PRINCIPAL,
            color_borde=constantes.ELEMENTO_BORDE_SECUNDARIO,
            grosor_borde=constantes.BORDE_INTERMEDIO,
        )
        else:
        # Crear botones para cada sala
            self.crear_botones_salas(menu_seleccion_sala, salas_disponibles)
    
    # Agregar botones de control
        self.agregar_botones_control_salas(menu_seleccion_sala)
    
        self.elementos_creados.append(menu_seleccion_sala)
        return menu_seleccion_sala
    def crear_botones_salas(self, menu, salas):
        """Crea botones para las salas disponibles"""
        grupo_salas = []
        columnas = 3
        espaciado_x = constantes.ANCHO_MENU_SELECCION_SALA * 0.05
        espaciado_y = constantes.ALTO_MENU_SELECCION_SALA * 0.05
    
        ancho_boton = (constantes.ELEMENTO_PEQUENO_ANCHO)*0.9
        alto_boton = constantes.ELEMENTO_PEQUENO_ALTO

        for i, sala in enumerate(salas):
            fila = i // columnas
            columna = i % columnas
        
            x_pos = espaciado_x + columna * (ancho_boton + espaciado_x)
            y_pos = constantes.ALTO_MENU_SELECCION_SALA * 0.2 + fila * (alto_boton + espaciado_y)
        
            # Verificar si la sala está llena
            sala_llena = sala["jugadores"] >= sala["max_jugadores"]
        
            # Crear el texto del boton
            texto_sala = f"{sala['nombre']}/{sala['jugadores']}/{sala['max_jugadores']}"
        
            menu.crear_elemento(
                Clase=BotonRadio,
                x=x_pos,
                y=y_pos,
                un_juego=self,
                texto=texto_sala,
                ancho=ancho_boton,
                alto=alto_boton,
                tamaño_fuente=constantes.F_MEDIANA,
                fuente=constantes.FUENTE_ESTANDAR,
                color=constantes.ELEMENTO_FONDO_PRINCIPAL,
                radio_borde=constantes.REDONDEO_NORMAL,
                color_texto=constantes.COLOR_TEXTO_PRINCIPAL,
                color_borde=constantes.ELEMENTO_BORDE_SECUNDARIO,
                grosor_borde=constantes.BORDE_LIGERO,
                color_borde_hover=constantes.ELEMENTO_HOVER_PRINCIPAL,
                color_borde_clicado=constantes.ELEMENTO_CLICADO_PRINCIPAL,
                grupo=grupo_salas,
                valor=sala,
                deshabilitado=sala_llena
            )
            grupo_salas.append(menu.botones[-1])
    def agregar_botones_control_salas(self, menu):
        """Agrega botones de control (Volver, Actualizar, Confirmar)"""
        x_volver = (constantes.ANCHO_MENU_SELECCION_SALA - constantes.ELEMENTO_PEQUENO_ANCHO) * 0.05
        y_volver = (constantes.ALTO_MENU_SELECCION_SALA - constantes.ELEMENTO_MEDIANO_ALTO) * 0.9
        # Botón Volver
        menu.crear_elemento(
            Clase=Boton,
            x=x_volver,
            y=y_volver,
            un_juego=self,
            texto="VOLVER",
            ancho=constantes.ELEMENTO_PEQUENO_ANCHO,
            alto=constantes.ELEMENTO_MEDIANO_ALTO,
            tamaño_fuente=constantes.F_MEDIANA,
            fuente=constantes.FUENTE_LLAMATIVA,
            color=constantes.ELEMENTO_FONDO_PRINCIPAL,
            radio_borde=constantes.REDONDEO_NORMAL,
            color_texto=constantes.COLOR_TEXTO_PRINCIPAL,
            color_borde=constantes.ELEMENTO_BORDE_SECUNDARIO,
            grosor_borde=constantes.BORDE_PRONUNCIADO,
            color_borde_hover=constantes.ELEMENTO_HOVER_PRINCIPAL,
            color_borde_clicado=constantes.ELEMENTO_CLICADO_PRINCIPAL,
            accion=lambda: acciones.Mostrar_seccion(self, self.menu_nombre_usuario)
        )
    
    # Botón Actualizar
        menu.crear_elemento(
            Clase=Boton,
            x=(constantes.ANCHO_MENU_SELECCION_SALA - constantes.ELEMENTO_PEQUENO_ANCHO) * 0.5,
            y=y_volver,
            un_juego=self,
            texto="ACTUALIZAR",
            ancho=constantes.ELEMENTO_PEQUENO_ANCHO,
            alto=constantes.ELEMENTO_MEDIANO_ALTO,
            tamaño_fuente=constantes.F_MEDIANA,
            fuente=constantes.FUENTE_LLAMATIVA,
            color=constantes.ELEMENTO_FONDO_PRINCIPAL,
            radio_borde=constantes.REDONDEO_NORMAL,
            color_texto=constantes.COLOR_TEXTO_PRINCIPAL,
            color_borde=constantes.ELEMENTO_BORDE_SECUNDARIO,
            grosor_borde=constantes.BORDE_PRONUNCIADO,
            color_borde_hover=constantes.ELEMENTO_HOVER_PRINCIPAL,
            color_borde_clicado=constantes.ELEMENTO_CLICADO_PRINCIPAL,
            accion=lambda: self.actualizar_lista_salas()
        )
    
    # Botón Confirmar
        menu.crear_elemento(
            Clase=Boton,
            x=(constantes.ANCHO_MENU_SELECCION_SALA - constantes.ELEMENTO_PEQUENO_ANCHO) * 0.95,
            y=y_volver,
            un_juego=self,
            texto="CONFIRMAR",
            ancho=constantes.ELEMENTO_PEQUENO_ANCHO,
            alto=constantes.ELEMENTO_MEDIANO_ALTO,
            tamaño_fuente=constantes.F_MEDIANA,
            fuente=constantes.FUENTE_LLAMATIVA,
            color=constantes.ELEMENTO_FONDO_PRINCIPAL,
            radio_borde=constantes.REDONDEO_NORMAL,
            color_texto=constantes.COLOR_TEXTO_PRINCIPAL,
            color_borde=constantes.ELEMENTO_BORDE_SECUNDARIO,
            grosor_borde=constantes.BORDE_PRONUNCIADO,
            color_borde_hover=constantes.ELEMENTO_HOVER_PRINCIPAL,
            color_borde_clicado=constantes.ELEMENTO_CLICADO_PRINCIPAL,
            accion=lambda: acciones.Unirse_a_sala_seleccionada(self, menu)
        )

    def actualizar_lista_salas(self):
        """Actualiza la lista de salas disponibles"""
        print("Actualizando lista de salas...")
        # Remover el menú actual
        if hasattr(self, "menu_seleccion_sala") and self.menu_seleccion_sala in self.elementos_creados:
            self.elementos_creados.remove(self.menu_seleccion_sala)
    
        # Crear nuevo menú con salas actualizadas
        self.menu_seleccion_sala = self.Menu_seleccion_sala()
        acciones.Mostrar_seccion(self, self.menu_seleccion_sala)
    """fin de las funciones para menu sala"""

    """Boton de salir del juego"""
    def salir(self):
        pygame.quit()
        sys.exit()

    """Funciones auxiliares para el ciclo principal del juego"""
    def ejecutar_manejo_eventos(self, evento):
        if self.cartel_alerta.manejar_evento(evento):
            return
        

        self.boton_jugar.manejar_evento(evento)

        
    
        # Verificar existencia antes de acceder
        menus = [
            self.menu_seleccion_sala, 
            self.menu_instrucciones, 
            self.menu_inicio, 
            self.menu_Cantidad_Jugadores
        ]
    
        for menu in menus:
            menu.manejar_eventos(evento)

        # Menús condicionales
        conditional_menus = [
            "menu_mesa_espera", 
            "menu_nombre_creador", 
            "menu_nombre_usuario", 
            "menu_seleccion_sala"
        ]
    
        for menu_name in conditional_menus:
            if hasattr(self, menu_name):
                getattr(self, menu_name).manejar_eventos(evento)

    def ejecutar_verificacion_hovers(self, posicion_raton):
        self.cartel_alerta.verificar_hover(posicion_raton)
        self.boton_jugar.verificar_hover(posicion_raton)
    
        # Menús principales
        main_menus = [
            self.menu_instrucciones, 
            self.menu_inicio, 
            self.menu_Cantidad_Jugadores
        ]
    
        for menu in main_menus:
            if menu:
                menu.verificar_hovers(posicion_raton)
    
        # Menús condicionales
        conditional_menus = [
            "menu_mesa_espera", 
            "menu_nombre_creador", 
            "menu_nombre_usuario", 
            "menu_seleccion_sala"
        ]
    
        for menu_name in conditional_menus:
            if hasattr(self, menu_name):
                getattr(self, menu_name).verificar_hovers(posicion_raton)

    def ejecutar_dibujado(self):
        self.pantalla.fill(constantes.FONDO_VENTANA)
        
        self.boton_jugar.dibujar()
        self.menu_instrucciones.dibujar_menu()
        self.menu_inicio.dibujar_menu()
        self.menu_Cantidad_Jugadores.dibujar_menu()
        self.menu_seleccion_sala.dibujar_menu()
        
        if hasattr(self, "menu_mesa_espera"):
            self.menu_mesa_espera.dibujar_menu()
        
        if hasattr(self, "menu_nombre_creador"):
            self.menu_nombre_creador.dibujar_menu()
        if hasattr(self, "menu_nombre_usuario"):
            self.menu_nombre_usuario.dibujar_menu()
        if hasattr(self, "menu_seleccion_sala"):
            self.menu_seleccion_sala.dibujar_menu()

        self.cartel_alerta.dibujar()
        
    def Correr_juego(self):
        ejecutar = True
        while ejecutar:
            posicion_raton = pygame.mouse.get_pos()
            eventos = pygame.event.get()

            # actualizar hover con la posición actual del ratón
            self.ejecutar_verificacion_hovers(posicion_raton)

            # ahora procesar eventos
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    acciones.Salir()
                    ejecutar = False
                if evento.type == constantes.EVENTO_NUEVO_JUGADOR:
                    self.actualizar_mesa_espera()
                if evento.type == constantes.EVENTO_SALAS_ENCONTRADAS:
                    self.lista_elementos["salas_disponibles"] = evento.salas
                self.ejecutar_manejo_eventos(evento)

            
            self.pantalla.fill(constantes.FONDO_VENTANA)

            self.ejecutar_dibujado()

            pygame.display.flip()
            self.clock.tick(constantes.FPS)
        pygame.quit()

ventana = Ventana()
ventana.Correr_juego()