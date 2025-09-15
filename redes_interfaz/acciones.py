import threading
from redes_interfaz import client_main
from redes_interfaz import server_main
from redes_interfaz import conexion
conexion_Rummy = conexion.conexion_Rummy
"""Metodos de redes(interfaz-redes)"""

"""Agregar un jugador en lista de jugadores de redes, y actualizar la lista de usurios de la interfaz por esa nueva lista"""
server_rummy = None  # servidor, si se crea uno
cliente_rummy = None  # cliente, si se crea uno
def validar_campos_servidor(menu):
    """Valida todos los campos necesarios para crear un servidor"""
    campos_requeridos = {
        'nombre_creador': False,
        'nombre_sala': False
    }
    
    for boton in menu.botones:
        if hasattr(boton, 'valor') and hasattr(boton, 'texto_valido'):
            texto_boton = getattr(boton, 'texto', '').lower()
            
            if "nombre" in texto_boton and "sala" not in texto_boton and boton.texto_valido:
                campos_requeridos['nombre_creador'] = True
            elif "sala" in texto_boton and boton.texto_valido:
                campos_requeridos['nombre_sala'] = True
    
    return all(campos_requeridos.values())

def Crear_servidor(un_juego, menu):

    valor_nombre_creador = None
    valor_nombre_sala = None
    nombre_creador_sala = None
    nombre_sala = None
    max_jugadores = un_juego.lista_elementos.get("cantidad_jugadores")
    campos_validos = True

    campos_entrada = []
    for boton in menu.botones:
        if hasattr(boton, 'valor') and hasattr(boton, 'texto_valido'):
            campos_entrada.append(boton)

    # Asignar valores por posición
    if len(campos_entrada) >= 1:
        campo_nombre = campos_entrada[0]
        nombre_creador_sala = campo_nombre.valor.strip() if campo_nombre.valor else ""
        un_juego.lista_elementos["nombre_creador"] = nombre_creador_sala
        if not campo_nombre.texto_valido:
            campos_validos = False

    if len(campos_entrada) >= 2:
        campo_sala = campos_entrada[1]
        nombre_sala = campo_sala.valor.strip() if campo_sala.valor else ""
        un_juego.lista_elementos["nombre_sala"] = nombre_sala
        if not campo_sala.texto_valido:
            campos_validos = False

    # Validación
    if (campos_validos and 
        nombre_creador_sala and 
        nombre_sala and 
        max_jugadores > 0):
        
        un_juego.lista_elementos = {
            "nombre_creador": nombre_creador_sala,
            "nombre_sala": nombre_sala,
            "cantidad_jugadores": max_jugadores,
            "ip_sala":"127.0.0.1",
            "lista_jugadores": [],
            "nombre_unirse": ""
        }
        print("holaaa")
        Agregar_jugador(un_juego)
        return True
    else:
        if not validar_campos_servidor(menu):
            print("Faltan campos requeridos o no son válidos")
            return False

    #A partir de aqui deberan crear la sala formalmente la sala puede utilizar sala_creada de la lista de elemento de ventana, los elementos del diccionario sala_creada son, sala_creada = {'nombre':'', 'ip':'','jugadores':0, 'max_jugadores': 0}, Como este metodo se llamara directamente despues de pedir los valores de creacion de la sala, pueden aplicar cualquier metodo para crear el servidor. la sala_creada es importante que tengan su variable interna donde tengan guardado esos datos del servidor.

def Crear_partida(un_juego):
    global server_rummy, cliente_rummy
    nombre_creador_sala = un_juego.lista_elementos.get("nombre_creador")
    nombre_sala = un_juego.lista_elementos.get("nombre_sala")
    max_jugadores = un_juego.lista_elementos.get("cantidad_jugadores")
    server_rummy = conexion_Rummy()
    cliente_rummy = conexion_Rummy()
    hilo_server = threading.Thread(
        target=server_main.run_server,
        args=(server_rummy,cliente_rummy,max_jugadores,nombre_creador_sala,nombre_sala,un_juego)
    )
    hilo_server.daemon = True
    hilo_server.start()

def Agregar_jugador(un_juego):
    """
    Agrega un jugador a la lista local del juego.
    """
    lista_elementos = un_juego.lista_elementos
    nombre_creador = lista_elementos["nombre_creador"]
    lista_jugadores = lista_elementos["lista_jugadores"]
    nombre_unirse = lista_elementos["nombre_unirse"]
    # Determinar qué nombre usar
    if lista_elementos:
        if nombre_creador and nombre_creador not in lista_jugadores:
            jugador = nombre_creador
            print(f"Agregando creador: {jugador}")
        elif nombre_unirse and nombre_unirse not in lista_jugadores:
            jugador = nombre_unirse
            print(f"Agregando jugador que se une: {jugador}")
        else:
            print("No se encontro nombre de jugador para agregar")
            return

    # Agregar jugador
    if jugador:
        lista_jugadores.append(jugador)
        print(f"Jugador agregado: {jugador}")
        print(f"Lista actual: {lista_jugadores}")
        
        # FORZAR ACTUALIZACIÓN INMEDIATA
        print("Forzando actualización de mesa de espera...")
        Notificar_cambio_jugadores(un_juego)
    else:
        print(f"Jugador ya existe o es inválido: {jugador}")

    #Actualizar las instancias de clase
    un_juego.lista_elementos = lista_elementos
    un_juego.lista_elementos["nombre_creador"] = nombre_creador
    un_juego.lista_elementos["lista_jugadores"] = lista_jugadores
    un_juego.lista_elementos["nombre_unirse"] = nombre_unirse
    
    # Notificar_cambio_jugadores(un_juego)  # Notifica los cambios y actualiza la mesa

def Obtener_salas_disponibles(un_juego):
    """Obtiene la lista de salas disponibles desde la red"""
    # EJEMPLO - REEMPLAZA CON LÓGICA REAL DE REDes
    salas_ejemplo = [
    {"creador":"Juan","nombre": "Sala 1","lista_jugadores":['Juan','jugador2'], "jugadores": 2, "max_jugadores": 4, "ip": "192.168.1.101"},
    {"creador":"Alejando","nombre": "Sala 2","lista_jugadores":['Alejandro','jugador2'], "jugadores": 1, "max_jugadores": 4, "ip": "192.168.1.102"},
    {"creador":"Maria","nombre": "Sala 3","lista_jugadores":['Maria','jugador2'], "jugadores": 3, "max_jugadores": 4, "ip": "192.168.1.103"},
    {"creador":"Roberto","nombre": "Sala 4","lista_jugadores":['Roberto','jugador2'], "jugadores": 0, "max_jugadores": 4, "ip": "192.168.1.104"},
    {"creador":"Pepe","nombre": "Sala 5","lista_jugadores":['Pepe','jugador2'], "jugadores": 4, "max_jugadores": 4, "ip": "192.168.1.105"},
    {"creador":"Gonzalo","nombre": "Sala 6","lista_jugadores":['Gonzalo','jugador2'], "jugadores": 2, "max_jugadores": 4, "ip": "192.168.1.106"},
    {"creador":"Felipe","nombre": "Sala 7","lista_jugadores":['Felipe','jugador2'], "jugadores": 1, "max_jugadores": 4, "ip": "192.168.1.107"},
    {"creador":"Marta","nombre": "Sala 8","lista_jugadores":['Marta','jugador2'], "jugadores": 3, "max_jugadores": 4, "ip": "192.168.1.108"},
    {"creador":"Diego","nombre": "Sala 9","lista_jugadores":['Diego','jugador2'], "jugadores": 2, "max_jugadores": 4, "ip": "192.168.1.109"},
    ]

    return salas_ejemplo



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

def Datos_unirse_sala(un_juego, menu):
    """Valida las entradas antes de unirse"""
    nombre_valido = True
    for boton in menu.botones:
        # Buscar elementos de entrada por sus atributos (sin importar clases)
        if hasattr(boton, 'valor') and hasattr(boton, 'texto_valido'):
            if not boton.texto_valido:
                nombre_valido = False
                print("Error: Nombre no válido")
                # Mostrar mensaje de error
                if hasattr(boton, 'mostrar_alerta'):
                    boton.mostrar_alerta("¡Nombre no válido! Recuerda no utilizar números o caracteres especiales.")  # Rojo para error
                break
            else:
                if hasattr(boton, 'obtener_texto_validado'):
                    un_juego.lista_elementos["nombre_unirse"] = boton.obtener_texto_validado()
                else:
                    un_juego.lista_elementos["nombre_unirse"] = boton.valor
    
    if nombre_valido:
        if hasattr(un_juego, 'cartel_alerta'):
            un_juego.cartel_alerta.ocultar()

        print("Uniendose al servidor... ")
        print(un_juego.lista_elementos.get("nombre_unirse"), "Te estas uniendo...")
        return True
    else:
        print("Por favor, corrige los errores en el formulario")
        return False
    
def Unirse_a_sala_seleccionada(un_juego, menu_seleccion_sala):
    """Conecta a la sala seleccionada"""
    sala_seleccionada = None
    
    # Buscar la sala seleccionada
    for boton in menu_seleccion_sala.botones:
        if (hasattr(boton, 'seleccionado') and hasattr(boton, 'valor') and boton.seleccionado and hasattr(boton, 'grupo')):  # Los BotonRadio tienen grupo
            sala_seleccionada = boton.valor
            break

    if sala_seleccionada:
        print(f"Conectando a {sala_seleccionada['nombre']}...")
        print(f"IP: {sala_seleccionada.get('ip', 'IP no disponible')}")
        print(f"Jugadores: {sala_seleccionada['jugadores']}/{sala_seleccionada['max_jugadores']}")
        print(f"Lista Jugadores: {sala_seleccionada['lista_jugadores']}")
        print(f"Usuario: {un_juego.lista_elementos.get('nombre_unirse')}")
        
        # Guardar información de la sala seleccionada
        un_juego.lista_elementos["nombre_creador"] = sala_seleccionada["creador"]
        un_juego.lista_elementos["nombre_sala"] = sala_seleccionada["nombre"]
        un_juego.lista_elementos["cantidad_jugadores"] = sala_seleccionada["max_jugadores"]
        un_juego.lista_elementos["ip_sala"] = sala_seleccionada["ip"]
        un_juego.lista_elementos["lista_jugadores"] = sala_seleccionada["lista_jugadores"]
        
        
        #Aqui deberian llamar a la funcion Agregar_jugador, ya que para este punto se conocen los datos de sala a entrar, "sala_seleccionada" definida igual que la "sala_creador"
        Agregar_jugador(un_juego)
        
        # Aquí iría la lógica real de conexión a través de VLAN
        # conectar_a_sala(sala_seleccionada['ip'], un_juego.lista_elementos.get('nombre_unirse'))
        
        # Después de conectar exitosamente, podrías ir a un menú de espera o de juego
        Mostrar_seccion(un_juego, un_juego.menu_mesa_espera)
        
        
    else:
        print("No se ha seleccionado ninguna sala")


def Actualizar_lista_salas(un_juego):
    """Función para actualizar la lista de salas"""
    print("Actualizando lista de salas...")
    # Esta función sería llamada desde el botón Actualizar
    # Deberías implementar la lógica para obtener salas actualizadas de la red

"""Metodos meramente para el control de aparicion de menus"""
def mostrar_menu_nombre_usuario(un_juego, creador=False):
    if creador:
        if not hasattr(un_juego, "menu_nombre_creador"):
            un_juego.menu_nombre_creador = un_juego.Menu_nombre_usuario(True)
        Confirmar_cantidad_jugadores(un_juego,un_juego.menu_nombre_creador,un_juego.menu_Cantidad_Jugadores)
    else:
        if not hasattr(un_juego, "menu_nombre_usuario"):
            un_juego.menu_nombre_usuario = un_juego.Menu_nombre_usuario(False)
        Mostrar_seccion(un_juego, un_juego.menu_nombre_usuario)

def mostrar_menu_mesa_espera(un_juego):
    if hasattr(un_juego, "menu_nombre_creador"):
        Valores_crear_sevidor(un_juego, un_juego.menu_nombre_creador)

    if Crear_servidor(un_juego, un_juego.menu_nombre_creador):
    # (re)crear el menú ahora que lista_elementos ya está actualizada
        un_juego.menu_mesa_espera = un_juego.Menu_mesa_espera()
        Mostrar_seccion(un_juego, un_juego.menu_mesa_espera)

def mostrar_menu_seleccion_sala(un_juego):
    """Muestra el menú de selección de sala"""
    # Crear el menú si no existe
    if not hasattr(un_juego, "menu_seleccion_sala"):
        un_juego.menu_seleccion_sala = un_juego.Menu_seleccion_sala()

    # Mostrar el menú y guardar el nombre del jugador
    Nombre_jugador_unirse(un_juego,un_juego.menu_nombre_usuario)
    Mostrar_seccion(un_juego, un_juego.menu_seleccion_sala)


"""Metodos meramente para las validaciones"""
def validar_y_unirse_sala(un_juego, menu):
    resultado = Datos_unirse_sala(un_juego, menu)
    if resultado == False:
        print("Los datos ingresados no son validos")
    elif resultado == True:
        mostrar_menu_seleccion_sala(un_juego)

def validar_y_crear_servidor(un_juego, menu):
    """Valida y procede a crear servidor"""
    if Crear_servidor(un_juego, menu):
    # Solo crear servidor si la validación fue exitosa
        Crear_partida(un_juego)
        mostrar_menu_mesa_espera(un_juego)

def Salir():
    global cliente_rummy, server_rummy
    if cliente_rummy is not None:
        cliente_rummy.desconectar()
    if server_rummy is not None:
        server_rummy.desconectar()
    else:
        print("No hay cliente o servidor para desconectar.")

def Buscar_salas(un_juego,):
    global hilo_busqueda
    conexion_salas = conexion_Rummy()
    hilo_busqueda = threading.Thread(
        target=conexion_salas.encontrar_ip_servidor,
        args=(un_juego,))
    hilo_busqueda.daemon = True
    hilo_busqueda.start()
    print(conexion_salas.conexiones_disponibles)