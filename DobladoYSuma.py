from Puntos import PuntosCurvaElip;

# Definimos la clase Punto para representar un punto en la curva elíptica
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

# Definimos la función que suma dos puntos en la curva elíptica
def sumar_puntos(p: Punto, q: Punto):
    #si es infinito mas un punto
    # Si uno de los puntos es el punto al infinito, devolvemos el otro punto
    if p is None:
        return q
    elif q is None:
        return p

    # Si los puntos son iguales, calculamos el doblado del punto
    if p.x == q.x and p.y == q.y:
        return doblar_punto(p)

    # Calculamos la pendiente de la recta que pasa por los puntos P y Q
    if p.x == q.x:
        return None
    m = ((q.y - p.y) * pow(q.x - p.x, -1, p_modulo)) % p_modulo

    # Calculamos las coordenadas x e y del punto R
    x = (pow(m, 2) - p.x - q.x) % p_modulo
    y = (m * (p.x - x) - p.y) % p_modulo

    return Punto(x, y)

# Definimos la función que realiza el doblado de un punto en la curva elíptica
def doblar_punto(p: Punto):
    # Si el punto es el punto al infinito, devolvemos el mismo punto
    if p is None:
        return None

    # Calculamos la pendiente de la recta tangente a la curva en el punto P
    m = ((3 * pow(p.x, 2) + a) * pow(2 * p.y, -1, p_modulo)) % p_modulo

    # Calculamos las coordenadas -x- e -y- del punto R
    x = (pow(m, 2) - 2 * p.x) % p_modulo
    y = (m * (p.x - x) - p.y) % p_modulo

    return Punto(x, y)

#La funcion verifica si el punto es generador
def verificar(a,b,p_modulo,Punto):
    puntos = PuntosCurvaElip(a, b, p_modulo)
    # Sumamos los puntos P y Q
    nPoint=str(Punto)
    points= str(puntos)
    if nPoint in points:
        return 1
    else:
        return 0

a = 2
b = 2
p_modulo = 17

# Definimos los puntos P y Q
P = Punto(3,1)
Q = Punto(3, 16)

