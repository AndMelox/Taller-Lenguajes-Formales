#!/usr/bin/env python3
# ============================================================
#  Lenguajes Formales - UPTC
#  Punto 4.3: Programando un árbol
#  Entorno: Garuda Linux | Intel i5-10300H | 15Gi RAM | ASUS FX506LHB
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox

EPSILON = 'λ'

# ------------------------------------------------------------
# 1. Nodo del árbol de derivación
# ------------------------------------------------------------
class NodoArbol:
    def __init__(self, etiqueta):
        self.etiqueta = etiqueta
        self.hijos = []

    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)


# ------------------------------------------------------------
# 2. Gramática
# ------------------------------------------------------------
class Gramatica:
    def __init__(self, terminales, no_terminales, inicio, producciones):
        self.terminales = set(terminales)
        self.no_terminales = set(no_terminales)
        self.inicio = inicio
        self.producciones = producciones

    def producciones_de(self, nt):
        return self.producciones.get(nt, [])


# ------------------------------------------------------------
# 3. Motor lógico: pertenencia + árbol particular
# ------------------------------------------------------------
class MotorLogico:
    def __init__(self, gramatica):
        self.g = gramatica

    def pertenece(self, palabra):
        nodo, pos = self._derivar(self.g.inicio, palabra, 0)
        if nodo is not None and pos == len(palabra):
            return True, nodo
        return False, None

    def _derivar(self, nt, palabra, pos):
        for prod in self.g.producciones_de(nt):
            nodo = NodoArbol(nt)
            pos_actual = pos
            exito = True
            for simbolo in prod:
                if simbolo == EPSILON:
                    nodo.agregar_hijo(NodoArbol(EPSILON))
                    continue
                if simbolo in self.g.no_terminales:
                    hijo, pos_actual = self._derivar(simbolo, palabra, pos_actual)
                    if hijo is None:
                        exito = False
                        break
                    nodo.agregar_hijo(hijo)
                else:
                    if pos_actual < len(palabra) and palabra[pos_actual] == simbolo:
                        nodo.agregar_hijo(NodoArbol(simbolo))
                        pos_actual += 1
                    else:
                        exito = False
                        break
            if exito:
                return nodo, pos_actual
        return None, None


# ------------------------------------------------------------
# 4. Árbol general (expansión hasta profundidad d)
# ------------------------------------------------------------
def arbol_general(gramatica, profundidad=3):
    def expandir(nt, nivel):
        nodo = NodoArbol(nt)
        if nivel >= profundidad:
            return nodo
        for prod in gramatica.producciones_de(nt):
            hijo = NodoArbol(' → '.join(prod))
            for simbolo in prod:
                if simbolo in gramatica.no_terminales:
                    hijo.agregar_hijo(expandir(simbolo, nivel + 1))
                else:
                    hijo.agregar_hijo(NodoArbol(simbolo))
            nodo.agregar_hijo(hijo)
        return nodo
    return expandir(gramatica.inicio, 0)


# ------------------------------------------------------------
# 5. Impresión jerárquica horizontal
# ------------------------------------------------------------
def imprimir_arbol(nodo, prefijo="", es_ultimo=True, es_raiz=True):
    if nodo is None:
        return ""
    conector = "" if es_raiz else ("└── " if es_ultimo else "├── ")
    salida = prefijo + conector + nodo.etiqueta + "\n"
    nuevo_prefijo = prefijo
    if not es_raiz:
        nuevo_prefijo += "    " if es_ultimo else "│   "
    for i, hijo in enumerate(nodo.hijos):
        salida += imprimir_arbol(hijo, nuevo_prefijo,
                                  i == len(nodo.hijos) - 1, False)
    return salida


# ------------------------------------------------------------
# 6. Interfaz gráfica
# ------------------------------------------------------------
class InterfazTk:
    def __init__(self, root):
        self.root = root
        root.title("Arbol de Derivacion")
        root.geometry("1000x720")

        # --- Panel de entrada ---
        frame_in = ttk.LabelFrame(root, text="Definición de la gramática")
        frame_in.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_in, text="Terminales (separados por coma):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.entry_term = ttk.Entry(frame_in, width=30)
        self.entry_term.insert(0, "0,1")
        self.entry_term.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame_in, text="No terminales (separados por coma):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.entry_nt = ttk.Entry(frame_in, width=30)
        self.entry_nt.insert(0, "S,A,B")
        self.entry_nt.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(frame_in, text="Símbolo inicial:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.entry_ini = ttk.Entry(frame_in, width=10)
        self.entry_ini.insert(0, "S")
        self.entry_ini.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(frame_in, text="Producciones (una por línea, formato A -> aB | c):").grid(row=3, column=0, sticky="nw", padx=5, pady=2)
        self.text_prod = tk.Text(frame_in, width=60, height=5)
        self.text_prod.insert("1.0", "S -> 0S1 | λ\nA -> aA | a\nB -> bB | b")
        self.text_prod.grid(row=3, column=1, padx=5, pady=2)

        ttk.Button(frame_in, text="Cargar gramática", command=self.cargar_gramatica).grid(row=4, column=1, sticky="e", padx=5, pady=5)

        # --- Panel de palabra ---
        frame_pal = ttk.LabelFrame(root, text="Análisis de palabra")
        frame_pal.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_pal, text="Palabra:").pack(side="left", padx=5)
        self.entry_pal = ttk.Entry(frame_pal, width=30)
        self.entry_pal.pack(side="left", padx=5)
        ttk.Button(frame_pal, text="Verificar", command=self.verificar).pack(side="left", padx=5)
        ttk.Button(frame_pal, text="Árbol general", command=self.mostrar_general).pack(side="left", padx=5)

        # --- Panel de salida ---
        frame_out = ttk.LabelFrame(root, text="Resultados")
        frame_out.pack(fill="both", expand=True, padx=10, pady=5)

        self.text_out = tk.Text(frame_out, wrap="none", font=("Monospace", 10))
        self.text_out.pack(fill="both", expand=True)

        self.gramatica = None

    def cargar_gramatica(self):
        try:
            term = [t.strip() for t in self.entry_term.get().split(",") if t.strip()]
            nt = [t.strip() for t in self.entry_nt.get().split(",") if t.strip()]
            ini = self.entry_ini.get().strip()
            lineas = self.text_prod.get("1.0", "end").strip().splitlines()

            producciones = {}
            for linea in lineas:
                if "->" not in linea:
                    continue
                izq, der = linea.split("->", 1)
                izq = izq.strip()
                alternativas = [a.strip() for a in der.split("|")]
                producciones[izq] = []
                for alt in alternativas:
                    # --- Tokenización robusta ---
                    # Si hay espacios, se separa por espacios.
                    # Si no, se separa símbolo a símbolo (letra por letra),
                    # respetando terminales/no terminales de varios caracteres.
                    if not alt.strip():
                        simbolos = [EPSILON]
                    elif " " in alt.strip():
                        simbolos = alt.split()
                    else:
                        # Separar reconociendo terminales/NoTerminales de varios caracteres
                        simbolos = []
                        i = 0
                        candidatos = sorted(
                            set(term) | set(nt),
                            key=len, reverse=True
                        )
                        while i < len(alt):
                            for cand in candidatos:
                                if alt.startswith(cand, i):
                                    simbolos.append(cand)
                                    i += len(cand)
                                    break
                            else:
                                # Si es un carácter suelto (terminal de 1 letra)
                                simbolos.append(alt[i])
                                i += 1
                    producciones[izq].append(simbolos)

            if len(term) < 2:
                raise ValueError("Se requieren mínimo 2 terminales.")
            if len(nt) < 3:
                raise ValueError("Se requieren mínimo 3 no terminales.")
            total_prod = sum(len(v) for v in producciones.values())
            if total_prod < 3:
                raise ValueError("Se requieren mínimo 3 producciones.")

            self.gramatica = Gramatica(term, nt, ini, producciones)
            messagebox.showinfo("OK", "Gramática cargada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def verificar(self):
        if self.gramatica is None:
            messagebox.showwarning("Aviso", "Cargue primero la gramática.")
            return
        palabra = self.entry_pal.get().strip()
        motor = MotorLogico(self.gramatica)
        acepta, arbol = motor.pertenece(palabra)

        self.text_out.delete("1.0", "end")
        self.text_out.insert("end", "=" * 60 + "\n")
        self.text_out.insert("end", f"Palabra: '{palabra}'\n")
        self.text_out.insert("end", "=" * 60 + "\n")
        if acepta:
            self.text_out.insert("end", "✔ PERTENECE al lenguaje.\n\n")
            self.text_out.insert("end", "Árbol de derivación particular:\n\n")
            self.text_out.insert("end", imprimir_arbol(arbol))
        else:
            self.text_out.insert("end", "✘ NO pertenece al lenguaje.\n")

    def mostrar_general(self):
        if self.gramatica is None:
            messagebox.showwarning("Aviso", "Cargue primero la gramática.")
            return
        arbol = arbol_general(self.gramatica, profundidad=3)
        self.text_out.delete("1.0", "end")
        self.text_out.insert("end", "Árbol de derivación general (profundidad 3):\n\n")
        self.text_out.insert("end", imprimir_arbol(arbol))


# ------------------------------------------------------------
# 7. Main
# ------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazTk(root)
    root.mainloop()