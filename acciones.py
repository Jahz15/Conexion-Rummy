import threading
import threading
import server_main
import client_main
from conexion import conexion_Rummy
"""Metodos de redes(interfaz-redes)"""

"""Agregar un jugador en lista de jugadores de redes, y actualizar la lista de usurios de la interfaz por esa nueva lista"""
server_rummy = None  # servidor, si se crea uno
cliente_rummy = None  # cliente, si se crea uno
def Crear_servidor(un_juego):
    global server_rummy, cliente_rummy
    valor_nombre_creador = None
    valor_nombre_sala = None

    nombre_creador_sala = un_juego.lista_elementos.get("nombre_creador")
    nombre_sala = un_juego.lista_elementos.get("nombre_sala")
    max_jugadores = un_juego.lista_elementos.get("cantidad_jugadores")
    #A partir de aqui deberan crear la sala formalmente la sala puede utilizar sala_creada de la lista de elemento de ventana, los elementos del diccionario sala_creada son, sala_creada = {'nombre':'', 'ip':'','jugadores':0, 'max_jugadores': 0}, Como este metodo se llamara directamente despues de pedir los valores de creacion de la sala, pueden aplicar cualquier metodo para crear el servidor. la sala_creada es importante que tengan su variable interna donde tengan guardado esos datos del servidor.

    server_rummy = conexion_Rummy()
    cliente_rummy = conexion_Rummy()
    hilo_server = threading.Thread(
        target=server_main.run_server,
        args=(server_rummy,cliente_rummy,max_jugadores,nombre_creador_sala,nombre_sala,un_juego)
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



def Agregar_jugador(un_juego):
    """
    Agrega un jugador a la lista local del juego.
    Esto simula que el servidor notificó que alguien entró.
    """
    #Esta logica deben reempalzarla, guarden el valor de 'un_juego.lista_elementos.get('nombre_unirse')' en una variable y agreguenlo a un arreglo interno que tengan para guardar la lista de jugadores, luego ahi si haran un_juego.lista_elementos["lista_jugadores"] = su_lista_interna
    jugador = un_juego.lista_elementos.get("nombre_unirse") #usen este dato y guardenlo en dicha lista interna, podrian llamar alguna funcion de redes, que agregue el valor de jugador a la lista interna
    jugadores = un_juego.lista_elementos.get("lista_jugadores") # aqui seria jugadores = lista_interna_de_redes_con_jugadores
    un_juego.lista_elementos["lista_jugadores"] = jugadores #esto si seria igual
    

    Notificar_cambio_jugadores(un_juego) #Notifica los cambios y actualiza la mesa, se supone que este metodo se aplica en cada ventana de cada jugador, incluyendo el creador del servidor




"""Metodos netamete interfaz(uso de funciones de interfaz-redes)"""

"""Accion que se ejecuta al presionar un boton de la ventana"""
def Mostrar_seccion(un_juego, menu_destino):
    """
    Oculta todos los menús del juego y muestra solo el destino.
    """
    for elemento in un_juego.elementos_creados:
        elemento.ocultar()

    # Mostramos el que queremos
    menu_destino.mostrar()


"""Metodo que obtiene el valor de cantidad de jugadores, al darle confirmar en el menu_cantidad_jugadores en la interfaz"""
def Confirmar_cantidad_jugadores(un_juego,menu_destino,menu_ocultar):
    #Recorremos todos los botones del menu, y verificamos que el boton tenga el atributo "valor" y el "seleccionado" con hasattr, luego verificamos si efectivamente el boton esta seleccionado
    
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

"""Metodo que obtiene el valor de el nombre del creador de la sala y el nombre de su sala"""
def Valores_crear_sevidor(un_juego, menu):
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

    if valor_nombre_creador != "" and valor_nombre_sala != "":
        print("Creador:",un_juego.lista_elementos["nombre_creador"])
        print("Sala:",un_juego.lista_elementos["nombre_sala"])
    else:
        print("No se ha seleccionado un creador o un nombre de sala")
        return

"""Metodo que permite obtener el nombre del jugador a unirse, usado en el boton de menu_inicio (unirse sala)"""
def Nombre_jugador_unirse(un_juego,menu):
    for boton in menu.botones:
        if hasattr(boton,"grupo"):
            if len(boton.grupo) >= 1:
                un_juego.lista_elementos["nombre_unirse"] = boton.grupo[0].valor
    print("Buscando servidores disponibles... ")

def Notificar_cambio_jugadores(un_juego):
    """
    Llama a la actualización de la mesa de espera.
    """
    un_juego.actualizar_mesa_espera()


def Unirse_a_sala_seleccionada(un_juego, menu_seleccion_sala):
    """Conecta a la sala seleccionada"""
    sala_seleccionada = None
    
    # Buscar la sala seleccionada
    for boton in menu_seleccion_sala.botones:
        if (hasattr(boton, 'seleccionado') and 
            hasattr(boton, 'valor') and 
            boton.seleccionado and 
            hasattr(boton, 'grupo')):  # Los BotonRadio tienen grupo
            sala_seleccionada = boton.valor
            break

    if sala_seleccionada:
        print(f"Conectando a {sala_seleccionada['nombre']}...")
        print(f"IP: {sala_seleccionada.get('ip', 'IP no disponible')}")
        print(f"Jugadores: {sala_seleccionada['jugadores']}/{sala_seleccionada['max_jugadores']}")
        print(f"Usuario: {un_juego.lista_elementos.get('nombre_unirse')}")
        
        # Guardar información de la sala seleccionada
        un_juego.lista_elementos["sala_seleccionada"] = sala_seleccionada
        
        #Aqui deberian llamar a la funcion Agregar_jugador, ya que para este punto se conocen los datos de sala a entrar, "sala_seleccionada" definida igual que la "sala_creador"
        Agregar_jugador(un_juego)
        
        # Aquí iría la lógica real de conexión a través de VLAN
        # conectar_a_sala(sala_seleccionada['ip'], un_juego.lista_elementos.get('nombre_unirse'))
        
        # Después de conectar exitosamente, podrías ir a un menú de espera o de juego
        # Mostrar_seccion(un_juego, un_juego.menu_mesa_espera)
        
        
    else:
        print("No se ha seleccionado ninguna sala")

def Actualizar_lista_salas(un_juego):
    """Función para actualizar la lista de salas"""
    print("Actualizando lista de salas...")
    # Esta función sería llamada desde el botón Actualizar
    # Deberías implementar la lógica para obtener salas actualizadas de la red

def Salir():
    global cliente_rummy, server_rummy
    if cliente_rummy is not None:
        cliente_rummy.desconectar()
    if server_rummy is not None:
        server_rummy.desconectar()
    else:
        print("No hay cliente o servidor para desconectar.")

def buscar_salas(un_juego,):
    global hilo_busqueda
    conexion_salas = conexion_Rummy()
    hilo_busqueda = threading.Thread(
        target=conexion_salas.encontrar_ip_servidor,
        args=(un_juego,))
    hilo_busqueda.daemon = True
    hilo_busqueda.start()
    print(conexion_salas.conexiones_disponibles)