# Búsqueda heurística: cómo el sistema encuentra la mejor ruta

**Integrante responsable:** [Nombre del Integrante 3]

## ¿Qué es una búsqueda heurística?

Cuando un problema tiene muchas soluciones posibles (en este caso, muchas
rutas posibles entre dos estaciones), explorar **todas** las combinaciones
a ciegas es ineficiente. Una **búsqueda heurística** usa una estimación
—la **heurística**— de qué tan cerca está cada estado (aquí, cada
estación) de la meta, para decidir por dónde conviene seguir explorando
primero. Así se evita perder tiempo en caminos que claramente van a
resultar más costosos.

## El algoritmo: A* (A estrella)

Este proyecto implementa **A***, uno de los algoritmos de búsqueda
heurística más usados en inteligencia artificial. Para cada estación que
evalúa, A* calcula:

```
f(n) = g(n) + h(n)
```

- **g(n)**: el costo real ya recorrido desde el origen hasta la estación `n`.
- **h(n)**: la heurística — una estimación de cuánto falta desde `n` hasta
  el destino.
- **f(n)**: el costo total estimado si se pasa por `n`.

El algoritmo mantiene una **cola de prioridad** con las estaciones por
explorar, y siempre expande primero la que tiene el **menor f(n)**.
Cuando la estación que se extrae de la cola es el destino, esa es la
mejor ruta encontrada.

## La heurística usada

En `transmilenio_ruta.py`, cada estación tiene una posición aproximada
`(x, y)` (diccionario `ESTACIONES`). La heurística `h(n)` es la
**distancia en línea recta** entre la estación `n` y el destino.

## El problema de la admisibilidad (y cómo se resolvió)

Para que A* **garantice** encontrar siempre la ruta óptima, la heurística
debe ser **admisible**: nunca puede sobreestimar el costo real que falta.
Si la heurística "miente" y dice que falta más de lo que realmente falta,
A* puede descartar por error una ruta que en realidad era la mejor.

Al agregar el tramo expreso (Calle 76 → Marly, que recorre más distancia
física en menos tiempo), la distancia en línea recta entre esas dos
estaciones resultó ser *mayor* que el costo real del tramo — es decir,
la heurística cruda **no era admisible** en ese caso.

La solución: se calculó la relación *(distancia / costo)* de cada
conexión del grafo, se tomó la más alta (la "velocidad" más rápida
observada, que corresponde justamente al tramo expreso), y se dividió
toda la heurística por ese valor:

```python
FACTOR_VELOCIDAD = max(
    distancia_en_linea_recta(a, b) / costo
    for a, b, costo in conexiones
)

def heuristica(estacion, destino):
    distancia = distancia_en_linea_recta(estacion, destino)
    return distancia / FACTOR_VELOCIDAD
```

Esto garantiza matemáticamente que la heurística nunca supera el costo
real de ningún tramo del grafo, sin importar qué tan rápido sea.

## Verificación: A* vs. Dijkstra

Para comprobar que la heurística quedó bien calibrada, se comparó el
resultado de A* contra el algoritmo de **Dijkstra** (que no usa
heurística: revisa exhaustivamente todos los caminos posibles y siempre
da el óptimo por definición) para **todas las combinaciones posibles**
de origen y destino del grafo.

El script `verificar_heuristica.py` hace exactamente esa comparación.
Para ejecutarlo:

```bash
python3 verificar_heuristica.py
```

### Resultado de la verificación

```
Comparaciones realizadas: 156
Diferencias encontradas: 0
```

Los dos algoritmos coincidieron en el 100% de los 156 pares posibles de
estaciones, lo que confirma que la heurística es admisible y que el
sistema siempre entrega la ruta de menor costo.

## Ejemplo de cómo el algoritmo elige entre dos rutas

Entre **Portal Norte** y **Universidad Nacional** existen (al menos) dos
caminos:

| Ruta | Costo |
|---|---|
| Cadena completa (sin usar el expreso) | 27 minutos |
| Usando el tramo expreso Calle 76 → Marly | **21 minutos** |

A* evalúa ambas y elige automáticamente la segunda, porque su `f(n)` en
el destino es menor. Esto es justamente lo que se busca demostrar: el
sistema no repite una ruta fija, sino que compara alternativas reales y
se queda con la más barata.
