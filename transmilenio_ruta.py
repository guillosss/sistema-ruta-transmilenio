"""
==========================================================================
 SISTEMA INTELIGENTE PARA ENCONTRAR LA MEJOR RUTA EN TRANSMILENIO
==========================================================================
Proyecto académico - Corporación Universitaria Iberoamericana (IBERO)

Este programa modela un fragmento del sistema TransMilenio como una
BASE DE CONOCIMIENTO (un grafo de estaciones y conexiones) y utiliza
BÚSQUEDA HEURÍSTICA (algoritmo A*) para encontrar la ruta de menor
costo entre una estación de origen y una de destino.

--------------------------------------------------------------------------
CÓMO EJECUTARLO
--------------------------------------------------------------------------
1. Requiere Python 3.8 o superior (no necesita librerías externas).
2. Desde la terminal, ubicado en la carpeta del proyecto, ejecutar:

       python3 transmilenio_ruta.py

3. El programa mostrará la lista de estaciones disponibles y pedirá:
       - Estación de origen
       - Estación de destino
4. Mostrará la ruta encontrada, el costo total (tiempo estimado en
   minutos) y el detalle de cada tramo.

También puede ejecutarse en "modo prueba" (sin digitar nada) pasando
argumentos por línea de comandos, por ejemplo:

       python3 transmilenio_ruta.py "Portal Norte" "Universidad Nacional"

--------------------------------------------------------------------------
ESTRUCTURA DEL CÓDIGO
--------------------------------------------------------------------------
1. ESTACIONES   -> base de conocimiento: coordenadas aproximadas de cada
                   estación (se usan solo para calcular la heurística).
2. CONEXIONES   -> base de conocimiento: reglas/hechos de qué estaciones
                   están unidas y el costo (minutos) de recorrer ese tramo.
3. heuristica() -> estima cuánto falta para llegar al destino (distancia
                   en línea recta), usada por el algoritmo A*.
4. busqueda_a_estrella() -> el algoritmo de búsqueda heurística en sí.
5. main()       -> interfaz de consola: pide origen/destino y muestra el
                   resultado.
==========================================================================
"""

import heapq
import math
import sys


# ==========================================================================
# 1. BASE DE CONOCIMIENTO: ESTACIONES (hechos: cada estación existe y
#    tiene una posición aproximada, usada únicamente para la heurística)
# ==========================================================================
ESTACIONES = {
    "Portal Norte":          (0.0, 22.0),
    "Toberín":                (0.5, 20.0),
    "Calle 100":              (1.0, 17.0),
    "Calle 85":               (1.0, 15.0),
    "Calle 76":               (1.2, 13.0),
    "Héroes":                 (1.5, 10.5),
    "Calle 72":               (1.5, 9.0),
    "Calle 63":               (1.5, 7.5),
    "Calle 57":               (1.5, 6.0),
    "Marly":                  (1.5, 4.5),
    "Calle 45":               (1.5, 3.0),
    "Universidad Nacional":   (1.5, 0.0),
    # Estación de una línea alterna (NQS), para mostrar que el sistema
    # es capaz de descartar rutas más largas aunque existan.
    "NQS - Calle 30":         (5.0, 5.0),
}


# ==========================================================================
# 2. BASE DE CONOCIMIENTO: CONEXIONES (hechos: qué estaciones están
#    conectadas directamente y el costo -en minutos- de ese tramo)
#    El grafo es NO dirigido: si A conecta con B, también se puede volver.
# ==========================================================================
CONEXIONES_BASE = [
    ("Portal Norte", "Toberín", 3),
    ("Toberín", "Calle 100", 4),
    ("Calle 100", "Calle 85", 2),
    ("Calle 85", "Calle 76", 2),
    ("Calle 76", "Héroes", 3),
    ("Héroes", "Calle 72", 2),
    ("Calle 72", "Calle 63", 2),
    ("Calle 63", "Calle 57", 2),
    ("Calle 57", "Marly", 2),
    ("Marly", "Calle 45", 2),
    ("Calle 45", "Universidad Nacional", 3),

    # Ruta "expresa" (troncal directa Calle 76 -> Marly, se salta
    # estaciones intermedias): permite que el sistema encuentre una
    # ruta distinta a la "obvia" cuando realmente es más rápida.
    ("Calle 76", "Marly", 5),

    # Ramal alterno por la NQS: existe, pero es más largo, para
    # comprobar que el algoritmo SÍ lo descarta si no conviene.
    ("Héroes", "NQS - Calle 30", 8),
    ("NQS - Calle 30", "Universidad Nacional", 9),
]


def construir_grafo(conexiones):
    """Convierte la lista de conexiones en un grafo tipo diccionario:
    { estacion: [(vecino, costo), ...], ... }
    """
    grafo = {estacion: [] for estacion in ESTACIONES}
    for a, b, costo in conexiones:
        grafo[a].append((b, costo))
        grafo[b].append((a, costo))
    return grafo


GRAFO = construir_grafo(CONEXIONES_BASE)


# ==========================================================================
# 3. HEURÍSTICA: distancia en línea recta entre dos estaciones, escalada
#    por FACTOR_VELOCIDAD. Para que A* garantice la mejor ruta, la
#    heurística NUNCA debe sobreestimar el costo real restante (debe ser
#    "admisible"). Como hay un tramo "expreso" que recorre más distancia
#    física en menos tiempo, se divide la distancia por la velocidad más
#    alta observada en todo el grafo: así la heurística siempre queda por
#    debajo (o igual) del costo real de cualquier tramo.
# ==========================================================================
FACTOR_VELOCIDAD = max(
    math.dist(ESTACIONES[a], ESTACIONES[b]) / costo
    for a, b, costo in CONEXIONES_BASE
)


def heuristica(estacion, destino):
    x1, y1 = ESTACIONES[estacion]
    x2, y2 = ESTACIONES[destino]
    distancia = math.dist((x1, y1), (x2, y2))
    return distancia / FACTOR_VELOCIDAD


# ==========================================================================
# 4. ALGORITMO DE BÚSQUEDA HEURÍSTICA (A*)
# ==========================================================================
def busqueda_a_estrella(origen, destino):
    """Devuelve (ruta, costo_total) usando el algoritmo A*.

    - g(n): costo real acumulado desde el origen hasta la estación n.
    - h(n): heurística (línea recta) desde n hasta el destino.
    - f(n) = g(n) + h(n): lo que ordena la cola de prioridad.

    Si no existe ruta, devuelve (None, None).
    """
    if origen not in GRAFO or destino not in GRAFO:
        return None, None

    # Cola de prioridad: (f, contador, estacion, costo_g, ruta_hasta_aqui)
    contador = 0
    frontera = [(heuristica(origen, destino), contador, origen, 0, [origen])]
    visitados = {}  # estacion -> mejor costo_g encontrado

    while frontera:
        f_actual, _, actual, costo_g, ruta = heapq.heappop(frontera)

        if actual == destino:
            return ruta, costo_g

        if actual in visitados and visitados[actual] <= costo_g:
            continue
        visitados[actual] = costo_g

        for vecino, costo_tramo in GRAFO[actual]:
            nuevo_costo_g = costo_g + costo_tramo
            if vecino in visitados and visitados[vecino] <= nuevo_costo_g:
                continue
            contador += 1
            nuevo_f = nuevo_costo_g + heuristica(vecino, destino)
            heapq.heappush(
                frontera,
                (nuevo_f, contador, vecino, nuevo_costo_g, ruta + [vecino]),
            )

    return None, None


# ==========================================================================
# 5. INTERFAZ DE CONSOLA
# ==========================================================================
def mostrar_estaciones():
    print("\nEstaciones disponibles:")
    for nombre in ESTACIONES:
        print(f"  - {nombre}")


def mostrar_resultado(origen, destino, ruta, costo):
    print("\n" + "=" * 60)
    if ruta is None:
        print(f"No se encontró una ruta entre '{origen}' y '{destino}'.")
        print("=" * 60)
        return

    print(f"Ruta encontrada: {' -> '.join(ruta)}")
    print(f"Costo total estimado: {costo} minutos")
    print("-" * 60)
    print("Detalle de tramos:")
    for i in range(len(ruta) - 1):
        actual, siguiente = ruta[i], ruta[i + 1]
        for vecino, costo_tramo in GRAFO[actual]:
            if vecino == siguiente:
                print(f"  {actual:<25} -> {siguiente:<25} ({costo_tramo} min)")
                break
    print("=" * 60)


def pedir_estacion(mensaje):
    while True:
        valor = input(mensaje).strip()
        # Permite escribir el nombre sin importar mayúsculas/minúsculas
        for nombre in ESTACIONES:
            if nombre.lower() == valor.lower():
                return nombre
        print(f"  '{valor}' no es una estación válida. Intenta de nuevo.")


def main():
    print("SISTEMA INTELIGENTE DE RUTAS - TRANSMILENIO (A*)")

    # Modo prueba: python3 transmilenio_ruta.py "Origen" "Destino"
    if len(sys.argv) == 3:
        origen, destino = sys.argv[1], sys.argv[2]
    else:
        mostrar_estaciones()
        origen = pedir_estacion("\nEstación de ORIGEN: ")
        destino = pedir_estacion("Estación de DESTINO: ")

    ruta, costo = busqueda_a_estrella(origen, destino)
    mostrar_resultado(origen, destino, ruta, costo)


if __name__ == "__main__":
    main()
