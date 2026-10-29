from utils import calcular_extremismo, calcular_esfuerzo

def modexFB(n, agentes, r_max):
    """
    Solución por Fuerza Bruta para el problema ModEx (ADA II).
    Explora exhaustivamente las 2^n combinaciones posibles y retorna
    la tripleta de la mejor estrategia aplicable: (E, Esfuerzo, Ext).
    """
    mejor_E = [0] * n
    mejor_esfuerzo = calcular_esfuerzo(agentes, mejor_E)
    mejor_ext = calcular_extremismo(agentes, mejor_E)
    
    # El espacio total de búsqueda para n agentes es de 2^n combinaciones.
    total_combinaciones = 2 ** n
    
    for i in range(total_combinaciones):
        # Generamos la representación binaria de tamaño n para el número i.
        # Ejemplo: para n=3 y i=5 -> bin(5)[2:] es '101'
        combinacion_str = bin(i)[2:].zfill(n)
        
        # Convertimos la cadena de caracteres en el vector binario de decisiones E
        E_actual = [int(bit) for bit in combinacion_str]
        
        # 1. Calculamos el esfuerzo total necesario para aplicar la estrategia E
        esfuerzo_actual = calcular_esfuerzo(agentes, E_actual)
        
        # 2. Verificamos la aplicabilidad de la estrategia: Esfuerzo <= R_max
        if esfuerzo_actual <= r_max:
            # 3. Calculamos el extremismo resultante de la red social Mod(RS, E)
            ext_actual = calcular_extremismo(agentes, E_actual)
            
            # 4. Buscamos el mínimo extremismo. Si hay un empate en extremismo,
            # o si encontramos una estrategia con menor extremismo, la actualizamos.
            if ext_actual < mejor_ext:
                mejor_ext = ext_actual
                mejor_esfuerzo = esfuerzo_actual
                mejor_E = E_actual

    # Retornamos la tripleta requerida por la especificación del proyecto
    return (mejor_E, mejor_esfuerzo, mejor_ext)