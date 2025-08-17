from conexion import conexion_Rummy
import time

if __name__ == "__main__":
    server = conexion_Rummy()
    server.iniciar_servidor()
    
    try:
        # Mantiene el servidor funcionando
        while True:
            time.sleep(1) 
    except KeyboardInterrupt:
        print("Servidor cerrándose...")
        server.desconectar()