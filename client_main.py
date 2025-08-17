from conexion import conexion_Rummy
import time

if __name__ == "__main__":
    client = conexion_Rummy()
    server_ip = client.encontrar_ip_servidor()

    if server_ip and client.conectar_a_servidor(server_ip):
        print(f"Cliente conectado al servidor en {server_ip}")
        try:
            # Mantiene al cliente funcionando
            while client.conectar_a_servidor:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Cliente desconectándose...")
        finally:
            client.desconectar()
    else:
        print("Fallo al conectar con el servidor.")