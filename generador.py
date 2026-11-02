import random

from utils import costo_moderar


def generar_caso(n, r_max=None, semilla=None):
    """
    Genera una red social aleatoria con n agentes.
    - opinion:      entero en [-100, 100]
    - receptividad: real en [0, 1] (2 decimales)
    - influencia:   real en [1, 3] (2 decimales)
    Si r_max es None, se toma aprox. el 40% del costo de moderar a todos,
    para que el presupuesto no alcance para todos (caso interesante).
    Retorna (n, agentes, r_max).
    """
    rnd = random.Random(semilla)
    agentes = []
    for _ in range(n):
        op = rnd.randint(-100, 100)
        rec = round(rnd.uniform(0, 1), 2)
        inf = round(rnd.uniform(1, 3), 2)
        agentes.append((op, rec, inf))

    if r_max is None:
        total = sum(costo_moderar(a) for a in agentes)
        r_max = int(total * 0.4)

    return n, agentes, r_max


def guardar_caso(ruta, n, agentes, r_max):
    """Escribe el caso con el formato de entrada del enunciado (n + 2 lineas)."""
    with open(ruta, "w") as f:
        f.write(f"{n}\n")
        for op, rec, inf in agentes:
            f.write(f"{op},{rec},{inf}\n")
        f.write(f"{r_max}\n")


if __name__ == "__main__":
    # Uso por consola:  python generador.py <n> [r_max] [archivo_salida]
    import sys

    if len(sys.argv) < 2:
        print("Uso: python generador.py <n> [r_max] [archivo_salida]")
        sys.exit(1)

    n = int(sys.argv[1])
    r_max = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] != "-" else None
    ruta = sys.argv[3] if len(sys.argv) > 3 else f"caso_n{n}.txt"

    n, agentes, r_max = generar_caso(n, r_max)
    guardar_caso(ruta, n, agentes, r_max)
    print(f"Caso generado en {ruta} (n={n}, R_max={r_max})")