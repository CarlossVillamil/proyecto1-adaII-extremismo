from utils import calcular_extremismo, calcular_esfuerzo_individual

def modexV(n, agentes: list[tuple[float, float, float]], r_max):
    """
    Esta solución voraz modera la mayor cantidad de agentes
    posibles priorizando aquellos cuya relación costo-beneficio
    al moderar sea mayor
    """
    e_array = [0] * n

    agentes_ordenados = sorted(
        enumerate(agentes),
        key=lambda par: costo_beneficio(par[1]),
        reverse=True
    )

    esfuerzo_acumulado = 0

    for indice, agente in agentes_ordenados:

        esfuerzo_actual = calcular_esfuerzo_individual(agente)

        if esfuerzo_acumulado + esfuerzo_actual > r_max:
            continue

        e_array[indice] = 1

        esfuerzo_acumulado += esfuerzo_actual

    return (e_array, esfuerzo_acumulado, calcular_extremismo(agentes, e_array))


def costo_beneficio(agente):
    """
    Calcula la relación costo beneficio de moderar un agente.
    Esto se hizo también en clase con el problema mochila fraccionario.
    """

    costo = calcular_esfuerzo_individual(agente)

    beneficio = agente[0]**2 * agente[2]

    # Evitamos dividir entre cero cuando un agente tiene una receptividad de 1
    # Lo priorizamos indicando uuna relacion costo-beneficio muy grande
    return beneficio/costo if costo != 0 else float("inf")
