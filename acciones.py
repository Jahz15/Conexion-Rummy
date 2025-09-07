import threading
import server_main
import client_main
from conexion import conexion_Rummy
"""Accion que se ejecuta al presionar un boton de la ventana"""
def Mostrar_seccion(un_juego, menu_destino):
    """
    Oculta todos los menús del juego y muestra solo el destino.
    """
    for elemento in un_juego.elementos_creados:
        elemento.ocultar()

    # Mostramos el que queremos
    menu_destino.mostrar()

def Confirmar_cantidad_jugadores(un_juego,menu_destino,menu_ocultar):
    """Recorremos todos los botones del menu, y verificamos que el boton tenga el atributo "valor" y el "seleccionado" con hasattr, luego verificamos si efectivamente el boton esta seleccionado"""
    
    valor_seleccionado = None
    
    for boton in menu_ocultar.botones:
        if hasattr(boton, 'valor') and hasattr(boton, 'seleccionado'):
            if boton.seleccionado:
                un_juego.lista_elementos["cantidad_jugadores"] = boton.valor
                valor_seleccionado = boton.valor

    if valor_seleccionado != None:
        print("Cantidad de jugadores:",un_juego.lista_elementos["cantidad_jugadores"])
    else:
        print("No se ha seleccionado ninguna cantidad de jugadores")
        return
    Mostrar_seccion(un_juego,menu_destino)

def Unirse_sala(un_juego,menu):
    global cliente_rummy
    global server_rummy
    for boton in menu.botones:
        if hasattr(boton,"grupo"):
            if len(boton.grupo) >= 1:
                un_juego.lista_elementos["nombre_unirse"] = boton.grupo[0].valor
    print("Uniendose al servidor... ")
    nombre_cliente = un_juego.lista_elementos.get("nombre_unirse")
    print(nombre_cliente,"Te estas uniendo...")
    cliente_rummy = conexion_Rummy()
    server_rummy = None
    hilo_cliente = threading.Thread(
    target=client_main.run_client,
    args=(cliente_rummy,nombre_cliente,)
    )
    hilo_cliente.daemon = True
    hilo_cliente.start()
def Crear_sevidor(un_juego, menu):
    global server_rummy, cliente_rummy
    valor_nombre_creador = None
    valor_nombre_sala = None

    for boton in menu.botones:
        if hasattr(boton, "grupo") and boton.grupo:
            if len(boton.grupo) >= 1:
                un_juego.lista_elementos["nombre_creador"] = boton.grupo[0].valor
                valor_nombre_creador = boton.grupo[0].valor
            if len(boton.grupo) >= 2:
                un_juego.lista_elementos["nombre_sala"] = boton.grupo[1].valor
                valor_nombre_sala = boton.grupo[1].valor
    server_rummy = conexion_Rummy()
    cliente_rummy = conexion_Rummy()
    cantidad_jugadores = int(un_juego.lista_elementos.get("cantidad_jugadores"))
    nombre_creador = un_juego.lista_elementos.get("nombre_creador")
    nombre_sala = un_juego.lista_elementos.get("nombre_sala")
    hilo_server = threading.Thread(
        target=server_main.run_server,
        args=(server_rummy,cliente_rummy,cantidad_jugadores,nombre_creador,nombre_sala)
    )
    hilo_server.daemon = True
    hilo_server.start()
    seleccionado = True

    if valor_nombre_creador != "" and valor_nombre_sala != "":
        print("Creador:",un_juego.lista_elementos["nombre_creador"])
        print("Sala:",un_juego.lista_elementos["nombre_sala"])
    else:
        print("No se ha seleccionado un creador o un nombre de sala")
        return

def Salir():
    global cliente_rummy, server_rummy
    if cliente_rummy is not None:
        cliente_rummy.desconectar()
    if server_rummy is not None:
        server_rummy.desconectar()
    else:
        print("No hay cliente o servidor para desconectar.")
    