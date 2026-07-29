import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys

# Constantes físicas
G = 6.674e-11           # constante de gravitación universal [m^3 kg^-1 s^-2]
M_TIERRA = 5.972e24     # masa de la Tierra [kg]
R_TIERRA = 6.371e6      # radio de la Tierra [m]
MU = G * M_TIERRA       # parámetro gravitacional estándar [m^3/s^2]

# Entrada de argumentos
args = sys.argv[1:]

if len(args) == 0:
    print("Uso:")
    print("  python main.py <h1> <h2>          (altitudes en km)")
    print("  python main.py --circular <h>     (órbita circular)")
    sys.exit(1)

# circular
if args[0] == "--circular":
    if len(args) != 2:
        print("Error: modo circular requiere una altitud.")
        sys.exit(1)

    h = float(args[1])
    hp = h
    ha = h

# general
else:
    if len(args) != 2:
        print("Error: debes ingresar dos altitudes (perigeo y apogeo).")
        sys.exit(1)

    h1 = float(args[0])
    h2 = float(args[1])

    if h1 < 0 or h2 < 0:
        print("Error: las altitudes deben ser >= 0.")
        sys.exit(1)

    hp = min(h1, h2)
    ha = max(h1, h2)

# Conversión a metros
altitud_perigeo = hp * 1e3
altitud_apogeo = ha * 1e3

# Tipo de órbita
if hp == ha:
    tipo_orbita = "circular"
else:
    tipo_orbita = "eliptica"

# Radios orbitales (medidos desde el centro de la Tierra)
r_p = R_TIERRA + altitud_perigeo   # radio de perigeo
r_a = R_TIERRA + altitud_apogeo    # radio de apogeo

# lo demás se deriva geométricamente de r_p y r_a:
a = (r_p + r_a) / 2                # semieje mayor
e = (r_a - r_p) / (r_a + r_p)      # excentricidad

# Velocidad en el perigeo (vis-viva)
# En el perigeo/apogeo la velocidad es puramente tangencial.
v_p = np.sqrt(MU * (2 / r_p - 1 / a))
v_a = np.sqrt(MU * (2 / r_a - 1 / a))  # (informativo)

# Arrancamos la simulación en el perigeo, sobre el eje x,
# moviéndose en +y (sentido antihorario).
x0, y0 = r_p, 0.0
vx0, vy0 = 0.0, v_p

r0 = r_p # (usado más tarde)

estado0 = np.array([x0, y0, vx0, vy0])

# Ecuaciones de movimiento
def derivadas(estado, mu=MU):
    """
    Devuelve d(estado)/dt = [vx, vy, ax, ay]
    a = -mu * r_vec / |r|^3   (gravitación de Newton)
    """
    x, y, vx, vy = estado
    r = np.hypot(x, y)
    ax = -mu * x / r**3
    ay = -mu * y / r**3
    return np.array([vx, vy, ax, ay])


def paso_rk4(estado, dt):
    """Un paso de integración Runge-Kutta de orden 4."""
    k1 = derivadas(estado)
    k2 = derivadas(estado + 0.5 * dt * k1)
    k3 = derivadas(estado + 0.5 * dt * k2)
    k4 = derivadas(estado + dt * k3)
    return estado + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

# Simulación
periodo_estimado = 2 * np.pi * np.sqrt(a**3 / MU)    # período kepleriano exacto (con el semieje mayor)
t_total = 2.2 * periodo_estimado                     # simulamos poco más de una vuelta
n_pasos = 20000
dt = t_total / n_pasos

estados = np.zeros((n_pasos + 1, 4))
estados[0] = estado0

for i in range(n_pasos):
    estados[i + 1] = paso_rk4(estados[i], dt)

x, y = estados[:, 0], estados[:, 1]
vx, vy = estados[:, 2], estados[:, 3]
r = np.hypot(x, y)

# energía específica orbital (debe mantenerse ~constante)
energia = 0.5 * (vx**2 + vy**2) - MU / r
deriva_energia = (energia.max() - energia.min()) / abs(energia[0])

if tipo_orbita == "circular":
    print(f"Altitud: {altitud_perigeo/1e3:.0f} km")
    print("\nTipo de órbita: circular\n")
    print(f"Radio orbital: {r_p/1e3:.1f} km")
    print(f"Velocidad orbital: {v_p:.2f} m/s")
    print(f"Período: {periodo_estimado:.0f} s ({periodo_estimado/60:.1f} min)")
else:
    print("\nTipo de órbita: elíptica\n")
    print(f"Perigeo: {r_p/1e3:.1f} km (altitud {altitud_perigeo/1e3:.0f} km) | v_p = {v_p:.2f} m/s")
    print(f"Apogeo:  {r_a/1e3:.1f} km (altitud {altitud_apogeo/1e3:.0f} km) | v_a = {v_a:.2f} m/s")
    print(f"Semieje mayor: {a/1e3:.1f} km | Excentricidad: {e:.4f}")
    print(f"Período: {periodo_estimado:.0f} s ({periodo_estimado/60:.1f} min)")

# Visualización
altura = (r - R_TIERRA) / 1e3              # altitud sobre la superficie [km]
fase = np.degrees(np.arctan2(y, x)) % 360  # ángulo de fase orbital [0, 360)

# trayectoria 2D
fig1, ax = plt.subplots(figsize=(8, 8))

# Tierra a escala
tierra = patches.Circle((0, 0), R_TIERRA / 1e3, color="#2b6cb0", zorder=3, label="Tierra")
ax.add_patch(tierra)

# Trayectoria del satélite
ax.plot(x / 1e3, y / 1e3, color="#e53e3e", linewidth=1.3, label="Trayectoria del satélite")

# Posición inicial
ax.plot(x[0] / 1e3, y[0] / 1e3, "o", color="black", markersize=5, label="Posición inicial")

margen = 1.1
lim = max(np.max(np.abs(x)), np.max(np.abs(y))) / 1e3 * margen
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)

ax.set_aspect("equal")
ax.set_xlabel("x [km]")
ax.set_ylabel("y [km]")
ax.set_title("Órbita de un satélite alrededor de la Tierra (2D, RK4)")
ax.legend(loc="upper right")
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("orbita_satelite_trayectoria.png", dpi=150)
print("Gráfico guardado en orbita_satelite_trayectoria.png")

# altitud vs fase orbital
fig2, ax2 = plt.subplots(figsize=(8, 6))

ax2.plot(fase, altura, ".", color="#38a169", markersize=1.5)
ax2.set_xlabel("Fase orbital [°]")
ax2.set_ylabel("Altitud sobre la superficie [km]")
ax2.set_title("Altitud vs. fase orbital")
ax2.set_xlim(0, 360)
ax2.set_xticks(np.arange(0, 361, 45))
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("orbita_satelite_altitud_fase.png", dpi=150)
print("Gráfico guardado en orbita_satelite_altitud_fase.png")