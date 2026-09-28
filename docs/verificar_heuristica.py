"""
==========================================================================
 VERIFICACIÓN DE LA HEURÍSTICA: A* vs. DIJKSTRA
==========================================================================
Este script comprueba que el algoritmo A* implementado en
`transmilenio_ruta.py` siempre encuentra la ruta de MENOR COSTO, y no
solo una ruta "razonable".

¿Cómo lo comprueba? Comparando su resultado contra el algoritmo de
Dijkstra, que no usa ninguna heurística: revisa exhaustivamente todos
los caminos posibles y por definición siempre encuentra el costo
óptimo. Si para cada par de estaciones A* y Dijkstra dan el MISMO costo,
eso confirma que la heurística usada por A* es admisible (nunca
sobreestima el costo real) y que el sistema es confiable.

Ejecución:
    python3 verificar_heuristica.py
==========================================================================
"""

import heapq
from transmilenio_ruta import GRAFO, ESTACIONES, busqueda_a_estrella


def dijkstra(origen, destino):
    """Calcula el costo de la ruta más corta entre origen y destino
    revisando exhaustivamente el grafo (sin heurística). Se usa aquí
    solo como referencia para validar el resultado de A*.
    """
    dist = {estacion: float("inf") for estacion in GRAFO}
    dist[origen] = 0
    cola = [(0, origen)]

    while cola:
        costo_actual, actual = heapq.heappop(cola)
        if costo_actual > dist[actual]:
            continue
        if actual == destino:
            return costo_actual
        for vecino, costo_tramo in GRAFO[actual]:
            nuevo_costo = costo_actual + costo_tramo
            if nuevo_costo < dist[vecino]:
                dist[vecino] = nuevo_costo
                heapq.heappush(cola, (nuevo_costo, vecino))

    return None if dist[destino] == float("inf") else dist[destino]


def main():
    print("Comparando A* contra Dijkstra para todos los pares de estaciones...\n")

    total = 0
    diferencias = 0

    for origen in ESTACIONES:
        for destino in ESTACIONES:
            if origen == destino:
                continue
            total += 1

            _, costo_a_estrella = busqueda_a_estrella(origen, destino)
            costo_dijkstra = dijkstra(origen, destino)

            if costo_a_estrella != costo_dijkstra:
                diferencias += 1
                print(
                    f"DIFERENCIA -> {origen} -> {destino}: "
                    f"A*={costo_a_estrella}  Dijkstra={costo_dijkstra}"
                )

    print("=" * 60)
    print(f"Comparaciones realizadas: {total}")
    print(f"Diferencias encontradas: {diferencias}")
    if diferencias == 0:
        print("La heurística es admisible: A* siempre encontró el costo óptimo.")
    else:
        print("Hay diferencias: revisar la heurística, puede estar sobreestimando.")
    print("=" * 60)


if __name__ == "__main__":
    main()
