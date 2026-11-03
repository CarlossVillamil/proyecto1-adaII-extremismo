"""
pruebas.py - Pruebas automaticas de ModEx (ADA II).

Ejecuta modexFB, modexV y modexPD sobre los archivos de casos_prueba/ y sobre
casos aleatorios pequenos, y verifica:
  1. FB y PD dan el mismo extremismo (ambos son optimos).
  2. El esfuerzo reportado coincide con un recalculo independiente y es <= R_max.
  3. El extremismo reportado coincide con un recalculo independiente.
  4. El voraz nunca supera al optimo.

El esfuerzo y el extremismo se recalculan AQUI con la formula del enunciado,
sin usar utils.py, para que la comprobacion sea independiente del codigo
que se esta probando.

Uso:
    py pruebas.py                  (FB solo hasta n <= 15)
    py pruebas.py --fb-max 18      (permite FB con mas agentes; mas lento)
    py pruebas.py --aleatorios 50  (cambia la cantidad de casos aleatorios)
"""
import argparse
import glob
import math
import os
import random
import time

from gui import leer_entrada
from modexfb import modexFB
from modexv import modexV
from modexpd import modexPD

TOL = 1e-9


def costo(o, r, inf):
    """Costo de moderar un agente: techo de |o|*(1-r)*inf (con el mismo
    redondeo a 9 decimales que usa el proyecto para evitar ruido de float)."""
    return math.ceil(round(abs(o) * (1 - r) * inf, 9))


def esfuerzo_ind(agentes, E):
    return sum(costo(*a) for a, e in zip(agentes, E) if e)


def extremismo_ind(agentes, E):
    s = sum(0 if e else o * o * inf for (o, _r, inf), e in zip(agentes, E))
    return math.sqrt(s) / len(agentes)


def generar_aleatorio(rng, n):
    agentes = [(rng.randint(-100, 100),
                round(rng.uniform(0, 1), 1),
                round(rng.uniform(1, 3), 1)) for _ in range(n)]
    total = sum(costo(*a) for a in agentes)
    return n, agentes, rng.randint(0, total)


def ejecutar(f, n, agentes, r_max):
    t0 = time.perf_counter()
    E, esf, ext = f(n, agentes, r_max)
    return list(E), esf, ext, time.perf_counter() - t0


def probar_caso(nombre, n, agentes, r_max, fb_max, filas, fallos):
    res = {}
    algoritmos = [("V", modexV), ("PD", modexPD)]
    if n <= fb_max:
        algoritmos.insert(0, ("FB", modexFB))
    for clave, f in algoritmos:
        try:
            res[clave] = ejecutar(f, n, agentes, r_max)
        except Exception as exc:  # noqa: BLE001
            fallos.append(f"{nombre}: {clave} lanzo {type(exc).__name__}: {exc}")
            return

    for clave, (E, esf, ext, _t) in res.items():
        if len(E) != n:
            fallos.append(f"{nombre}: {clave} devolvio E de longitud {len(E)} (n={n})")
            continue
        esf_real = esfuerzo_ind(agentes, E)
        if esf != esf_real:
            fallos.append(f"{nombre}: {clave} reporta esfuerzo {esf}, recalculo {esf_real}")
        if esf_real > r_max:
            fallos.append(f"{nombre}: {clave} no es aplicable ({esf_real} > R_max {r_max})")
        ext_real = extremismo_ind(agentes, E)
        if abs(ext - ext_real) > TOL:
            fallos.append(f"{nombre}: {clave} reporta extremismo {ext}, recalculo {ext_real}")

    ext_pd = res["PD"][2]
    if "FB" in res and abs(res["FB"][2] - ext_pd) > TOL:
        fallos.append(f"{nombre}: FB ({res['FB'][2]}) y PD ({ext_pd}) difieren")
    optimo = res["FB"][2] if "FB" in res else ext_pd
    if res["V"][2] < optimo - TOL:
        fallos.append(f"{nombre}: el voraz ({res['V'][2]}) supera al optimo ({optimo})")

    voraz_opt = "Si" if abs(res["V"][2] - optimo) <= TOL else "No"
    fb = res.get("FB")
    filas.append((nombre, n, r_max,
                  f"{fb[2]:.4f}" if fb else "-",
                  f"{res['V'][2]:.4f}", f"{ext_pd:.4f}",
                  res["PD"][1],
                  f"{fb[3]:.4f}" if fb else "-",
                  f"{res['V'][3]:.4f}", f"{res['PD'][3]:.4f}",
                  voraz_opt))


def imprimir_tabla(filas):
    enc = ("caso", "n", "R_max", "ext_FB", "ext_V", "ext_PD", "esf_PD",
           "t_FB(s)", "t_V(s)", "t_PD(s)", "V optimo?")
    datos = [enc] + [tuple(str(c) for c in f) for f in filas]
    anchos = [max(len(r[i]) for r in datos) for i in range(len(enc))]
    for k, fila in enumerate(datos):
        print("  ".join(c.ljust(w) for c, w in zip(fila, anchos)))
        if k == 0:
            print("  ".join("-" * w for w in anchos))


def main():
    ap = argparse.ArgumentParser(description="Pruebas automaticas de ModEx")
    ap.add_argument("--fb-max", type=int, default=15,
                    help="n maximo para ejecutar fuerza bruta (default 15)")
    ap.add_argument("--aleatorios", type=int, default=30,
                    help="cantidad de casos aleatorios (default 30)")
    ap.add_argument("--semilla", type=int, default=2026,
                    help="semilla para los casos aleatorios (default 2026)")
    ap.add_argument("--carpeta", default="casos_prueba",
                    help="carpeta con los .txt de entrada")
    args = ap.parse_args()

    filas, fallos = [], []

    archivos = sorted(glob.glob(os.path.join(args.carpeta, "*.txt")))
    if not archivos:
        print(f"Aviso: no hay .txt en '{args.carpeta}'.")
    for ruta in archivos:
        nombre = os.path.basename(ruta)
        try:
            n, agentes, r_max = leer_entrada(ruta)
        except Exception as exc:  # noqa: BLE001
            fallos.append(f"{nombre}: no se pudo leer ({type(exc).__name__}: {exc})")
            continue
        probar_caso(nombre, n, agentes, r_max, args.fb_max, filas, fallos)

    rng = random.Random(args.semilla)
    for k in range(args.aleatorios):
        n = rng.randint(1, 12)
        _n, agentes, r_max = generar_aleatorio(rng, n)
        probar_caso(f"aleatorio_{k + 1}", n, agentes, r_max, args.fb_max, filas, fallos)

    imprimir_tabla(filas)
    print()
    sub = [f for f in filas if f[0].endswith(".txt")]
    no_opt = [f[0] for f in sub if f[-1] == "No"]
    print(f"Casos ejecutados: {len(filas)} ({len(sub)} de archivo, "
          f"{len(filas) - len(sub)} aleatorios)")
    print(f"El voraz no fue optimo en: {', '.join(no_opt) if no_opt else 'ninguno de los archivos'}")
    if fallos:
        print(f"\nFALLARON {len(fallos)} COMPROBACIONES:")
        for f in fallos:
            print("  -", f)
        raise SystemExit(1)
    print("\nTodas las comprobaciones pasaron.")


if __name__ == "__main__":
    main()