import socket
import sys
import rsa
import time
import ctypes
from threading import Thread
BUFFER_SIZE = 256


def enviar_caracter(i):
    # Sending data to server
    caracter_encriptado = (ord(i)**int(e_serv[0])) % int(e_serv[1])
    # print(caracter_encriptado)
    conn.sendall(str(caracter_encriptado).encode())


if __name__ == '__main__':
    global e_serv, d, n
    # Creación del par de llaves del cliente
    N = 50
    # Creación del par de llaves del servidor python optimizado
    p = None
    q = None
    while (p == q):
        p = rsa.finder2(N)
        q = rsa.finder2(N)
    n = p*q
    phi = (p-1)*(q-1)
    e = rsa.pub_key(phi)
    d = rsa.priv_key(e, phi)
    """
    # Creación del par de llaves del cliente python no optimizado
    p = None
    q = None
    while (p == q):
        p = rsa.prime_finder(N)
        q = rsa.prime_finder(N)
    n = p*q
    phi = (p-1)*(q-1)
    e = rsa.pub_key1(phi)
    d = rsa.priv_key(e, phi)
    """
    """
    # Creación del par de llaves del cliente con C
    so_file = './rsa_c.so'
    lib = ctypes.CDLL(so_file)
    lib.inicia.argtypes = []
    lib.gcd2.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.gcd2.restype = ctypes.c_int
    lib.prime_finder2.argtypes = [ctypes.c_int]
    lib.prime_finder2.restype = ctypes.c_int
    lib.pubkeys.argtypes = [ctypes.c_int]
    lib.pubkeys.restype = ctypes.c_int
    lib.privkeys.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.privkeys.restype = ctypes.c_int
    lib.inicia()
    p = None
    q = None
    while (p == q):
        p = lib.prime_finder2(N)
        q = lib.prime_finder2(N)
    n = p*q
    phi = (p-1)*(q-1)
    e = lib.pubkeys(phi)
    d = lib.privkeys(e, phi)"""
    print(p)
    print(q)
    print(phi)
    print(
        f"Llave pública del cliente: ({e}, {n})\nLlave privada del cliente: ({d}, {n})")

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Client socket is created')
    try:
        conn.connect(("0.0.0.0", 4444))
        print('Connected')
    except:
        print('An Error Occured!')
        sys.exit()

    # Primero, enviar llave pública al servidor
    llave = str(e) + "," + str(n)
    print("---Enviando llave pública al servidor---\n")
    conn.sendall(llave.encode())
    # Recibir llave pública del servidor
    data = conn.recv(BUFFER_SIZE)
    print("---Recibiendo llave pública del servidor---\n")
    e_serv = data.decode().split(",")
    print(
        f"Llave pública del servidor: ({e_serv[0]}, {e_serv[1]})\n")
    tiempos_enviar = []
    tiempos_recibir = []
    while True:
        # Cliente siempre inicia la conversación
        mensaje_recv = ''
        # Mensaje_a_enviar
        MESSAGE_input = input('Cliente: ')    # Taking input from user
        inicio_enviar = time.perf_counter()
        # Send message length to server
        conn.sendall(str(len(MESSAGE_input)).encode())
        for i in MESSAGE_input:
            h_enviar = Thread(target=enviar_caracter, args=(i,))
            h_enviar.start()
            h_enviar.join()
        fin_enviar = time.perf_counter()
        tiempos_enviar.append(fin_enviar-inicio_enviar)
        print(f"Tiempo de envío: {fin_enviar-inicio_enviar} s")
        print(f"Total_time_send_1 es = {sum(tiempos_enviar)} segundos")
        if MESSAGE_input == 'quit':    # Enter 'quit' to break/stop the loop
            break
        # Mensaje a recibir
        print("Aguardando mensaje del servidor ...")
        # Receive message length from server
        len_message = conn.recv(BUFFER_SIZE)
        caracteres_recv = []
        inicio_recibir = time.perf_counter()
        for k in range(int(len_message.decode())):
            # Receiving data from server
            caracteres_recv.append((int(conn.recv(BUFFER_SIZE).decode())))
        for k in caracteres_recv:
            caracter_desencriptado = (k**d) % n
            mensaje_recv += chr(caracter_desencriptado)
            # print(mensaje_recv)
        fin_recibir = time.perf_counter()
        tiempos_recibir.append(fin_recibir-inicio_recibir)
        print(f"Tiempo de recepción: {fin_recibir-inicio_recibir} s")
        print(f"total_time_recieve_2 es : {sum(tiempos_recibir)} segundos")
        if mensaje_recv == 'quit':
            break
        # Decoding received data and printing
        print("Servidor: ", mensaje_recv)
    conn.close()   # Closing the TCP socket
    print('Connection Closed')
