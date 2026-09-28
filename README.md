# Sistema inteligente para encontrar la mejor ruta en TransMilenio

Proyecto académico — IBERO. Modela un fragmento de TransMilenio como una
base de conocimiento (grafo de estaciones y conexiones) y usa **búsqueda
heurística (A*)** para hallar la ruta de menor costo (tiempo) entre un
origen y un destino.

## Requisitos

- Python 3.8 o superior.
- No requiere instalar ninguna librería externa (solo usa `heapq`, `math`
  y `sys`, que vienen incluidas en Python).

## Cómo ejecutarlo

Desde una terminal, ubicado en la carpeta del proyecto:

```bash
python3 transmilenio_ruta.py
```

El programa mostrará la lista de estaciones disponibles y pedirá:

```
Estación de ORIGEN: Portal Norte
Estación de DESTINO: Universidad Nacional
```

Y mostrará la ruta encontrada, el costo total estimado (en minutos) y el
detalle de cada tramo.

### Modo rápido (sin digitar nada)

También se puede indicar origen y destino directamente como argumentos,
útil para grabar el video o hacer pruebas rápidas:

```bash
python3 transmilenio_ruta.py "Portal Norte" "Universidad Nacional"
python3 transmilenio_ruta.py "Héroes" "Universidad Nacional"
```

## Estaciones disponibles en la base de conocimiento

Portal Norte, Toberín, Calle 100, Calle 85, Calle 76, Héroes, Calle 72,
Calle 63, Calle 57, Marly, Calle 45, Universidad Nacional, NQS - Calle 30.

> Se incluyó a propósito un tramo "expreso" (Calle 76 → Marly, salta
> estaciones intermedias) y un ramal alterno más largo por la NQS. Esto
> permite que el algoritmo demuestre que sí evalúa varias rutas posibles
> y elige la de menor costo, no simplemente la primera que encuentra —
> que es justamente el punto de usar búsqueda heurística en vez de listar
> la ruta "obvia" a mano.




