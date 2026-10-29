from utils import calcular_extremismo, calcular_esfuerzo

def modexPD(n, agentes, r_max):
    """
    Solución por Programación Dinámica .
    """
    # TODO
    e_dummy = [0] * n
    esfuerzo = calcular_esfuerzo(agentes, e_dummy)
    ext = calcular_extremismo(agentes, e_dummy)
    return (e_dummy, esfuerzo, ext)