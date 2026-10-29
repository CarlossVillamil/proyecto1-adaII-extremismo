# ModEx - Moderación de Extremismo de Opiniones en una Red Social

**Proyecto de curso:** Análisis y Diseño de Algoritmos II  
**Escuela de Ingeniería de Sistemas y Computación**  
**Universidad del Valle**  

## Integrantes

1. Carlos Manuel Villamil Grisales - 2257751
2. Sebastian Saldaña -
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
proyecto_modex/
│
├── main.py              # Punto de entrada de la aplicación
├── gui.py               # Interfaz gráfica (Tkinter/ttk native UI)
├── modexfb.py           # Algoritmo de Fuerza Bruta (modexFB)
├── modexv.py            # Algoritmo Voraz (modexV)
├── modexpd.py           # Algoritmo de Programación Dinámica (modexPD)
├── utils.py             # Funciones matemáticas de extremismo y esfuerzo
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

> **Nota para usuarios de Linux (Ubuntu/Debian):** si Tkinter no está
> instalado, ejecuta `sudo apt-get install python3-tk`.

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
| Fuerza bruta | `modexFB` | `O(2^n)` | `O(n)` | Explora exhaustivamente las `2^n` combinaciones de decisiones posibles. Garantiza la solución óptima. |
| Voraz (Greedy) | `modexV` | `O(n log n)` | `O(n)` | Aplica una heurística de selección rápida basada en la mejor relación beneficio/esfuerzo. No garantiza el óptimo global. |
| Programación dinámica | `modexPD` | `O(n · R_max)` | `O(n · R_max)` | Construye la matriz de subproblemas y reconstruye el vector óptimo `E`. Garantiza la solución óptima eficientemente. |

