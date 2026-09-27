# Punto 2.1 - Reconocedor de Patrones Repetitivos
# NFA-epsilon que acepta: (01)+ o (010)+
# Estados: q0, q1, q2, q3, q4, q5, q6, q7
# Estado inicial: q0
# Estados finales: q3, q7

# Transiciones con simbolos (0 y 1)
transiciones = {
    ("q1", "0"): ["q2"],
    ("q2", "1"): ["q3"],
    ("q3", "0"): ["q2"],
    ("q4", "0"): ["q5"],
    ("q5", "1"): ["q6"],
    ("q6", "0"): ["q7"],
    ("q7", "0"): ["q5"],
}

transiciones_epsilon = {
    "q0": ["q1", "q4"],
}

estado_inicial = "q0"
estados_finales = ["q3", "q7"]

def cerradura_epsilon(estados):
    resultado = set(estados)
    pendientes = list(estados)

    while pendientes:
        actual = pendientes.pop()
        if actual in transiciones_epsilon:
            for destino in transiciones_epsilon[actual]:
                if destino not in resultado:
                    resultado.add(destino)
                    pendientes.append(destino)

    return resultado

def mover(estados, simbolo):
    resultado = set()
    for estado in estados:
        clave = (estado, simbolo)
        if clave in transiciones:
            for destino in transiciones[clave]:
                resultado.add(destino)
    return resultado

def procesar_cadena(cadena):
    estados_actuales = cerradura_epsilon([estado_inicial])
    print("Estados iniciales (con epsilon):", estados_actuales)

    for simbolo in cadena:
        estados_actuales = mover(estados_actuales, simbolo)
        estados_actuales = cerradura_epsilon(estados_actuales)
        print(f"Leido '{simbolo}' -> estados actuales: {estados_actuales}")

    for final in estados_finales:
        if final in estados_actuales:
            return True
    return False

palabras = ["01", "0101", "010", "0", "011"]

for palabra in palabras:
    print("\nProbando la palabra:", palabra)
    aceptada = procesar_cadena(palabra)
    if aceptada:
        print("Resultado: ACEPTADA")
    else:
        print("Resultado: RECHAZADA")