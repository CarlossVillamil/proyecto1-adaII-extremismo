import math

def calcular_extremismo(agentes, estrategia):
    """
    Calcula el extremismo de la red dada una estrategia de moderación E.
    agentes: lista de tuplas (op, rec, inf)
    estrategia: lista de 0s y 1s de tamaño n
    """
    n = len(agentes)
    suma = 0.0
    for i in range(n):
        op, rec, inf = agentes[i]
        # Si e_i == 1, la opinión pasa a 0; si e_i == 0, se mantiene op
        op_nueva = 0 if estrategia[i] == 1 else op
        suma += (op_nueva ** 2) * inf
        
    return math.sqrt(suma) / n

def calcular_esfuerzo(agentes, estrategia):
    """
    Calcula el esfuerzo total necesario para aplicar la estrategia E.
    """
    esfuerzo_total = 0
    for i in range(len(agentes)):
        if estrategia[i] == 1:
            op, rec, inf = agentes[i]
            # Ceil(|op - 0| * (1 - rec) * inf)
            costo_i = math.ceil(abs(op) * (1 - rec) * inf)
            esfuerzo_total += costo_i
    return esfuerzo_total