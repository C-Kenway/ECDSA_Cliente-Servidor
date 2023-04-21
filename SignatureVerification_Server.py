import socket
import json
from DobladoYSuma import sumar_puntos
from DobladoYSuma import Punto
import Euclides_Ext

HOST = "localhost"
#HOST = "192.168.230.165"  # The server's hostname or IP address
PORT = 5000  # Puerto usado por el servidor
buffer_size = 1024

#HOST = str(input('Ingrese el la direccion del host para el server: '))
#PORT = int(input('Ingrese el Puerto: '))
# Crear un objeto socket para el servidor
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asignar una dirección IP y un número de puerto al socket
Server.bind((HOST, PORT))

# Configurar el socket para escuchar conexiones entrantes
Server.listen(1)
print('El servidor está escuchando en {}:{}'.format(HOST, PORT))

try:
    # Aceptar una conexión entrante
    Cliente, direccion = Server.accept()
    print('Se ha establecido una conexión desde {}:{}'.format(direccion[0], direccion[1]))
    ####################################
    # Recibir datos del cliente
    ###################################
    print("####################################")
    print("Recibir datos")
    print("####################################")
    # Recibir valores de la curva elíptica desde el cliente
    aCurva = json.loads(Cliente.recv(buffer_size).decode())
    bCurva = json.loads(Cliente.recv(buffer_size).decode())
    pModulo = json.loads(Cliente.recv(buffer_size).decode())
    print(f"a: {aCurva}, b: {bCurva}, p: {pModulo}")

    # Recibir punto E desde el cliente
    Valores = json.loads(Cliente.recv(buffer_size).decode())
    x = Valores[0]
    y = Valores[1]
    G = Punto(x, y)
    print(f"Punto G: {G}")

    #Recibir el valor de q.
    q = json.loads(Cliente.recv(buffer_size).decode())
    print(f"Valor q: {q}")

    #Recibir entero -d-: 0<d<q
    d = json.loads(Cliente.recv(buffer_size).decode())
    print(f"Valor d: {d}")

    # Recibir Punto B desde el cliente
    ValoresB = json.loads(Cliente.recv(buffer_size).decode())
    x = ValoresB[0]
    y = ValoresB[1]
    B = Punto(x, y)
    print(f"Punto B: {B}")

    #Recibir valor de r:
    r = json.loads(Cliente.recv(buffer_size).decode())
    print(f"Valor de r: {r}")

    #Recibir valor de Hash: H(m)
    Hm = json.loads(Cliente.recv(buffer_size).decode())
    print(f"Hash: H(m) = {Hm}")

    # Recibir valor de s = (H(m)+dr)KE^-1
    s = json.loads(Cliente.recv(buffer_size).decode())
    print(f"Valor S: {s}")

    ####################################
    # Signature Verification
    ###################################
    print("####################################")
    print("Signature Verification")
    print("####################################")
    # Computa w = s^-1 mod q
    #Primero debemos obtener s_1. Nota:  s_1 = S^-1 mod p (-gcd- e -y- se pueden usar posteriormente para alguna validacion)
    gcd, s_1, y = Euclides_Ext.euclideanExt(s, q)
    print(f"s^-1: {s_1}")
    #Ahora si calculamos w
    w = Euclides_Ext.moduloNormal(s_1,q)
    print(f"Valor de w: {w}")
    #Computar u1 =( w * Hm ) mod q
    u1 = Euclides_Ext.moduloNormal(w*Hm,q)
    print (f"u1: {u1}")
    #Computar u2 = (w*r) mod q
    u2 = Euclides_Ext.moduloNormal(w*r,q)
    print(f"u2: {u2}")
    """
    Computar el punto: p = u1*G + u2*B
    Todo por partes
    """
    # Punto C: u1*G
    C = G
    # como i comienza en 0 para hacer las iteraciones totales, es d-1
    t=0
    for t in range(u1 - 1):
        C = sumar_puntos(G, C)
    print(f"C:{C} = {u1}*{G}")
    #Punto D: u2*B
    D = B
    # como i comienza en 0 para hacer las iteraciones totales, es d-1
    f=0
    for f in range(u2 - 1):
        D = sumar_puntos(B, D)
    print(f"D:{D} = {u2}*{B}")

    #Suma de puntos para obtener el Punto: p
    p = sumar_puntos(C,D)
    print(f"Punto p: {p}")

    if p.x == r:
        message = "Exitoo! \(^-^)/"
        print(message)
        Enviar = json.dumps(message)
        Cliente.sendall(Enviar.encode())
    else:
        message = "NO!... ;-;"
        print(message)
        Enviar = json.dumps(message)
        Cliente.sendall(Enviar.encode())


    # Cerrar la conexión con el cliente
    Cliente.close()

except Exception as e:
    print("Error:", e)

finally:
    # Cerrar el socket del servidor
    Server.close()