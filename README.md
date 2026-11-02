# ModEx - Moderación de Extremismo de Opiniones en una Red Social

**Proyecto de curso:** Análisis y Diseño de Algoritmos II  
**Escuela de Ingeniería de Sistemas y Computación**  
**Universidad del Valle**  

## Integrantes

1. Carlos Manuel Villamil Grisales - 2257751
2. Sebastian Saldaña - 2410214
3. Sebastian Marulanda -
4. Mateo Noguera - 


## Descripción del proyecto

El proyecto **ModEx** aborda el problema combinatorio de reducir al máximo el
extremismo global en una red social, respetando un presupuesto límite de
esfuerzo (`R_max`).

Cada usuario o agente `i` de la red posee:

1. **Opinión (`o_i`):** número entero en `[-100, 100]`. Los valores alejados
   de `0` representan opiniones extremas; `0` indica neutralidad o moderación.
2. **Receptividad (`r_i`):** valor real en `[0.0, 1.0]` que cuantifica la
   facilidad para moderar al agente (`1.0` es la máxima receptividad y `0.0`
   la mínima).
3. **Influencia (`inf_i`):** valor real en `[1.0, 3.0]` que modela el impacto
   de la opinión del agente en toda la red.

El extremismo global de la red `RS` se calcula mediante:

```math
Ext(RS) = \frac{\sqrt{\sum_{i=0}^{n-1} (o_i^2 \times inf_i)}}{n}
```

Al moderar la opinión de un agente, esta cambia a `0`, con un esfuerzo
asociado de:

```math
Esfuerzo_i = \lceil |o_i| \times (1 - r_i) \times inf_i \rceil
```

El objetivo es determinar el vector binario de moderación
`E = <e_0, e_1, ..., e_{n-1}>`, de modo que el esfuerzo total sea menor o igual
que `R_max` y el extremismo `Ext(Mod(RS, E))` sea **mínimo**.

## Estructura del proyecto

El código está diseñado bajo una arquitectura modular desacoplada en Python 3
para facilitar el trabajo en equipo mediante Git y evitar conflictos de fusión:

```text
proyecto1-adaII-extremismo/
│
├── main.py              # Punto de entrada de la aplicación
├── gui.py               # Interfaz gráfica (Tkinter/ttk native UI)
├── modexfb.py           # Algoritmo de Fuerza Bruta (modexFB)
├── modexv.py            # Algoritmo Voraz (modexV)
├── modexpd.py           # Algoritmo de Programación Dinámica (modexPD)
├── utils.py             # Funciones matemáticas de extremismo y esfuerzo
├── generador.py         # Generador de casos de prueba aleatorios
├── README.md            # Documentación del proyecto
└── casos_prueba/        # Archivos .txt de prueba de entrada y salida
```

## Instalación y ejecución

### Requisitos

- Python 3.8 o superior.
- No se requiere la instalación de librerías externas mediante `pip`, ya que
  se utiliza únicamente la biblioteca estándar.

### Instrucciones de ejecución

1. Clona este repositorio o descarga el código fuente.
2. Abre una terminal en la raíz del proyecto.
3. Ejecuta el archivo principal:

   ```bash
   python main.py
   ```

   (En Windows, si `python` no responde, usa `py main.py`.)

> **Nota para usuarios de Linux (Ubuntu/Debian):** si Tkinter no está
> instalado, ejecuta `sudo apt-get install python3-tk`.

## Funciones de la interfaz

- **Cargar Archivo .txt:** lee una red social con el formato de entrada.
- **Generar Caso de Prueba:** pide `n` y, opcionalmente, `R_max` (si se deja
  vacío usa el 40 % del costo total de moderar a todos). Luego pide dónde
  guardar el archivo, genera una red aleatoria (sin semilla, por lo que no es
  reproducible), la guarda en ese `.txt` y la carga en la interfaz. Si se
  cancela el diálogo de guardado, no se genera nada.
- **Ejecutar:** corre el algoritmo elegido (FB, V o PD) y muestra el
  extremismo, el esfuerzo y qué agentes se moderan.
- **Verificación de la Solución:** después de ejecutar, recalcula el esfuerzo
  sumando los costos de los agentes moderados (los costos de la tabla, que se
  calculan con la misma función `costo_moderar` que usan los algoritmos) y el
  extremismo con su fórmula a partir de opinión e influencia. Comprueba que
  coincidan con lo que devolvió el algoritmo y que el esfuerzo sea menor o
  igual que `R_max`. No comprueba la optimalidad (eso se ve en "Comparar los
  3").
- **Comparar los 3:** ejecuta los tres algoritmos y muestra extremismo,
  esfuerzo, tiempo y la columna "¿Óptimo?".
- **Guardar Salida .txt:** escribe el resultado con el formato de salida.

## Formato de archivos de entrada y salida

### Archivo de entrada (`.txt`)

El archivo tiene exactamente `n + 2` líneas:

1. **Línea 1:** número de agentes `n` (entero).
2. **Líneas 2 a `n + 1`:** datos del agente `i`: opinión, receptividad e
   influencia.
3. **Línea `n + 2`:** presupuesto máximo de esfuerzo `R_max` (entero).

#### Ejemplo de entrada

```text
3
100, 0.5, 1
100, 0.1, 1
-10, 0.1, 1
55
```

### Archivo de salida (`.txt`)

El archivo tiene exactamente `n + 2` líneas:

1. **Línea 1:** extremismo resultante de la red (`Ext`).
2. **Línea 2:** esfuerzo total consumido.
3. **Líneas 3 a `n + 2`:** indicadores binarios de moderación para cada agente
   (`0` no moderado, `1` moderado).

## Módulos y algoritmos implementados

| Algoritmo | Función | Complejidad temporal | Complejidad espacial | Descripción |
|---|---|---:|---:|---|
| Fuerza bruta | `modexFB` | `Θ(n · 2^n)` | `O(n)` | Explora exhaustivamente las `2^n` combinaciones de decisiones posibles; cada una se evalúa en `O(n)`. Garantiza la solución óptima. |
| Voraz (Greedy) | `modexV` | `O(n log n)` | `O(n)` | Aplica una heurística de selección rápida basada en la mejor relación beneficio/esfuerzo. No garantiza el óptimo global. |
| Programación dinámica | `modexPD` | `O(n · R_max)` | `O(n · R_max)` | Construye la matriz de subproblemas y reconstruye el vector óptimo `E`. Garantiza la solución óptima eficientemente. |

