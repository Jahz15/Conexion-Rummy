import pygame
import sys

import constantes
import acciones
from  elementos_de_interfaz_de_usuario import Elemento_texto,Boton,BotonRadio, EntradaTexto
from menu import Menu

"""Clase ventana donde estaran todos los diseños e interacciones"""
class Ventana:
    """Inicializar pygame, fuentes, crear pantalla, nombre de la misma, cargar imagenes, crear menus y botones"""
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.pantalla = pygame.display.set_mode((constantes.ANCHO_VENTANA,constantes.ALTO_VENTANA))
        pygame.display.set_caption("Rummy500")

        # Datos de juego
        self.lista_elementos = {
            "cantidad_jugadores":0,
            "nombre_creador":"",
            "nombre_sala":"",
            "nombre_unirse":""
        }

        self.elementos_creados = []

        # Logo
        self.logo_rummy = pygame.image.load("assets//Imagenes//Logos//Logo(1).png")

        # Menús iniciales
        self.menu_instrucciones = self.Menu_instrucciones()
        self.menu_inicio = self.Menu_inicio()
        self.boton_jugar = self.Boton_jugar()
        self.menu_Cantidad_Jugadores = self.Menu_Cantidad_Jugadores()
        # self.menu_mesa_espera = self.Menu_mesa_espera()

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

    """Funcion que crea el menu de instrucciones usan ElementoTexto"""
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

        self.elementos_creados.append(menu_instrucciones)
        return menu_instrucciones
    def mostrar_menu_nombre_usuario(self, creador=False):
        if creador:
            if not hasattr(self, "menu_nombre_creador"):
                self.menu_nombre_creador = self.Menu_nombre_usuario(True)
            acciones.Confirmar_cantidad_jugadores(self,self.menu_nombre_creador,self.menu_Cantidad_Jugadores)
        else:
            if not hasattr(self, "menu_nombre_usuario"):
                self.menu_nombre_usuario = self.Menu_nombre_usuario(False)
            acciones.Mostrar_seccion(self, self.menu_nombre_usuario)

    """Se define el menu nombre de usuario, depende de si es el creador o es solamente un participante ejecuta una cosa u otra"""
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
                    grupo=grupos_elementos_entrada
                )
                grupos_elementos_entrada.append(menu_nombre_usuario.botones[-1])
        texto_botones = ("VOLVER","CONFIRMAR")
        crear_sevidor = None
        if not creador_sala: 
            mostrar = self.menu_inicio
            unirse_servidor = lambda: (print("Uniendose al servidor"),acciones.Unirse_sala(self,menu_nombre_usuario))
            accion_confirmar = unirse_servidor
        else:
            mostrar = self.menu_Cantidad_Jugadores
            crear_sevidor = lambda: (print("Ejecutando crear_sevidor"), self.mostrar_menu_mesa_espera())[1]
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
        self.elementos_creados.append(menu_nombre_usuario)
        return menu_nombre_usuario
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
        #Creacion de cada boton por cada elemento de texto_menu_inicio(acompañado de sus acciones)
        texto_menu_inicio = ("CREAR SALA","UNIRSE A LA SALA","COMO JUGAR","SALIR DEL JUEGO")
        funciones_menu_inicio = (
            lambda: acciones.Mostrar_seccion(self, self.menu_Cantidad_Jugadores), 
            lambda: self.mostrar_menu_nombre_usuario(False),   # ← unirse
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
        posicion_logo = (constantes.ANCHO_MENU_I*0.05,constantes.ALTO_MENU_I*0.1)
        menu_inicio.agregar_imagen(self.logo_rummy,posicion_logo,constantes.SCALA)
        self.elementos_creados.append(menu_inicio)
        return menu_inicio

    """Menu cantidad de jugadores, pide los jugadores(6 botones tipo radio,2 botones normales)"""
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
                valor=(i+2)
            )
            # Agregamos el ultimo boton creado al grupo
            botones_radio.append(menu_cantidad.botones[-1])

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
                accion=lambda: self.mostrar_menu_nombre_usuario(True)

        )
        self.elementos_creados.append(menu_cantidad)
        return menu_cantidad
    # en Ventana
    def mostrar_menu_mesa_espera(self):
        # asegurarnos de tener inputs
        acciones.Crear_sevidor(self, self.menu_nombre_creador)
        # (re)crear el menú ahora que lista_elementos ya está actualizada
        self.menu_mesa_espera = self.Menu_mesa_espera()
        acciones.Mostrar_seccion(self, self.menu_mesa_espera)

        # acciones.(self,self.menu_nombre_creador,self.menu_Cantidad_Jugadores)
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
        ancho_txt_esperando = constantes.ELEMENTO_GRANDE_ANCHO*1.6
        alto_txt_esperando = constantes.ELEMENTO_MEDIANO_ALTO*2.6
        x_txt_esperando = (constantes.ANCHO_MENU_MESA_ESPERA - ancho_txt_esperando)*(0.5)
        y_txt_esperando = (constantes.ALTO_MENU_MESA_ESPERA - alto_txt_esperando)*(0.5)
        menu_mesa_espera.crear_elemento(
            Clase=Elemento_texto,
            x=x_txt_esperando,
            y=y_txt_esperando,
            un_juego=self,
            texto=f"NOMBRE DE LA SALA: {self.lista_elementos['nombre_sala']}\nCREADOR DE LA SALA: {self.lista_elementos['nombre_creador']}\nESPERANDO JUGADORES...\nFALTAN: {self.lista_elementos['cantidad_jugadores']}",
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
        self.elementos_creados.append(menu_mesa_espera)
        return menu_mesa_espera
    """Boton de salir del juego"""
    def salir(self):
        pygame.quit()
        sys.exit()

    """Funciones auxiliares para el ciclo principal del juego"""
    def ejecutar_manejo_eventos(self, evento):
        self.boton_jugar.manejar_evento(evento)

        self.menu_instrucciones.manejar_eventos(evento)
        self.menu_inicio.manejar_eventos(evento)
        self.menu_Cantidad_Jugadores.manejar_eventos(evento)
        if hasattr(self, "menu_mesa_espera"):
            self.menu_mesa_espera.manejar_eventos(evento)
        
        if hasattr(self, "menu_nombre_creador"):
            self.menu_nombre_creador.manejar_eventos(evento)
        if hasattr(self, "menu_nombre_usuario"):
            self.menu_nombre_usuario.manejar_eventos(evento)

    def ejecutar_verificacion_hovers(self, posicion_raton):
        self.boton_jugar.verificar_hover(posicion_raton)
        self.menu_instrucciones.verificar_hovers(posicion_raton)
        self.menu_inicio.verificar_hovers(posicion_raton)
        self.menu_Cantidad_Jugadores.verificar_hovers(posicion_raton)
        
        if hasattr(self, "menu_mesa_espera"):
            self.menu_mesa_espera.verificar_hovers(posicion_raton)

        if hasattr(self, "menu_nombre_creador"):
            self.menu_nombre_creador.verificar_hovers(posicion_raton)
        if hasattr(self, "menu_nombre_usuario"):
            self.menu_nombre_usuario.verificar_hovers(posicion_raton)

    def ejecutar_dibujado(self):
        self.boton_jugar.dibujar()
        self.menu_instrucciones.dibujar_menu()
        self.menu_inicio.dibujar_menu()
        self.menu_Cantidad_Jugadores.dibujar_menu()
        
        if hasattr(self, "menu_mesa_espera"):
            self.menu_mesa_espera.dibujar_menu()
        
        if hasattr(self, "menu_nombre_creador"):
            self.menu_nombre_creador.dibujar_menu()
        if hasattr(self, "menu_nombre_usuario"):
            self.menu_nombre_usuario.dibujar_menu()

        
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
                self.ejecutar_manejo_eventos(evento)

            
            self.pantalla.fill(constantes.FONDO_VENTANA)

            self.ejecutar_dibujado()

            pygame.display.flip()
            self.clock.tick(constantes.FPS)
        pygame.quit()

ventana = Ventana()
ventana.Correr_juego()