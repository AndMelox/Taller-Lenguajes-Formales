# Punto 2.2 - Reconocedor de Propiedades Aritmeticas
# NFA-epsilon que acepta: cantidad impar de ceros, o cantidad de unos multiplo de 3
# Estados: q0, q1, q2, q3, q4, q5
# Estado inicial: q0
# Estados finales: q2, q3

# Transiciones con simbolos (0 y 1)
# Llave: (estado_actual, simbolo) -> Valor: lista de estados destino.
# Rama C (paridad de ceros): q1 = cantidad par de ceros, q2 = cantidad impar.
#   Cada 0 alterna entre q1 y q2; los 1 no cambian el estado (bucle).
# Rama D (unos modulo 3): q3, q4, q5 = 0, 1 y 2 unos (mod 3).
#   Cada 1 avanza q3->q4->q5->q3; los 0 no cambian el estado (bucle).
transiciones = {
    ("q1", "0"): ["q2"],
    ("q2", "0"): ["q1"],
    ("q1", "1"): ["q1"],
    ("q2", "1"): ["q2"],
    ("q3", "1"): ["q4"],
    ("q4", "1"): ["q5"],
    ("q5", "1"): ["q3"],
    ("q3", "0"): ["q3"],
    ("q4", "0"): ["q4"],
    ("q5", "0"): ["q5"],
}

transiciones_epsilon = {
    "q0": ["q1", "q3"],
}

estado_inicial = "q0"           
estados_finales = ["q2", "q3"]  

# Calcula la cerradura epsilon: estados alcanzables solo con transiciones epsilon
# (incluye los estados de entrada).
def cerradura_epsilon(estados):
    resultado = set(estados)       # Empieza con los estados dados
    pendientes = list(estados)     # Estados por explorar

    while pendientes:
        actual = pendientes.pop()                  # Saca un estado pendiente
        if actual in transiciones_epsilon:         # Si tiene salidas epsilon...
            for destino in transiciones_epsilon[actual]:
                if destino not in resultado:       # ...y el destino es nuevo
                    resultado.add(destino)         # Se agrega al resultado
                    pendientes.append(destino)     # Y se explora despues


    return resultado


# Devuelve los estados a los que se llega desde el conjunto 'estados' leyendo 'simbolo'.
def mover(estados, simbolo):
    resultado = set()
    for estado in estados:
        clave = (estado, simbolo)                  # Busca la transicion (estado, simbolo)
        if clave in transiciones:
            for destino in transiciones[clave]:
                resultado.add(destino)
    return resultado


# Simula el automata sobre una cadena e imprime los estados activos tras cada simbolo.
# Retorna True si la cadena es aceptada y False si es rechazada.
def procesar_cadena(cadena):
    # Conjunto inicial: q0 mas lo alcanzable por epsilon (q0, q1, q3)
    estados_actuales = cerradura_epsilon([estado_inicial])
    print("Estados iniciales (con epsilon):", estados_actuales)

    # Lectura de la cadena simbolo por simbolo
    for simbolo in cadena:
        estados_actuales = mover(estados_actuales, simbolo)         # Transicion por el simbolo
        estados_actuales = cerradura_epsilon(estados_actuales)      # Cerradura epsilon del resultado
        print(f"Leido '{simbolo}' -> estados actuales: {estados_actuales}")

    # Aceptada si al final hay al menos un estado final activo
    for final in estados_finales:
        if final in estados_actuales:
            return True
    return False

# Palabras de prueba: "101", "111" y "000" son validas; "1111" y "11" son invalidas
palabras = ["101", "111", "000", "1111", "11"]

# Se evalua cada palabra y se imprime el resultado
for palabra in palabras:
    print("\nProbando la palabra:", palabra)
    aceptada = procesar_cadena(palabra)
    if aceptada:
        print("Resultado: ACEPTADA")
    else:
        print("Resultado: RECHAZADA")