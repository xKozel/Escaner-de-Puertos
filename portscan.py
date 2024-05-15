import socket
import threading

def escanear_puertos(ip, inicio, fin):
    for puerto in range(inicio, fin + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Tiempo de espera ajustado a 1 segundo

            result = sock.connect_ex((ip, puerto))

            if result == 0:
                servicio = socket.getservbyport(puerto)
                print(f"Puerto {puerto} abierto: {servicio}")
            else:
                print(f"Puerto {puerto} cerrado")
            
            sock.close()
        except Exception as e:
            print(f"Error al escanear puerto {puerto}: {str(e)}")

def main():
    ip = input("Ingrese la dirección IP a escanear: ")
    inicio = int(input("Ingrese el puerto inicial del rango a escanear: "))
    fin = int(input("Ingrese el puerto final del rango a escanear: "))

    # Dividir el rango de puertos en subrangos para escaneo paralelo
    subrangos = [(inicio + i, min(inicio + i + 999, fin)) for i in range(0, fin - inicio + 1, 1000)]

    threads = []
    for subrango in subrangos:
        t = threading.Thread(target=escanear_puertos, args=(ip, subrango[0], subrango[1]))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
