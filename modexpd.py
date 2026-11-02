from utils import calcular_extremismo, calcular_esfuerzo, costo_moderar


def modexPD(n, agentes, r_max):
    """
    Solución por Programación Dinámica para ModEx.

    Idea: Ext = sqrt(S - G) / n, donde S = suma de op^2 * inf de todos los
    agentes (fijo) y G = suma de op^2 * inf de los agentes moderados.
    Como S y n son fijos y la raíz es creciente, minimizar el extremismo es
    lo mismo que MAXIMIZAR G sin pasarse del presupuesto: una mochila 0/1.
        - costo[i]    = esfuerzo de moderar al agente i   (peso)
        - ganancia[i] = op^2 * inf del agente i           (valor)

    Recurrencia (G(i, j) = mejor ganancia con los primeros i agentes y
    presupuesto j):
        G(0, j) = 0
        G(i, j) = G(i-1, j)                                   si costo[i-1] > j
        G(i, j) = max(G(i-1, j), ganancia[i-1] + G(i-1, j - costo[i-1]))  si no

    Retorna la tripleta (E, Esfuerzo(RS, E), Ext(Mod(RS, E))).
    """
    if n == 0:
        return ([], 0, 0.0)

    costo = []      # esfuerzo de moderar cada agente
    ganancia = []   # cuanto deja de aportar al extremismo si lo moderamos
    for i in range(n):
        op, rec, inf = agentes[i]
        costo.append(costo_moderar(agentes[i]))
        ganancia.append(op * op * inf)

    # No tiene sentido tener mas presupuesto que el costo de moderar a todos.
    # Esto acota la tabla: cap <= 300 * n, porque cada costo es <= 100*1*3.
    cap = min(r_max, sum(costo))

    # Para ahorrar memoria NO guardamos la tabla completa de valores G(i, j):
    # la fila i solo depende de la fila i-1, asi que basta con dos filas.
    anterior = [0] * (cap + 1)   # G(i-1, j)

    # Estructura para reconstruir la solucion (punto 3.3.4):
    # decision[i][j] = 1 si en el subproblema (i, j) conviene moderar al
    # agente i-1. bytearray usa 1 byte por celda (en vez de ~25 de una lista).
    decision = [None] * (n + 1)

    # Llenar la tabla fila por fila
    for i in range(1, n + 1):
        c = costo[i - 1]
        g = ganancia[i - 1]
        actual = anterior[:]            # opcion 1: no moderar -> G(i-1, j)
        dec = bytearray(cap + 1)        # todo en 0 al inicio
        for j in range(c, cap + 1):
            # opcion 2: moderarlo (solo si alcanza el presupuesto: j >= c)
            con = anterior[j - c] + g
            if con > actual[j]:
                actual[j] = con
                dec[j] = 1
        decision[i] = dec
        anterior = actual

    # Reconstruir E recorriendo las decisiones de atras hacia adelante
    E = [0] * n
    j = cap
    for i in range(n, 0, -1):
        if decision[i][j] == 1:
            E[i - 1] = 1
            j -= costo[i - 1]

    esfuerzo = calcular_esfuerzo(agentes, E)
    ext = calcular_extremismo(agentes, E)
    return (E, esfuerzo, ext)