# 261 — Representación de órbita de un satélite alrededor de la Tierra (2D)

## Qué es

Simulación numérica de la órbita de un satélite alrededor de la Tierra en dos dimensiones, utilizando un modelo gravitatorio newtoniano.

El programa permite definir órbitas circulares o elípticas a partir de altitudes de perigeo y apogeo, y genera:

- Trayectoria orbital en el plano cartesiano
- Evolución de la altitud en función de la fase orbital
- Parámetros físicos relevantes (velocidad, período, excentricidad, etc.)

---

## Objetivo

Modelar y visualizar el comportamiento dinámico de un satélite en órbita terrestre, verificando:

- Conservación de la energía mecánica
- Consistencia con las leyes de Kepler
- Relación entre geometría orbital y magnitudes físicas

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
> [!WARNING]
> Todas las altitudes en kilómetros por encima del nivel del mar.

## Ejemplo (elíptica):
```console
python main.py 1000 2000
```
Resultado:
```console
Tipo de órbita: elíptica

Perigeo: 7371.0 km (altitud 1000 km) | v_p = 7583.39 m/s
Apogeo:  8371.0 km (altitud 2000 km) | v_a = 6677.48 m/s
Semieje mayor: 7871.0 km | Excentricidad: 0.0635
Período: 6950 s (115.8 min)
Gráfico guardado en orbita_satelite_trayectoria.png
Gráfico guardado en orbita_satelite_altitud_fase.png
```
<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/97f498b2-bc56-4282-860a-04759cfdb68d" />
<img width="400" height="300" alt="image" src="https://github.com/user-attachments/assets/f75592d0-0f43-4068-a57b-faf5d362364b" />

##Ejemplo (circular):
```console
python main.py --circular 2000
```
Resultado:
```console
Tipo de órbita: circular

Radio orbital: 8371.0 km
Velocidad orbital: 6900.24 m/s
Período: 7622 s (127.0 min)
Gráfico guardado en orbita_satelite_trayectoria.png
Gráfico guardado en orbita_satelite_altitud_fase.png
```
<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/1d4cad0a-85d0-4664-8175-67d1aae53d7b" />
<img width="400" height="300" alt="image" src="https://github.com/user-attachments/assets/a72bcb68-4066-42ee-a945-ba50dab9de7b" />
