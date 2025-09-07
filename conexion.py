import socket
import threading
import json
import time

class conexion_Rummy:
    def __init__(self,max_jugadores=7):
        self.puerto = 5555
        self.ejecutandose = False
        self.candado = threading.RLock()

        # Host
        self.max_jugadores = max_jugadores
        self.socket_servidor = None
        self.clientes = []
        self.cola_mensajes = []
        self.estado_juego = None
        self.nombre_partida = None
        self.id_jugador_enviador = None  # Atributo para el ID del jugador que envía mensajes

        # Cliente
        self.socket_cliente = None
        self.conectado = False
        self.id_jugador = None
        self.hilo_recepcion = None
        self.conexiones_disponibles = []
        self.jugadores_desconectados = {}  # Nuevo: almacena datos de jugadores desconectados

        # eventos 
        self.eventos_conexion = []

    #----------------------
    # En caso de ser el Host
    #----------------------

    def iniciar_servidor(self, nombre_sala="Sala1"):
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind(('0.0.0.0', self.puerto))
        self.socket_servidor.listen(self.max_jugadores)
        self.ejecutandose = True
        hilo_servidor = threading.Thread(target=self.aceptar_conexiones)
        hilo_servidor.daemon = True
        hilo_servidor.start()

        hilo_anuncio = threading.Thread(target=self.anunciar_servidor)
        hilo_anuncio.daemon = True
        hilo_anuncio.start()

        hilo_procesar = threading.Thread(target=self._procesar_mensajes)
        hilo_procesar.daemon = True
        hilo_procesar.start()


        print(f"Servidor iniciado en el puerto {self.puerto}, esperando jugadores...")
    
    def aceptar_conexiones(self):
        while self.ejecutandose:
            try:
                #Limitar el número de clientes activos
                with self.candado:
                    jugadores_conectados = len(self.clientes)
                if jugadores_conectados >= self.max_jugadores:
                    print("Sala llena, no se aceptan más conexiones.")
                    time.sleep(1)
                    continue
                socket_cliente, addr = self.socket_servidor.accept()
                with self.candado:
                    print(f"Cliente conectado desde {addr}")
                    id_jugador = len(self.clientes)+1
                    # Añadir el cliente a la lista
                    manejador_cliente = threading.Thread(target=self._manejar_cliente, args=(socket_cliente, id_jugador))
                    manejador_cliente.daemon = True
                    manejador_cliente.start()
                    print(f"Cliente asignado ID {id_jugador}")
            except Exception as e:
                if self.ejecutandose:
                    print(f"Error al aceptar conexiones: {e}")
    
    def _manejar_cliente(self, socket_cliente, id_jugador):
        try:
            while self.ejecutandose:
                data = socket_cliente.recv(4096)
                if not data:
                    break

                mensaje = json.loads(data.decode('utf-8'))
                nombre_jugador = mensaje.get('nombre', f'Jugador{id_jugador}')
                with self.candado:
                    self.cola_mensajes.append((id_jugador, mensaje))
                    
                    if mensaje.get('type') == 'ClienteDesconectado':
                        print(f"Mensaje del cliente: {mensaje}")
                        # Guardar datos del jugador desconectado
                        self.jugadores_desconectados[id_jugador] = {
                            'estado_juego': self.estado_juego,
                            'nombre': self.clientes[id_jugador-1]['nombre'] if id_jugador-1 < len(self.clientes) else nombre_jugador
                        }
                        self.difundir({
                            'type': 'JugadorDesconectado',
                            'id_jugador': id_jugador,
                            'TotalJugadores': len(self.clientes)
                        })
                        self._eliminar_cliente(id_jugador)
                        print(self.jugadores_desconectados)
                        break
                    if mensaje.get('type') == 'Reconectar':
                        # Procesar reconexión
                        id_jugador_reconectar = mensaje.get('id_jugador')
                        datos_guardados = self.jugadores_desconectados.get(id_jugador_reconectar)
                        if datos_guardados:
                            # Reasignar el mismo ID y restaurar datos
                                self.clientes.append({
                                    'socket': socket_cliente,
                                    'id': id_jugador_reconectar,
                                    'nombre': datos_guardados['nombre'],
                                    'thread': threading.current_thread()
                                })

                                self.enviar_a_cliente(id_jugador_reconectar, {
                                    'type': 'Reconectado',
                                    'id_jugador': id_jugador_reconectar,
                                    'estado_juego': datos_guardados['estado_juego'],
                                    'nombre': datos_guardados['nombre']
                                })
                                del self.jugadores_desconectados[id_jugador_reconectar]
                                # Difundir la reconexión a otros jugadores
                                self.difundir({
                                    'type': 'JugadorReconectado',
                                    'id_jugador': id_jugador_reconectar,
                                    'nombre': datos_guardados['nombre']
                                })
                        else: # Mensaje no es 'Reconectar'
                                    id_jugador = len(self.clientes) +len(self.jugadores_desconectados) + 1 
                                    self.clientes.append({
                                        'socket': socket_cliente,
                                        'id': id_jugador,
                                        'nombre': mensaje.get('nombre'),
                                        'thread': threading.current_thread()
                                    })
                                    self.enviar_a_cliente(id_jugador, {
                                        'type': 'Bienvenido',
                                        'id_jugador': id_jugador,
                                        'nombre': mensaje.get('nombre'),
                                        'game_state': self.estado_juego
                                    })
                                    # Difundir la nueva conexión a otros jugadores
                                    self.difundir({
                                        'type': 'NuevoJugador',
                                        'id_jugador': id_jugador,
                                        'nombre': mensaje.get('nombre'),
                                        'TotalJugadores': len(self.clientes)
                                    })
                        print(self.clientes)

                    if mensaje.get('type') == 'NuevoJugador':
                            print(f"Mensaje del cliente: {mensaje}")
                            id_jugador = len(self.clientes) +len(self.jugadores_desconectados) + 1 
                            self.clientes.append({
                                'socket': socket_cliente,
                                'id': id_jugador,
                                'nombre': mensaje.get('nombre'),
                                'thread': threading.current_thread()
                            })
                            self.enviar_a_cliente(id_jugador, {
                                'type': 'Bienvenido',
                                'id_jugador': id_jugador,
                                'nombre': mensaje.get('nombre'),
                                'game_state': self.estado_juego
                            })
                            # Difundir la nueva conexión a otros jugadores
                            self.difundir({
                                'type': 'NuevoJugador',
                                'id_jugador': id_jugador,
                                'nombre': mensaje.get('nombre'),
                                'TotalJugadores': len(self.clientes)
                            })
                            break
        except (ConnectionResetError, socket.error) as e:
            print(f"Error con el cliente {id_jugador}: Conexión perdida - {e}")
            print(self.jugadores_desconectados)
        finally:
                pass

    def guardar_nombre_local(self, nombre):
        try:
            with open("nombre_jugador.txt", "w", encoding="utf-8") as f:
                f.write(nombre)
        except Exception as e:
            print(f"Error al guardar el nombre local: {e}")

    def cargar_nombre_local(self):
        try:
            with open("nombre_jugador.txt", "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            return None
        
    def _enviar_mensajes(self,id_jugador_origen,mensaje):
        print("Mensaje de parte de{id_jugador_origen}:{mensaje}")

        if mensaje.get('type') == 'chat_message':
            # Añadir información sobre el remitente
            mensaje['sender_id'] = id_jugador_origen
            # Reenviar el mensaje a todos los demás clientes
            self.difundir(mensaje)

    def _eliminar_cliente(self, id_jugador):
        with self.candado:
            clientes_a_eliminar = [c for c in self.clientes if c['id'] == id_jugador]
            for cliente in clientes_a_eliminar:
                try:
                    cliente['socket'].shutdown(socket.SHUT_RDWR)
                    cliente['socket'].close()
                except Exception as e:
                    print(f"Error cerrando socket de cliente {id_jugador}: {e}")
            # Elimina fuera del bucle
            self.clientes = [c for c in self.clientes if c['id'] != id_jugador]
            self.difundir({
                'type': 'JugadorDesconectado',
                'id_jugador': id_jugador,
                'TotalJugadores': len(self.clientes)
            })

    def difundir(self, mensaje):
        for cliente in self.clientes:
            if cliente['id'] != mensaje.get('id_jugador'):
                try: 
                    cliente['socket'].send((json.dumps(mensaje) + '\n').encode('utf-8'))
                except Exception as e:
                    print(f"Error al enviar mensaje al cliente {cliente['id']}: {e}")
            

    def enviar_a_cliente(self, id_jugador, mensaje):
        for cliente in self.clientes:
            if cliente['id'] == id_jugador:
                try:
                    cliente['socket'].sendall((json.dumps(mensaje) + '\n').encode('utf-8'))
                except Exception as e:
                    print(f"Error al enviar mensaje al cliente {id_jugador}: {e}")
                    print(self.jugadores_desconectados)
    def anunciar_servidor(self):
        socket_anuncio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_anuncio.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        socket_anuncio.settimeout(1)

        mensaje = json.dumps({
            'type': 'RummyServer',
            'port': self.puerto,
            'partida': self.nombre_partida,
            'host': getattr(self, 'nombre_host', 'Host'),
            'id_jugadores_desconectados': self.jugadores_desconectados
        }).encode('utf-8')
        try:
            while self.ejecutandose:
                socket_anuncio.sendto(mensaje, ('255.255.255.255', 5556)) # Puerto diferente al de conexión
                time.sleep(5) # Anunciarse cada 5 segundos
        except Exception as e:
            print(f"Error en el anuncio del servidor: {e}")
        finally:
            socket_anuncio.close()      

    def _procesar_mensajes(self):
        while self.ejecutandose:
            id_jugador = None
            mensaje = None
            with self.candado:
                if self.cola_mensajes:
                    id_jugador, mensaje = self.cola_mensajes.pop(0)
            if mensaje is not None:
                # Manejar el mensaje aquí
                if mensaje.get('type') == 'NuevoJugador1':
                    print(f"Nuevo jugador conectado: ID {mensaje['id_jugador']}, Total jugadores: {mensaje['TotalJugadores']}")
            
            


    #----------------------
    # En caso de ser Cliente
    #----------------------

    def conectar_a_servidor(self, ip_servidor, id_jugador_reconectar=None, nombre_jugador=None):
        try:
            print(f"Conectado al servidor en {ip_servidor}:{self.puerto}")
            self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_cliente.connect((ip_servidor, self.puerto))
            self.conectado = True
            print("Enviando mensaje de conexión...")
            if id_jugador_reconectar is not None:
                mensaje = {
                        'type': 'Reconectar',
                        'id_jugador': id_jugador_reconectar,
                        'nombre': nombre_jugador
                    }
            else:
                mensaje = {
                    'type': 'NuevoJugador',
                    'nombre': nombre_jugador
                }
            print(f"Mensaje enviado: {mensaje}")    
            self.socket_cliente.sendall((json.dumps(mensaje) + '\n').encode('utf-8'))
            self.hilo_recepcion = threading.Thread(target=self._recibir_mensajes)
            self.hilo_recepcion.daemon = True
            self.hilo_recepcion.start()
            return True
        except Exception as e:
            print(f"Error al conectar al servidor: {e}")
            return False

    def guardar_id_local(self):
        if self.id_jugador is not None:
            try:
                with open("id_jugador.txt", "w") as f:
                    f.write(str(self.id_jugador))
            except Exception as e:
                print(f"Error guardando el ID local: {e}")
    
    def cargar_id_local(self):
        try:
            with open("id_jugador.txt", "r") as f:
                self.id_jugador = int(f.read().strip())
                print(f"ID de jugador cargado localmente: {self.id_jugador}")
                return self.id_jugador
        except Exception:
            return None
            
    def _recibir_mensajes(self):
        buffer = ""
        while self.conectado:
            try:
                data = self.socket_cliente.recv(4096)
                buffer += data.decode('utf-8')
                while '\n' in buffer:
                    mensaje_str, buffer = buffer.split('\n', 1)
                    if mensaje_str.strip():
                        mensaje = json.loads(mensaje_str)
                        self._manejo_mensaje_red(mensaje)
                        
            except Exception as e:
                print(f"Error al recibir mensaje del servidor: {e}")
                self.conectado = False
                # Intentar reconexión automática
                if self.id_jugador is not None and self.socket_cliente is not None:
                    ip_servidor = self.socket_cliente.getpeername()[0]
                    self.intentar_reconexion(ip_servidor)
                break
    
    def _manejo_mensaje_red(self, mensaje):
        if mensaje['type'] == 'Bienvenido':
            self.id_jugador = mensaje['id_jugador']
            self.guardar_id_local()  # Guarda el ID localmente
            nombre = mensaje.get('nombre')
            print(f'ID:{self.id_jugador} - Nombre: {nombre}')
            self.estado_juego = mensaje.get('game_state', None)
        elif mensaje['type'] == 'Reconectado':
            self.id_jugador = mensaje['id_jugador']
            self.guardar_id_local()  # Guarda el ID localmente
            self.estado_juego = mensaje.get('estado_juego', None)
            print(f"Reconectado como {mensaje.get('nombre')}, estado restaurado.")
        elif mensaje['type'] == 'JugadorReconectado':
            print(f"Jugador {mensaje['nombre']} (ID {mensaje['id_jugador']}) se ha reconectado.")
        elif mensaje['type'] == 'game_update':
            self.estado_juego = mensaje.get('game_state', None)
        elif mensaje['type'] == 'NuevoJugador':
            nombre = mensaje.get('nombre')
            print(f"Nuevo jugador conectado: ID {mensaje['id_jugador']} - Nombre: {nombre}, Total jugadores: {mensaje['TotalJugadores']}")
        elif mensaje['type'] == 'JugadorDesconectado':
            print(f"Jugador desconectado: ID {mensaje['id_jugador']}, Total jugadores: {mensaje['TotalJugadores']}")
        elif mensaje['type'] == 'ServidorCerrado':
            print("El servidor ha cerrado la conexión.")
            self.desconectar()

    def desconectar(self):# Cierra todas las conexiones
        self.ejecutandose = False
        self.conectado = False
        # Cerrar servidor
        if self.socket_servidor:
            try:
                self.difundir({
                    'type': 'ServidorCerrado'
                })
            except Exception as e:
                print(f"Error al notificar a cliente sobre el cierre del servidor: {e}")
            self.socket_servidor.close()
            self.socket_servidor = None

        # Cerrar cliente (y notificar al servidor)
        if self.socket_cliente and self.id_jugador is not None:
            try:
                mensaje_desconexion = {
                    'type': 'ClienteDesconectado',
                    'id_jugador': self.id_jugador
                }
                self.socket_cliente.send(json.dumps(mensaje_desconexion).encode('utf-8'))
                time.sleep(0.5)
            except Exception as e:
                print(f"Error al notificar al servidor sobre la desconexión: {e}")
            finally:
                try:
                    self.socket_cliente.shutdown(socket.SHUT_RDWR)
                except Exception:
                    pass
                self.socket_cliente.close()
                self.socket_cliente = None
                self._manejo_mensaje_red({
                    'type': 'JugadorDesconectado',
                    'id_jugador': self.id_jugador,
                    'TotalJugadores': len(self.clientes)
                })
        else:
            print("Socket cliente no existe o ID de jugador no asignado")
            print(f"Socket cliente: {self.socket_cliente}, ID jugador: {self.id_jugador}")

        # Cerrar hilo de recepción del cliente
        if self.hilo_recepcion and threading.current_thread() != self.hilo_recepcion:
            self.hilo_recepcion.join()
        
    def encontrar_ip_servidor(self):
        socket_busqueda = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_busqueda.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_busqueda.bind(('', 5556)) # Escuchar en el mismo puerto que el anuncio
        socket_busqueda.settimeout(5) # Esperar 5 segundos

        print("Buscando servidor en la red...")
        try:
            while True:
                data, direccion_servidor = socket_busqueda.recvfrom(1024)
                mensaje = json.loads(data.decode('utf-8'))
                ip_encontrada = direccion_servidor[0]
                server_completo = []
                self.jugadores_desconectados = mensaje.get('id_jugadores_desconectados', {})
                if mensaje.get('type') == 'RummyServer' and direccion_servidor[0] not in self.conexiones_disponibles:
                    nombre_partida = mensaje.get('partida', 'Desconocida')
                    nombre_host = mensaje.get('host', 'Host')
                    print(f"Servidor encontrado en la IP: {ip_encontrada} - Partida: {nombre_partida} - Host: {nombre_host}")
                    self.conexiones_disponibles.append(ip_encontrada)
                    server_completo.append((ip_encontrada, nombre_partida))
                    print(f"Conexiones disponibles: {self.conexiones_disponibles}")
                else:
                    break
        except socket.timeout:
            if not self.conexiones_disponibles:
                print("Tiempo de búsqueda agotado. Servidor no encontrado.")
            else:
                print("Búsqueda finalizada.")
        except Exception as e:
            print(f"Error buscando servidor: {e}")
        finally:
            socket_busqueda.close()
        return self.conexiones_disponibles if self.conexiones_disponibles else None
    
    def intentar_reconexion(self, ip_servidor, intentos=5, espera=3):
        """
        Intenta reconectar automáticamente al servidor usando el id_jugador anterior.
        """
        # Cargar el ID local antes de intentar reconectar
        id_local = self.cargar_id_local()
        if id_local:
            self.id_jugador = id_local
        for intento in range(intentos):
            print(f"Intentando reconectar... (Intento {intento + 1}/{intentos})")
            exito = self.conectar_a_servidor(ip_servidor, id_jugador_reconectar=self.id_jugador)
            if exito:
                print("Reconexión exitosa.")
                return True
            time.sleep(espera)
        print("No se pudo reconectar después de varios intentos.")
        return False