# Base de conocimiento del sistema

**Integrante responsable:** [Nombre del Integrante 1]

## El problema

Un usuario del sistema TransMilenio conoce su estación de origen y su
estación de destino, pero no sabe cuál es el camino más rápido entre las
decenas de conexiones posibles del sistema. Este proyecto automatiza esa
decisión: dado un origen y un destino, el sistema encuentra por sí solo
la ruta de menor costo (tiempo) entre ambos.

## ¿Qué es una base de conocimiento?

Una base de conocimiento es un conjunto de **hechos** y **reglas** que un
sistema inteligente puede consultar para razonar sobre un problema, sin
necesidad de que un humano le diga paso a paso qué hacer en cada caso
particular. En este proyecto, la base de conocimiento tiene dos tipos de
hechos:

1. **Las estaciones que existen** (los objetos del dominio).
2. **Las conexiones entre estaciones**, cada una con un costo en minutos
   (las relaciones entre esos objetos).

A partir de esos hechos, el sistema puede razonar y encontrar rutas que
nadie escribió explícitamente — por ejemplo, combinando varios tramos
hasta llegar al destino.

## Reglas lógicas del sistema

- Si dos estaciones **A** y **B** están conectadas directamente con un
  costo **c**, entonces se puede viajar de A a B (y de B a A) pagando
  ese costo.
- Una **ruta válida** entre un origen y un destino es una secuencia de
  conexiones directas donde cada estación de la secuencia está
  conectada con la siguiente.
- El **costo de una ruta** es la suma de los costos de todos sus tramos.
- La **mejor ruta** entre un origen y un destino es, de todas las rutas
  válidas posibles, la que tiene el menor costo total.

Encontrar esa "mejor ruta" no es trivial cuando hay varias combinaciones
posibles — por eso el sistema usa búsqueda heurística (ver
`busqueda_heuristica.md`) en lugar de comparar todas las rutas a mano.

## Estaciones del sistema

| Estación | Rol en el grafo |
|---|---|
| Portal Norte | Extremo norte de la troncal Autonorte |
| Toberín | Estación intermedia |
| Calle 100 | Estación intermedia |
| Calle 85 | Estación intermedia |
| Calle 76 | Punto donde nace el tramo expreso |
| Héroes | Punto donde nace el ramal alterno (NQS) |
| Calle 72 | Estación intermedia |
| Calle 63 | Estación intermedia |
| Calle 57 | Estación intermedia |
| Marly | Punto donde llega el tramo expreso |
| Calle 45 | Estación intermedia |
| Universidad Nacional | Destino principal de las pruebas |
| NQS - Calle 30 | Estación del ramal alterno (más largo) |

## Conexiones y costos (en minutos)

| Origen | Destino | Costo |
|---|---|---|
| Portal Norte | Toberín | 3 |
| Toberín | Calle 100 | 4 |
| Calle 100 | Calle 85 | 2 |
| Calle 85 | Calle 76 | 2 |
| Calle 76 | Héroes | 3 |
| Héroes | Calle 72 | 2 |
| Calle 72 | Calle 63 | 2 |
| Calle 63 | Calle 57 | 2 |
| Calle 57 | Marly | 2 |
| Marly | Calle 45 | 2 |
| Calle 45 | Universidad Nacional | 3 |
| Calle 76 | Marly *(tramo expreso)* | 5 |
| Héroes | NQS - Calle 30 *(ramal alterno)* | 8 |
| NQS - Calle 30 | Universidad Nacional | 9 |

Todas las conexiones son **bidireccionales**: si se puede ir de A a B,
también se puede volver de B a A con el mismo costo.

## Por qué se agregaron el tramo expreso y el ramal alterno

El enunciado original del proyecto plantea una única cadena lineal de
estaciones. Si esa fuera la única estructura del grafo, "encontrar la
mejor ruta" no tendría mucho sentido: solo habría un camino posible.

Por eso se agregaron dos elementos que obligan al sistema a **elegir**
entre varias opciones reales:

- Un **tramo expreso** (Calle 76 → Marly) que se salta estaciones
  intermedias, representando un servicio que no para en todas las
  estaciones.
- Un **ramal alterno** por la NQS (Héroes → NQS - Calle 30 →
  Universidad Nacional) que existe, pero es más largo.

Esto permite demostrar que el sistema realmente compara alternativas y
descarta las que no convienen, en vez de simplemente repetir la cadena
de estaciones del enunciado.
