from utils import calcular_extremismo, calcular_esfuerzo

def modexV(n, agentes, r_max):
    """
    Solución Voraz .
    """
    # TODO: 
    e_dummy = [0] * n
    esfuerzo = calcular_esfuerzo(agentes, e_dummy)
    ext = calcular_extremismo(agentes, e_dummy)
    return (e_dummy, esfuerzo, ext)