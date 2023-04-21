def euclideanExt(a, b):
    # Caso base
    if b == 0:
        return (a, 1, 0)

    # Caso recursivo
    gcd, x1, y1 = euclideanExt(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (gcd, x, y)

def modInv(a, m):
    # Calcula el máximo común divisor y los coeficientes de Bezout
    gcd, x, y = euclideanExt(a, m)

    # Si a y m no son coprimos, no existe inverso multiplicativo
    if gcd != 1:
        return None

    # Ajusta el valor de x para que esté en el rango [0, m)
    return x % m

def moduloNormal(a,p):
    if a<p:
        return a
    else:
        return a%p
