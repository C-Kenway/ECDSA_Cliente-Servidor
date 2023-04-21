import socket
import json
from DobladoYSuma import sumar_puntos
from DobladoYSuma import Punto
from DobladoYSuma import verificar
import Euclides_Ext

HOST = "127.0.0.1"  # Nombre del host o direccion ip
#HOST = "192.168.254.223"  # Nombre del host o direccion ip
PORT = 5000  # Puerto usado por el servidor
buffer_size = 1024

#HOST = str(input('Ingrese el la direccion del host para el server: '))
#PORT = int(input('Ingrese el Puerto: '))
# Crear un objeto socket para el cliente (Cliente)
Cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar el socket a un servidor remoto en el puerto 5000
Cliente.connect((HOST, PORT))
print('Se ha establecido una conexión con el servidor remoto.')


#Aqui comineza el programa

####################################
#Parte 1: Key Generation
###################################
print("####################################")
print("Signature Algorithm")
print("####################################")

print("\nNotacion: y^2 = x^3 + ax + b (mod p):")
# Definimos los valores de 'a' como -aCurva-, 'b' como -bCurva- y 'p' como -pModulo- para la curva elíptica E
#Valor a
#Ingresa el valor para "a" en la expresion de la formula
aCurva=int(input("Ingrese l valor de a: \n"))
eleccion = str(aCurva)
Cliente.send(eleccion.encode())
#Ingresa el valor para "b" en la expresion de la formula
bCurva=int(input("Ingrese l valor de b: \n"))
eleccion = str(bCurva)
Cliente.send(eleccion.encode())
#Ingresa valor de Modulo
pModulo=int(input("Ingrese l valor de p: \n"))
eleccion = str(pModulo)
Cliente.send(eleccion.encode())
while(True):
    print("Notacion: Punto G:[Valor X, Valor Y]")
    # Generador
    # Valor x
    Gx = int(input("Ingrese el Valor X: \n"))
    # Valor y
    Gy = int(input("Ingrese el Valor Y: \n"))
    G = Punto(Gx,Gy)
    # Verificamos si el punto G es generador si no, entonces no continua
    ver = verificar(aCurva, bCurva, pModulo, G)
    if ver == 1:
        Vx = G.x
        Vy = G.y
        ValPunto = [Vx, Vy]
        Enviar = json.dumps(ValPunto)
        Cliente.sendall(Enviar.encode())
        break
    else:
        print(f"El punto P: {G}. No es generador en la curva intente otros valores")

#Valor de -q-: Numero de puntos dentro de la curva E
q=int(input("Ingrese l valor de q: \n"))
eleccion = str(q)
Cliente.send(eleccion.encode())

#Enviar entero -d-: 0<d<q
while(True):
    print("Nota: 0 < d < q")
    d = int(input("Ingrese l valor de d: \n"))
    if (0<d) and d<q:
        Enviar = json.dumps(d)
        Cliente.sendall(Enviar.encode())
        break
    else:
        print(f"El valor de d: {d}. No es correcto")

#Computar el valor de B: B=dG (Primera Suma)
B = G
# como i comienza en 0 para hacer las iteraciones totales, es d-1
for i in range(d - 1):
    B = sumar_puntos(G, B)
Vx = B.x
Vy = B.y
ValPunto = [Vx, Vy]
Enviar = json.dumps(ValPunto)
Cliente.sendall(Enviar.encode())

####################################
#Parte 2: Signature Algorithm
###################################
print("####################################")
print("Signature Algorithm")
print("####################################")

#Escoje una llave efimera
KE=int(input("Ingrese el valor de KE (Llave Efimera): \n"))
eleccion = str(KE)

#Computa R = KE*G
R = G
# como i comienza en 0 para hacer las iteraciones totales, es d-1
for i in range(KE - 1):
    R = sumar_puntos(G, R)

#Extraemos el valor x en R para su utlizizacion posterior y lo enviamos
r = R.x
Enviar = json.dumps(r)
Cliente.sendall(Enviar.encode())

"""
Computa S = (H(m)+d*r)KE^-1
Lo haremos por partes
"""
#Primero recibimos el valor del Hash: H(m) -> Hm y lo enviamos
Hm=int(input("Ingrese l valor de H(m): \n"))
eleccion = str(Hm)
Cliente.send(eleccion.encode())

#Despues el inverso de KE: de estos -Ke_1- es el valor que nos importa, puesto que -Ke_1- es el inverso. -> Ke_1 = KE^-1 mod p
#(-gcd- e -y- se pueden usar posteriormente para alguna validacion)
gcd,Ke_1,y = Euclides_Ext.euclideanExt(Hm, pModulo)



#Luego hacemos la suma del valor Hash y enviamos
s = (Hm+(d*r))*Ke_1
s = Euclides_Ext.moduloNormal(s,q)
eleccion = str(s)
Cliente.send(eleccion.encode())

#Esperamos respuesta si fue Exito! o No...
Respuesta = json.loads(Cliente.recv(buffer_size).decode())
print("\n------------------------------------")
print("Adivina que... Tu respuesta fue... ")
print(Respuesta)

# Cerrar la conexión con el servidor
Cliente.close()