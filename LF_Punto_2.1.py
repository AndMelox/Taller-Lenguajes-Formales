# Punto 2.1 - Reconocedor de Patrones Repetitivos
# NFA-epsilon que acepta: (01)+ o (010)+
# Estados: q0, q1, q2, q3, q4, q5, q6, q7
# Estado inicial: q0
# Estados finales: q3, q7

# Transiciones con simbolos (0 y 1)
# Diccionario: la llave es (estado_actual, simbolo) y el valor es la lista de estados destino.
# Rama A (patron "01" repetido): q1 -0-> q2 -1-> q3, y desde q3 con 0 vuelve a q2 (repite el patron)
# Rama B (patron "010" repetido): q4 -0-> q5 -1-> q6 -0-> q7, y desde q7 con 0 vuelve a q5 (repite el patron)
transiciones = {
    ("q1", "0"): ["q2"],
    ("q2", "1"): ["q3"],
    ("q3", "0"): ["q2"],
    ("q4", "0"): ["q5"],
    ("q5", "1"): ["q6"],
    ("q6", "0"): ["q7"],
    ("q7", "0"): ["q5"],
}

# Transiciones epsilon (se toman sin leer ningun simbolo).
# Desde q0 el automata se bifurca al mismo tiempo hacia la rama A (q1) y la rama B (q4).
transiciones_epsilon = {
    "q0": ["q1", "q4"],
}

estado_inicial = "q0"          # Estado donde comienza el automata
estados_finales = ["q3", "q7"] # Si al terminar la cadena hay algun estado activo aqui, se acepta

# Calcula la cerradura epsilon: todos los estados alcanzables
# desde los estados dados usando unicamente transiciones epsilon (incluye los propios estados).
def cerradura_epsilon(estados):
    resultado = set(estados)       # Conjunto resultado; empieza con los estados de entrada
    pendientes = list(estados)     # Pila de estados por explorar

    while pendientes:
        actual = pendientes.pop()                  # Toma un estado pendiente
        if actual in transiciones_epsilon:         # Si tiene transiciones epsilon...
            for destino in transiciones_epsilon[actual]:
                if destino not in resultado:       # ...y el destino aun no fue visitado
                    resultado.add(destino)         # Lo agrega al resultado
                    pendientes.append(destino)     # Y lo deja pendiente para explorar sus epsilon

    return resultado

# Dado un conjunto de estados activos y un simbolo, devuelve el conjunto de estados
# a los que se llega al leer ese simbolo (sin considerar epsilon).
def mover(estados, simbolo):
    resultado = set()
    for estado in estados:
        clave = (estado, simbolo)                  # Busca la transicion (estado, simbolo)
        if clave in transiciones:
            for destino in transiciones[clave]:    # Puede haber varios destinos (no determinismo)
                resultado.add(destino)
    return resultado

# Simula el automata sobre una cadena y dice si es aceptada (True) o rechazada (False).
def procesar_cadena(cadena):
    # Se parte del estado inicial junto con todo lo alcanzable por epsilon (q0, q1, q4)
    estados_actuales = cerradura_epsilon([estado_inicial])
    print("Estados iniciales (con epsilon):", estados_actuales)

    # Se lee la cadena simbolo por simbolo
    for simbolo in cadena:
        estados_actuales = mover(estados_actuales, simbolo)         # Avanza leyendo el simbolo
        estados_actuales = cerradura_epsilon(estados_actuales)      # Aplica epsilon al nuevo conjunto
        print(f"Leido '{simbolo}' -> estados actuales: {estados_actuales}")

    # Al terminar la cadena, se acepta si algun estado activo es final
    for final in estados_finales:
        if final in estados_actuales:
            return True
    return False

# Palabras de prueba: validas ("01", "0101", "010") e invalidas ("0", "011")
palabras = ["01", "0101", "010", "0", "011"]

# Se prueba cada palabra e imprime ACEPTADA o RECHAZADA
for palabra in palabras:
    print("\nProbando la palabra:", palabra)
    aceptada = procesar_cadena(palabra)
    if aceptada:
        print("Resultado: ACEPTADA")
    else:
        print("Resultado: RECHAZADA")