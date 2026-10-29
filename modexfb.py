from utils import calcular_extremismo, calcular_esfuerzo

def modexFB(n, agentes, r_max):
    """
    Solución por Fuerza Bruta .
    Explora las 2^n combinaciones y retorna la mejor tripleta (E, Esfuerzo, Ext).
    """
    # TODO: 
    e_dummy = [0] * n
    esfuerzo = calcular_esfuerzo(agentes, e_dummy)
    ext = calcular_extremismo(agentes, e_dummy)
    return (e_dummy, esfuerzo, ext)