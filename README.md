# Taller Primer 50% - Lenguajes Formales

**Universidad Pedagógica y Tecnológica de Colombia (UPTC)**
Facultad de Ingeniería - Ingeniería de Sistemas y Computación
Docente: Ing. Alex Puertas González - Tunja, 2026

## Autores

- Andrés Felipe Melo Avellaneda
- Nicolás David Lizarazo Rojas
- Duvan Camilo Hernandez Chavarro
- Edison Eduardo Olarte Arias

## Descripción

Repositorio del taller del primer 50% de Lenguajes Formales (lenguajes, gramáticas y autómatas). Contiene los programas y archivos de apoyo que sustentan el documento del taller.

## Contenido del taller

| Punto | Tema | Valor |
|-------|------|-------|
| 2.1 | Reconocedor de patrones repetitivos (NFA-ε) | 0.5 |
| 2.2 | Reconocedor de propiedades aritméticas (NFA-ε) | 0.5 |
| 3.1 | Gramáticas de muchos tipos (clasificación de Chomsky) | 0.5 |
| 3.2 | Equivalencia gramática ↔ autómata | 0.5 |
| 3.3 | Funciones de salida (FTE) | 0.5 |
| 4.1 | NFA → DFA | 0.5 |
| 4.2 | DFA → DFA mínimo | 0.5 |
| 4.3 | Programando un árbol de derivación | 1.0 |

## Archivos del repositorio

- `LF_Punto_2_1.py`: emulador del NFA-ε que acepta `(01)+` o `(010)+`.
- `LF_Punto_2_2.py`: emulador del NFA-ε que acepta cantidad impar de ceros o cantidad de unos múltiplo de 3.
- `TLF_2_1.jff` y `LF_T2_2.jff`: autómatas de los puntos 2.1 y 2.2 para JFLAP.
- `programa_arbol.py`: programa "Árbol de Derivación" (punto 4.3).

## Requisitos

- Python 3.x
- JFLAP (solo para abrir los archivos `.jff`)

## Ejecución

```powershell
python LF_Punto_2_1.py
python LF_Punto_2_2.py
python programa_arbol.py
```

Los emuladores 2.1 y 2.2 imprimen, para cada palabra de prueba, el conjunto de estados activos tras cada símbolo leído (aplicando clausura-ε) y el resultado final: ACEPTADA o RECHAZADA.

## Programa Árbol de Derivación (punto 4.3)

Interfaz gráfica que permite:

- Ingresar una gramática libre de contexto (mínimo 2 terminales, 3 no terminales y 3 producciones).
- Verificar si una palabra pertenece al lenguaje generado.
- Mostrar el árbol de derivación particular de la palabra y el árbol de derivación general de la gramática.

## Actualizar el repositorio

```powershell
git pull origin main
```