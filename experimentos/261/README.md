# 261 — Representación de la órbita de un satélite alrededor de la Tierra (2D)

## Qué es

Simulación estatonumérica de la órbita de un satélite alrededor de la Tierra en dos dimensiones, utilizando un modelo gravitatorio newtoniano.

El programa permite definir órbitas circulares o elípticas a partir de altitudes de perigeo y apogeo.

---

## Objetivo

Modelar y visualizar el comportamiento dinámico de un satélite en órbita terrestre.

---

## Cómo se ejecuta

Requisitos:
- Python 3.x
- Librerías: numpy, matplotlib

Instalación:
```console
pip install numpy matplotlib
```
Ejecución:
```console
python main.py <altitud1> <altitud2>
```
Parámetros:
```console
<altitud1> <altitud2> (elíptica)
```
```console
--circular <altitud> (circular)
```
> [!WARNING]
> Todas las altitudes en kilómetros por encima del nivel del mar (>0 km ASL).
