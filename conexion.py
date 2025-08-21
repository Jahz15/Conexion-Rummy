import socket
import threading
import json
import time

class conexion_Rummy:
    def __init__(self):
        self.puerto = 5555
        self.ejecutandose = False
        self.candado = threading.Lock()

        # Host
        self.socket_servidor = None
        self.clientes = []
        self.cola_mensajes = []
        self.estado_juego = None
        self.id_jugador_enviador = None  # Atributo para el ID del jugador que envía mensajes

        # Cliente
        self.socket_cliente = None
        self.conectado = False
        self.id_jugador = None
        self.hilo_recepcion = None
    #----------------------
    # En caso de ser el Host
    #----------------------

    def iniciar_servidor(self):  #Método que inicia el servidor
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind(('0.0.0.0', self.puerto))
        self.socket_servidor.listen(7)
        self.ejecutandose = True

        hilo_servidor = threading.Thread(target=self.aceptar_conexiones)
        hilo_servidor.daemon = True
        hilo_servidor.start()

        hilo_anuncio = threading.Thread(target=self.anunciar_servidor)
        hilo_anuncio.daemon = True
        hilo_anuncio.start()

        print(f"Servidor iniciado en el puerto {self.puerto}, esperando jugadores...")
    
    def aceptar_conexiones(self): #Metodo que acepta conexiones de clientes
        while self.ejecutandose:
            try:
                socket_cliente, addr = self.socket_servidor.accept()
                
                with self.candado:
                    id_jugador = len(self.clientes)+1
                    self.id_jugador = id_jugador
                    # Añadir el cliente a la lista
                    manejador_cliente = threading.Thread(target=self._manejar_cliente, args=(socket_cliente, id_jugador))
                    manejador_cliente.daemon = True
                    manejador_cliente.start()

                    self.clientes.append({
                        'socket': socket_cliente,
                        'id': self.id_jugador,
                        'thread': manejador_cliente
                    })

                    # Notificar evento de nueva conexión
                    self.enviar_a_cliente(id_jugador,{
                        'type': 'Bienvenido',
                        'id_jugador': self.id_jugador,
                        'game_state': self.estado_juego
                    })

                    # Notificar a todos
                    self.difundir({
                        'type': 'NuevoJugador',
                        'id_jugador': id_jugador,
                        'TotalJugadores': len(self.clientes)
                    })
            
                print(f"Nuevo jugador conectado desde {addr}, ID asignado: {id_jugador}. Total de jugadores: {len(self.clientes)}")
            except Exception as e:
                if self.ejecutandose:
                    print(f"Error al aceptar conexiones: {e}")
    
    def _manejar_cliente(self, socket_cliente, id_jugador): # Método que maneja la comunicación con un cliente
        try:
            while self.ejecutandose:
                data = socket_cliente.recv(4096)
                if not data:
                    break

                mensaje = json.loads(data.decode('utf-8'))
                with self.candado:
                    self.cola_mensajes.append((id_jugador, mensaje))
                    # La función para procesar mensajes va aquí
                    # self._procesar_mensajes()

        except Exception as e:
            print(f"Error con el cliente {id_jugador}: {e}")
        finally:
            self._eliminar_cliente(id_jugador)

    def _enviar_mensajes(self,id_jugador_origen,mensaje): #Metodo provisional para que un cliente envíe mensajes a todos los clientes
        print("Mensaje de parte de{id_jugador_origen}:{mensaje}")

        if mensaje.get('type') == 'chat_message':
            # Añadir información sobre el remitente
            mensaje['sender_id'] = id_jugador_origen
            # Reenviar el mensaje a todos los demás clientes
            self.difundir(mensaje)

    def _eliminar_cliente(self, id_jugador): # Método que elimina un cliente de la lista
        with self.candado:
            self.clientes = [c for c in self.clientes if c['id'] != id_jugador]
            self.difundir({
                'type': 'JugadorDesconectado',
                'id_jugador': id_jugador,
                'TotalJugadores': len(self.clientes)
            })
    
    def difundir(self, mensaje): # Método que envía un mensaje a todos los clientes conectados
        for cliente in self.clientes:
            try: 
                cliente['socket'].send(json.dumps(mensaje).encode('utf-8'))
            except Exception as e:
                print(f"Error al enviar mensaje al cliente {cliente['id']}: {e}")

    def enviar_a_cliente(self, id_jugador, mensaje): # Método que envía un mensaje a un cliente específico
        for cliente in self.clientes:
            if cliente['id'] == id_jugador:
                try:
                    cliente['socket'].send(json.dumps(mensaje).encode('utf-8'))
                except Exception as e:
                    print(f"Error al enviar mensaje al cliente {cliente['id']}: {e}")
                break

    def anunciar_servidor(self): # Método que anuncia el servidor en la red local
        socket_anuncio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_anuncio.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        socket_anuncio.settimeout(1)

        mensaje = f"RummyServer:{self.puerto}".encode('utf-8')
        try:
            while self.ejecutandose:
                socket_anuncio.sendto(mensaje, ('255.255.255.255', 5556)) # Puerto diferente al de conexión
                time.sleep(5) # Anunciarse cada 5 segundos
        except Exception as e:
            print(f"Error en el anuncio del servidor: {e}")
        finally:
            socket_anuncio.close()      
        
    #----------------------
    # En caso de ser Cliente
    #----------------------

    def conectar_a_servidor(self, ip_servidor): # Método que conecta al cliente a un servidor
        try:
            self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_cliente.connect((ip_servidor, self.puerto))

            self.hilo_recepcion = threading.Thread(target=self._recibir_mensajes)
            self.hilo_recepcion.daemon = True
            self.hilo_recepcion.start()

            self.conectado = True
            return True
        except Exception as e:
            print(f"Error al conectar al servidor: {e}")
            return False
        
    def _recibir_mensajes(self): # Método que recibe mensajes del servidor
        while self.conectado:
            try:
                data = self.socket_cliente.recv(4096)
                if not data:
                    break

                mensaje = json.loads(data.decode('utf-8'))
                self._manejo_mensaje_red(mensaje)
            except Exception as e:
                print(f"Error al recibir mensaje del servidor: {e}")
                self.desconectar()
    
    def _manejo_mensaje_red(self, mensaje): #Método que maneja la información recibida del servidor
        if mensaje['type'] == 'Bienvenido':
            self.id_jugador = mensaje['id_jugador']
            self.estado_juego = mensaje.get('game_state', None)
        elif mensaje['type'] == 'game_update':
            self.estado_juego = mensaje.get('game_state', None)
        elif mensaje['type'] == 'NuevoJugador':
            print(f"Nuevo jugador conectado: ID {mensaje['id_jugador']}, Total jugadores: {mensaje['TotalJugadores']}")
        elif mensaje['type'] == 'JugadorDesconectado':
            print(f"Jugador desconectado: ID {mensaje['id_jugador']}, Total jugadores: {mensaje['TotalJugadores']}")
        
    def desconectar(self):# Cierra todas las conexiones
        self.ejecutandose = False
        self.conectado = False

        # Cerrar servidor
        if self.socket_servidor:
            self.socket_servidor.close()
            for cliente in self.clientes:
                cliente['socket'].close()

        # Cerrar cliente
        if self.socket_cliente:
            self.socket_cliente.close()

        if self.hilo_recepcion:
            self.hilo_recepcion.join()

    def encontrar_ip_servidor(self): # Método que busca un servidor en la red local
        socket_busqueda = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_busqueda.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_busqueda.bind(('', 5556)) # Escuchar en el mismo puerto que el anuncio
        socket_busqueda.settimeout(5) # Esperar 5 segundos

        print("Buscando servidor en la red...")
        try:
            data, direccion_servidor = socket_busqueda.recvfrom(1024)
            if data.decode('utf-8').startswith("RummyServer"):
                print(f"Servidor encontrado en la IP: {direccion_servidor[0]}")
                return direccion_servidor[0]
        except socket.timeout:
            print("Tiempo de búsqueda agotado. Servidor no encontrado.")
        except Exception as e:
            print(f"Error buscando servidor: {e}")
        finally:
            socket_busqueda.close()
        return None