================================================================================
ModEx - Moderacion de Extremismo de Opiniones en una Red Social
================================================================================

Proyecto de curso: Analisis y Diseno de Algoritmos II
Escuela de Ingenieria de Sistemas y Computacion
Universidad del Valle
Profesor: Jesus Alexander Aranda
Monitor: Samuel Galindo

--------------------------------------------------------------------------------
1. Integrantes del proyecto
--------------------------------------------------------------------------------
1. Carlos Manuel Villamil Grisales - 2257751
2. Sebastian Saldana - 2410214
3. Sebastian Marulanda - 2410241
4. Mateo Noguera - 2342673

--------------------------------------------------------------------------------
2. Descripcion del problema ModEx
--------------------------------------------------------------------------------
ModEx aborda el problema de minimizar el extremismo global de una red social
de n agentes, donde cada agente i posee una opinion entera en [-100, 100],
receptividad en [0, 1] e influencia en [1, 3]. Se dispone de un presupuesto
maximo de esfuerzo R_max. Al moderar a un agente, su opinion pasa a 0 con un
costo entero ceil(|opinion| * (1 - receptividad) * influencia). El objetivo es
determinar el subconjunto de agentes a moderar que minimice el extremismo global
sin exceder R_max.

--------------------------------------------------------------------------------
3. Estructura y lista de archivos del repositorio
--------------------------------------------------------------------------------
- main.py: Punto de entrada de la aplicacion que inicializa la interfaz grafica.
- gui.py: Modulo de interfaz grafica (Tkinter/ttk) y lectura/escritura de archivos.
- modexfb.py: Implementacion del algoritmo de Fuerza Bruta (modexFB).
- modexv.py: Implementacion del algoritmo Voraz heuristico (modexV).
- modexpd.py: Implementacion del algoritmo de Programacion Dinamica (modexPD).
- utils.py: Funciones matematicas de calculo de extremismo y costo de moderacion.
- generador.py: Generador de casos de prueba y redes sociales aleatorias.
- pruebas.py: Suite de pruebas automaticas con recalculacion independiente.
- Readme.txt: Descripcion general, manual de usuario e instrucciones de ejecucion.
- casos_prueba/: Directorio con casos de prueba en formato .txt.

--------------------------------------------------------------------------------
4. Se agrega al empaquetar
--------------------------------------------------------------------------------
Al momento de generar el archivo comprimido final (.zip) se debe incluir:
- Informe del proyecto en formato PDF: Informe de Proyecto - Analisis y Diseno de Algoritmos II.pdf

--------------------------------------------------------------------------------
5. Requisitos del sistema
--------------------------------------------------------------------------------
- Python 3.8 o superior con soporte para Tkinter.
- En Windows y macOS, Tkinter se incluye por defecto con el instalador oficial.
- En distribuciones Linux (Ubuntu/Debian), si no esta instalado:
    sudo apt-get install python3-tk
- No se requieren librerias externas ni ejecucion de "pip install".

--------------------------------------------------------------------------------
6. Instrucciones de ejecucion
--------------------------------------------------------------------------------
Abrir una terminal en la raiz del proyecto y ejecutar:
    python main.py (en Windows, si python no responde, usa py main.py)

--------------------------------------------------------------------------------
7. Formatos de archivos de entrada y salida
--------------------------------------------------------------------------------
Formato de entrada (.txt):
- Linea 1: n (numero de agentes, entero)
- Lineas 2 a n+1: opinion, receptividad, influencia (para cada agente)
- Linea n+2: R_max (presupuesto maximo de esfuerzo, entero)

Ejemplo de entrada (casos_prueba/ejemplo1.txt):
3
100, 0.5, 1
100, 0.1, 1
-10, 0.1, 1
55

Formato de salida (.txt):
- Linea 1: extremismo final resultante de la red (numero real)
- Linea 2: esfuerzo total consumido (numero entero)
- Lineas 3 a n+2: 1 si el agente i fue moderado, 0 en caso contrario

Ejemplo de salida correspondiente a ejemplo1.txt:
33.4995854037363
50
1
0
0

--------------------------------------------------------------------------------
8. Uso de la interfaz grafica en 5 pasos
--------------------------------------------------------------------------------
Paso 1: Cargar datos. Presionar "Cargar Archivo .txt" para seleccionar un archivo
        de entrada, o "Generar Caso de Prueba" para crear y guardar uno nuevo.
Paso 2: Inspeccionar red. Revisar en la tabla los agentes cargados con su opinion,
        receptividad, influencia, costo de moderacion y aporte o^2*inf.
Paso 3: Seleccionar algoritmo. Elegir Fuerza Bruta (FB), Voraz (V) o Programacion
        Dinamica (PD) en el panel de opciones.
Paso 4: Ejecutar y verificar. Presionar "Ejecutar". Se mostraran el extremismo y
        esfuerzo resultantes, se resaltaran en verde los moderados y el panel
        "Verificacion de la Solucion" comprobara consistencia y aplicabilidad.
Paso 5: Comparar o exportar. Presionar "Comparar los 3" para ver una tabla
        comparativa de tiempos, esfuerzo y optimalidad, o presionar
        "Guardar Salida .txt" para exportar el resultado con el formato oficial.

--------------------------------------------------------------------------------
9. Ejecucion de pruebas automaticas
--------------------------------------------------------------------------------
Para ejecutar la suite de pruebas automaticas:
    py pruebas.py

Opciones disponibles:
- py pruebas.py --fb-max 20
  Permite evaluar Fuerza Bruta en casos con hasta n=20 agentes (por defecto n<=15).
- py pruebas.py --aleatorios 50
  Permite variar el numero de casos aleatorios evaluados (por defecto 30).

Las pruebas validan que FB y PD coincidan en extremismo, que ningun algoritmo
exceda R_max, que los valores reportados coincidan con el recalculo independiente
y que el algoritmo Voraz nunca supere al optimo.

--------------------------------------------------------------------------------
10. Descripcion de archivos en casos_prueba/
--------------------------------------------------------------------------------
- ejemplo1.txt: Ejemplo 1 del enunciado oficial (n=3, R_max=55).
- ejemplo2.txt: Ejemplo 2 del enunciado oficial (n=3, R_max=35).
- borde_n1.txt: Caso borde con un unico agente en la red (n=1, R_max=40).
- borde_rmax0.txt: Caso borde con presupuesto cero (R_max=0); no permite esfuerzo.
- borde_opiniones_cero.txt: Caso borde donde todos los agentes tienen opinion 0.
- borde_presupuesto_total.txt: Caso borde donde R_max excede el costo de toda la red.
- aleatorio_n8.txt: Caso aleatorio de dimension reducida (n=8, R_max=150).
- aleatorio_n10.txt: Caso aleatorio mediano (n=10, R_max=250).
- aleatorio_n15.txt: Caso aleatorio en el limite de ejecucion rapida de FB (n=15, R_max=400).
- aleatorio_n20.txt: Caso aleatorio de n=20 (R_max=600); requiere --fb-max 20.
- grande_n1000.txt: Caso de gran escala (n=1000, R_max=20000) para medir PD y Voraz.
- voraz_falla1.txt: Contraejemplo donde la heuristica voraz no alcanza el optimo (n=3).
- voraz_contraejemplo.txt: Contraejemplo donde el voraz falla: un agente barato de alta razon bloquea al agente de mayor aporte (n=2, R_max=99).
- voraz_falla2.txt: Caso disenado para enganar a un voraz que elige por menor costo. Nuestro voraz (por razon beneficio/costo) SI encuentra el optimo aqui (n=3, R_max=60).

--------------------------------------------------------------------------------
11. Complejidad teorica de los algoritmos
--------------------------------------------------------------------------------
- Fuerza Bruta (modexFB):
  Complejidad temporal: Theta(n * 2^n).
  Complejidad espacial: O(n).
  Explora las 2^n combinaciones binarias de decision; evaluar el esfuerzo y
  extremismo de cada combinacion toma O(n). Garantiza la solucion optima.

- Algoritmo Voraz (modexV):
  Complejidad temporal: O(n log n).
  Complejidad espacial: O(n).
  Ordena los agentes por la razon beneficio/costo (o^2 * inf / costo_moderar)
  en tiempo O(n log n) y selecciona vorazmente mientras haya presupuesto.
  Es rapido pero no garantiza la solucion optima global.

- Programacion Dinamica (modexPD):
  Complejidad temporal: Theta(n * R).
  Complejidad espacial: Theta(n * R).
  Donde R = min(R_max, suma_costos). Modela el problema como una mochila 0/1
  optimizada en memoria con tabla de decisiones compacta de 1 byte por celda
  y reconstruccion hacia atras en O(n). Garantiza la solucion optima de
  manera eficiente.

