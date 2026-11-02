# ModEx: Moderación del Extremismo de Opiniones en una Red Social
## Informe de Proyecto - Análisis y Diseño de Algoritmos II

---

### Portada y Datos del Proyecto

- **Institución:** Universidad del Valle
- **Facultad:** Facultad de Ingeniería
- **Escuela:** Escuela de Ingeniería de Sistemas y Computación
- **Curso:** Análisis y Diseño de Algoritmos II
- **Profesor:** Jesús Alexander Aranda
- **Monitor:** Samuel Galindo
- **Fecha de entrega:** [COMPLETAR: ej. 10 de noviembre de 2026]

#### Integrantes del Grupo
1. Carlos Manuel Villamil Grisales - Código: 2257751
2. Sebastian Saldaña - Código: 2410214
3. Sebastian Marulanda - Código: [COMPLETAR]
4. Mateo Noguera - Código: [COMPLETAR]

---

## 1. Introducción

> **Responsable:** Integrante D (Integración)  
> **Qué pide el enunciado:** Secciones 1, 2.1 y 2.2 del enunciado del proyecto.  
> **Hechos verificados del código:** Funciones `costo_moderar` y `calcular_extremismo` en [utils.py:4-29](file:///utils.py#L4-L29). Representación de la red como lista de tuplas `(op, rec, inf)` y presupuesto entero `r_max`.

El problema **ModEx** modela una red social $RS = \langle AG, R_{\max} \rangle$ compuesta por una secuencia de $n$ agentes $AG = \langle a_0, a_1, \dots, a_{n-1} \rangle$, donde cada agente $i$ posee una opinión entera $o_i \in [-100, 100]$, un nivel de receptividad real $r_i \in [0.0, 1.0]$ y un nivel de influencia real $\text{inf}_i \in [1.0, 3.0]$. La red cuenta con un presupuesto entero de esfuerzo $R_{\max} \ge 0$. El extremismo global de la red social se calcula mediante la fórmula:

$$Ext(RS) = \frac{\sqrt{\sum_{i=0}^{n-1} (o_i^2 \cdot \text{inf}_i)}}{n}$$

Una estrategia de moderación es un vector binario $E = \langle e_0, e_1, \dots, e_{n-1} \rangle$ con $e_i \in \{0, 1\}$. Si $e_i = 1$, la opinión del agente pasa a $0$, consumiendo un esfuerzo individual dado por:

$$\text{Esfuerzo}_i = \lceil |o_i| \cdot (1 - r_i) \cdot \text{inf}_i \rceil$$

El esfuerzo total de aplicar la estrategia $E$ es la suma de los esfuerzos de los agentes moderados:

$$\text{Esfuerzo}(RS, E) = \sum_{i=0}^{n-1} e_i \cdot \lceil |o_i| \cdot (1 - r_i) \cdot \text{inf}_i \rceil$$

Una estrategia es **aplicable** si $\text{Esfuerzo}(RS, E) \le R_{\max}$. El objetivo combinatorio de ModEx consiste en encontrar una estrategia aplicable $E$ tal que el extremismo resultante de la red modificada, $Ext(\text{Mod}(RS, E))$, sea **mínimo**.

#### Preguntas guía para el redactor:
1. ¿Cuál es la motivación social y computacional de abordar la moderación de opiniones extremas con un presupuesto acotado?
2. ¿Por qué la opinión neutral se modela con el valor 0 y cómo impacta esto en la suma cuadrática del extremismo?
3. ¿Cómo influyen los parámetros de receptividad e influencia en el costo de convencer a un agente?

**Texto a redactar:**  
[COMPLETAR: Párrafo de contextualización del problema en el ámbito de redes sociales y justificación del modelo matemático.]

---

## 2. Solución por Fuerza Bruta

> **Responsable:** Integrante A  
> **Qué pide el enunciado:** Sección 3.1. Subsecciones 3.1.1 (Complejidad: orden y argumentación) y 3.1.2 (Corrección: argumentación de si siempre da la respuesta correcta).  
> **Hechos verificados del código:** Función `modexFB` en [modexfb.py:3-40](file:///modexfb.py#L3-L40). Genera $2^n$ cadenas binarias con `bin(i)[2:].zfill(n)`. Para cada combinación calcula esfuerzo en [utils.py:31-39](file:///utils.py#L31-L39) ($O(n)$) y extremismo en [utils.py:14-29](file:///utils.py#L14-L29) ($O(n)$). Actualiza si `ext_actual < mejor_ext` (estricto).

### 2.1. Descripción del algoritmo
El algoritmo de Fuerza Bruta (`modexFB`) explora de manera exhaustiva el espacio total de soluciones posibles. Dado que para cada uno de los $n$ agentes existen dos decisiones posibles (no moderar, $e_i = 0$; o moderar, $e_i = 1$), el espacio de búsqueda contiene exactamente $2^n$ vectores binarios de decisión.

El algoritmo inicializa la mejor solución con la estrategia nula $E = \langle 0, 0, \dots, 0 \rangle$, cuyo esfuerzo es 0 (siempre aplicable dado $R_{\max} \ge 0$). Luego, itera a través de los enteros $i \in [0, 2^n - 1]$, convirtiendo cada entero en su representación binaria de tamaño $n$. Para cada combinación, evalúa si el esfuerzo acumulado no excede $R_{\max}$; de ser aplicable, calcula el extremismo resultante y actualiza la mejor solución si encuentra un extremismo estrictamente menor.

### 2.2. Análisis de Complejidad (Enunciado 3.1.1)

#### Preguntas guía para la argumentación:
1. ¿Cuál es el tamaño exacto del espacio de configuraciones posibles en términos de $n$?
2. En la implementación concreta, ¿cuánto cuesta convertir el entero $i$ a binario y vector de enteros?
3. ¿Cuánto tiempo toman las funciones `calcular_esfuerzo` y `calcular_extremismo` para un vector de tamaño $n$?
4. ¿Por qué la complejidad temporal total es $\Theta(n \cdot 2^n)$ y no simplemente $O(2^n)$?
5. ¿Cuál es la complejidad espacial y qué estructuras consumen memoria durante la ejecución?

#### Puntos clave obligatorios:
- **Complejidad Temporal:** $\Theta(n \cdot 2^n)$. Justificar que hay $2^n$ iteraciones y que en cada una se realiza un recorrido de longitud $n$ para verificar aplicabilidad y calcular extremismo.
- **Complejidad Espacial:** $O(n)$. Justificar que solo se mantienen en memoria los vectores de tamaño $n$ para la combinación actual y la mejor encontrada.

**Texto a redactar:**  
[COMPLETAR: Demostración formal y argumentación detallada de la complejidad temporal y espacial.]

### 2.3. Demostración de Corrección (Enunciado 3.1.2)

#### Preguntas guía para la argumentación:
1. ¿El algoritmo deja alguna estrategia aplicable por fuera del espacio evaluado?
2. ¿Por qué la estrategia inicial $E = \langle 0, \dots, 0 \rangle$ garantiza que siempre exista al menos una solución aplicable cuando $R_{\max} \ge 0$?
3. En presencia de empates en el valor de extremismo mínimo, ¿qué estrategia preserva la implementación y por qué sigue siendo una solución óptima válida?
4. ¿Garantiza siempre encontrar la solución óptima global?

#### Puntos clave obligatorios:
- Argumentar exhaustividad: el algoritmo enumera el conjunto potencia $\{0, 1\}^n$.
- Argumentar optimalidad: al evaluar todas las opciones válidas y conservar el mínimo absoluto de la función objetivo $Ext$, es imposible que exista una estrategia aplicable con menor extremismo no considerada.

**Texto a redactar:**  
[COMPLETAR: Demostración de corrección del algoritmo de fuerza bruta.]

---

## 3. Solución Voraz (Greedy)

> **Responsable:** Integrante B  
> **Qué pide el enunciado:** Sección 3.2. Subsecciones 3.2.1 (Descripción detallada del algoritmo voraz diseñado), 3.2.2 (Salida y costo para ejemplos 2.3.1 y 2.3.2, y tabla con $\ge 4$ entradas adicionales evaluando optimalidad), 3.2.3 (Complejidad temporal y espacial argumentada) y 3.2.4 (Corrección: argumentación de si siempre da el óptimo, con análisis de cuándo sí y cuándo no).  
> **Hechos verificados del código:** Función `modexV` en [modexv.py:3-30](file:///modexv.py#L3-L30). Función `costo_beneficio` en [modexv.py:33-45](file:///modexv.py#L33-L45) calcula beneficio $= o_i^2 \cdot \text{inf}_i$ y costo $= \lceil |o_i|(1-r_i)\text{inf}_i \rceil$. Ordena decrecientemente por beneficio/costo. Recorre y modera si cabe; si excede, continúa (`continue`).

### 3.1. Descripción del algoritmo voraz y criterio de selección (Enunciado 3.2.1)
El algoritmo voraz diseñado (`modexV`) adapta la heurística clásica del problema de la mochila fraccionaria al problema discreto de moderación. El objetivo de moderar al agente $i$ es eliminar su contribución al extremismo, dada por $o_i^2 \cdot \text{inf}_i$ (beneficio), invirtiendo un costo de $\lceil |o_i| \cdot (1 - r_i) \cdot \text{inf}_i \rceil$ unidades de esfuerzo.

El criterio de ordenamiento voraz se define mediante la razón beneficio/costo:

$$\text{Razón}_i = \begin{cases} \frac{o_i^2 \cdot \text{inf}_i}{\lceil |o_i| \cdot (1 - r_i) \cdot \text{inf}_i \rceil} & \text{si costo} > 0 \\ +\infty & \text{si costo} = 0 \end{cases}$$

El algoritmo ordena a los agentes de mayor a menor según esta razón en $O(n \log n)$ y realiza una exploración voraz: si el esfuerzo del agente actual cabe en el presupuesto remanente, se fija $e_i = 1$ y se acumula el esfuerzo; en caso contrario, se ignora ($e_i = 0$) y se evalúa el siguiente agente.

**Texto a redactar:**  
[COMPLETAR: Justificación intuitiva de por qué se eligió esta heurística y explicación paso a paso del algoritmo.]

### 3.2. Evaluación con los ejemplos del enunciado (Enunciado 3.2.2)

#### Ejemplo 1 del enunciado (Sección 2.3.1)
- **Entrada:** $n = 3$, $R_{\max} = 55$. Agentes: $a_0 = \langle 100, 0.5, 1 \rangle$, $a_1 = \langle 100, 0.1, 1 \rangle$, $a_2 = \langle -10, 0.1, 1 \rangle$.
- **Cálculo de razones:**
  - $a_0$: Beneficio $= 10000$, Costo $= \lceil 100 \cdot 0.5 \cdot 1 \rceil = 50$, Razón $= 10000 / 50 = 200.0$.
  - $a_1$: Beneficio $= 10000$, Costo $= \lceil 100 \cdot 0.9 \cdot 1 \rceil = 90$, Razón $= 10000 / 90 \approx 111.11$.
  - $a_2$: Beneficio $= 100$, Costo $= \lceil 10 \cdot 0.9 \cdot 1 \rceil = 9$, Razón $= 100 / 9 \approx 11.11$.
- **Selección voraz:** Orden $\langle a_0, a_1, a_2 \rangle$. Modera $a_0$ (esfuerzo 50). Presupuesto restante: 5. $a_1$ (costo 90) no cabe. $a_2$ (costo 9) no cabe.
- **Salida voraz:** $E = \langle 1, 0, 0 \rangle$, $\text{Esfuerzo} = 50$, $Ext \approx 33.50$.
- **¿Es óptima?:** Sí. Coincide con la solución óptima global demostrada en el enunciado.

#### Ejemplo 2 del enunciado (Sección 2.3.2)
- **Entrada:** $n = 3$, $R_{\max} = 35$. Agentes: $a_0 = \langle -30, 0.9, 1 \rangle$, $a_1 = \langle 20, 0.1, 2 \rangle$, $a_2 = \langle 50, 0.5, 1 \rangle$.
- **Cálculo de razones:**
  - $a_0$: Beneficio $= 900$, Costo $= \lceil 30 \cdot 0.1 \cdot 1 \rceil = 3$, Razón $= 900 / 3 = 300.0$.
  - $a_1$: Beneficio $= 800$, Costo $= \lceil 20 \cdot 0.9 \cdot 2 \rceil = 36$, Razón $= 800 / 36 \approx 22.22$.
  - $a_2$: Beneficio $= 2500$, Costo $= \lceil 50 \cdot 0.5 \cdot 1 \rceil = 25$, Razón $= 2500 / 25 = 100.0$.
- **Selección voraz:** Orden $\langle a_0, a_2, a_1 \rangle$. Modera $a_0$ (esfuerzo 3, resta 32). Modera $a_2$ (esfuerzo 25, resta 7). $a_1$ (costo 36) no cabe.
- **Salida voraz:** $E = \langle 1, 0, 1 \rangle$, $\text{Esfuerzo} = 28$, $Ext \approx 9.43$.
- **¿Es óptima?:** Sí. Coincide con la solución óptima demostrada en el enunciado.

### 3.3. Tabla de entradas adicionales y evaluación de optimalidad (Enunciado 3.2.2)

A continuación se evalúa el comportamiento del algoritmo voraz en 4 casos adicionales diseñados para contrastar aciertos y fallos:

| Caso / Archivo | Entrada ($n$, $R_{\max}$, agentes) | Salida Voraz $E$ | Esfuerzo Voraz | Extremismo Voraz | Solución Óptima ($E^*$, Esf$^*$, Ext$^*$) | ¿Es óptima? |
|---|---|---|---|---|---|---|
| `borde_n1.txt` | $n=1$, $R_{\max}=40$, $\langle 80, 0.5, 2 \rangle$ | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | Sí |
| `borde_rmax0.txt` | $n=3$, $R_{\max}=0$, $\langle 40, 0.2, 1 \rangle, \langle -70, 0.5, 2 \rangle, \langle 90, 0.3, 3 \rangle$ | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | Sí |
| `voraz_falla1.txt` | $n=3$, $R_{\max}=100$, $\langle 60, 0, 1 \rangle, \langle 50, 0, 1 \rangle, \langle 50, 0, 1 \rangle$ | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | No |
| `voraz_falla2.txt` | $n=3$, $R_{\max}=60$, $\langle 10, 0, 1 \rangle, \langle 10, 0, 1 \rangle, \langle 60, 0, 1 \rangle$ | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | No |

**Texto a redactar:**  
[COMPLETAR: Análisis detallado de cada una de las 4 filas de la tabla explicando por qué se alcanzó o no el óptimo.]

### 3.4. Análisis de Complejidad (Enunciado 3.2.3)

#### Preguntas guía para la argumentación:
1. ¿Cuál es el costo computacional de calcular la relación beneficio/costo para cada agente?
2. ¿Cuánto cuesta ordenar los $n$ agentes por su razón (usando Timsort nativo de Python)?
3. ¿Cuánto cuesta el bucle voraz de selección lineal?
4. ¿Cuánto cuesta el cálculo final de extremismo de la red resultante?
5. ¿Cuál es la complejidad temporal y espacial total del algoritmo?

#### Puntos clave obligatorios:
- **Complejidad Temporal:** $O(n \log n)$, dominada por el paso de ordenamiento.
- **Complejidad Espacial:** $O(n)$, requerida para almacenar la lista indexada y el vector de resultados $E$.

**Texto a redactar:**  
[COMPLETAR: Justificación matemática del orden de complejidad temporal y espacial.]

### 3.5. Corrección: ¿Siempre da la respuesta correcta? (Enunciado 3.2.4)

El algoritmo voraz **NO** siempre da la respuesta correcta al problema ModEx.

#### Contraejemplo formal:
Considere una red social con $n = 2$ agentes y presupuesto $R_{\max} = 99$:
- Agente $a_0$: $o_0 = 10$, $r_0 = 0.9$, $\text{inf}_0 = 1.0$.
  - $\text{Beneficio}_0 = 10^2 \cdot 1.0 = 100$.
  - $\text{Costo}_0 = \lceil 10 \cdot (1 - 0.9) \cdot 1.0 \rceil = \lceil 1.0 \rceil = 1$.
  - $\text{Razón}_0 = 100 / 1 = 100.0$.
- Agente $a_1$: $o_1 = 99$, $r_1 = 0.0$, $\text{inf}_1 = 1.0$.
  - $\text{Beneficio}_1 = 99^2 \cdot 1.0 = 9801$.
  - $\text{Costo}_1 = \lceil 99 \cdot (1 - 0.0) \cdot 1.0 \rceil = \lceil 99.0 \rceil = 99$.
  - $\text{Razón}_1 = 9801 / 99 = 99.0$.

**Ejecución voraz:**
1. Ordena $\langle a_0, a_1 \rangle$ porque $\text{Razón}_0 (100) > \text{Razón}_1 (99)$.
2. Selecciona $a_0$, acumulando esfuerzo 1. Presupuesto restante: $99 - 1 = 98$.
3. Evalúa $a_1$: su costo (99) excede el presupuesto restante (98). Se rechaza.
4. Salida voraz: $E_{\text{voraz}} = \langle 1, 0 \rangle$, $\text{Esfuerzo} = 1$, $Ext_{\text{voraz}} = \frac{\sqrt{0 + 99^2 \cdot 1}}{2} = \frac{99}{2} = 49.5$.

**Solución óptima real:**
- Moderar únicamente a $a_1$: $E^* = \langle 0, 1 \rangle$, $\text{Esfuerzo} = 99 \le R_{\max}$.
- $Ext^* = \frac{\sqrt{10^2 \cdot 1 + 0}}{2} = \frac{10}{2} = 5.0$.
- El extremismo del voraz (49.5) es casi **10 veces peor** que el óptimo (5.0).

#### Preguntas guía para el análisis:
1. ¿Cuándo sí da la respuesta correcta? (Cuando la capacidad no deja espacio residual "desperdiciado", cuando todos los costos son uniformes, o cuando el presupuesto es suficiente para todos los candidatos de alta razón).
2. ¿Cuándo no da la respuesta correcta? (Cuando elegir un elemento con alta densidad beneficio/costo bloquea a un elemento con un beneficio absoluto mucho mayor que encajaría exactamente en la capacidad).
3. ¿Por qué la naturaleza indivisible (0/1) del problema impide la propiedad de elección voraz?

**Texto a redactar:**  
[COMPLETAR: Discusión exhaustiva de las condiciones bajo las cuales el voraz acierta o fracasa, fundamentando la analogía con la mochila 0/1 entera.]

---

## 4. Solución por Programación Dinámica

> **Responsable:** Integrante C  
> **Qué pide el enunciado:** Sección 3.3. Subsecciones 3.3.1 (Subestructura óptima y número de subproblemas), 3.3.2 (Definición recursiva del valor óptimo), 3.3.3 (Algoritmo para calcular el costo/ganancia óptima), 3.3.4 (Estructura y algoritmo de reconstrucción de la solución) y 3.3.5 (Complejidad temporal/espacial y análisis práctico con $n = 2^k$, $3 \times 10^8$ ops/min y 4 bytes/celda).  
> **Hechos verificados del código:** Función `modexPD` en [modexpd.py:4-71](file:///modexpd.py#L4-L71). Maximiza ganancia $G = \sum e_i \cdot o_i^2 \cdot \text{inf}_i$ sujeto a esfuerzo $\le R$. Cota superior $R = \min(R_{\max}, \sum \text{costos})$ en línea 35. Optimización de memoria en valores: 2 filas (`anterior`, `actual`). Matriz `decision` con `bytearray(cap + 1)` en líneas 44-58. Reconstrucción hacia atrás en líneas 61-67.

### 4.1. Caracterización de la subestructura óptima y subproblemas (Enunciado 3.3.1)
El extremismo tras moderar la red se expresa como:

$$Ext(\text{Mod}(RS, E)) = \frac{\sqrt{\sum_{i=0}^{n-1} o_i^2 \cdot \text{inf}_i - \sum_{i=0}^{n-1} e_i \cdot o_i^2 \cdot \text{inf}_i}}{n} = \frac{\sqrt{S_{\text{total}} - G(E)}}{n}$$

Dado que $S_{\text{total}}$ y $n$ son constantes fijas de la entrada, y la función $\sqrt{\cdot}$ es monótona creciente, **minimizar el extremismo equivale estrictamente a maximizar la ganancia total $G(E) = \sum_{i=0}^{n-1} e_i \cdot (o_i^2 \cdot \text{inf}_i)$** sujeta a la restricción $\sum_{i=0}^{n-1} e_i \cdot c_i \le R_{\max}$, donde $c_i = \text{costo\_moderar}(a_i)$. Esto corresponde a una mochila 0/1 entera.

- **Definición del subproblema:**  
  Sea $G(i, j)$ la máxima ganancia acumulada que se puede obtener considerando únicamente los primeros $i$ agentes ($0 \le i \le n$) con un presupuesto disponible de esfuerzo $j$ ($0 \le j \le R$), donde $R = \min(R_{\max}, \sum_{k=0}^{n-1} c_k)$.
- **Número de subproblemas:**  
  Hay $(n + 1) \cdot (R + 1)$ subproblemas distintos.

#### Preguntas guía para la argumentación:
1. ¿Cómo se demuestra que un prefijo de la solución óptima global es a su vez solución óptima de un subproblema con capacidad reducida? (Principio de optimalidad de Bellman).
2. ¿Por qué se puede acotar la capacidad de la tabla a $\min(R_{\max}, \sum c_i)$ sin perder optimalidad?

**Texto a redactar:**  
[COMPLETAR: Demostración formal de la propiedad de subestructura óptima.]

### 4.2. Definición recursiva del valor de una solución óptima (Enunciado 3.3.2)

La recurrencia formal para el cálculo de $G(i, j)$ se define como:

$$G(i, j) = \begin{cases} 
0 & \text{si } i = 0 \text{ o } j = 0 \\
G(i-1, j) & \text{si } i > 0 \text{ y } c_{i-1} > j \\
\max\Big(G(i-1, j),\, g_{i-1} + G(i-1, j - c_{i-1})\Big) & \text{si } i > 0 \text{ y } c_{i-1} \le j 
\end{cases}$$

Donde para el agente $i-1$:
- $c_{i-1} = \lceil |o_{i-1}| \cdot (1 - r_{i-1}) \cdot \text{inf}_{i-1} \rceil$ es el costo de esfuerzo.
- $g_{i-1} = o_{i-1}^2 \cdot \text{inf}_{i-1}$ es la ganancia de extremismo eliminada.

**Texto a redactar:**  
[COMPLETAR: Explicación de los casos base, la condición de exclusión por presupuesto insuficiente y la regla de decisión óptima.]

### 4.3. Algoritmo para calcular el valor óptimo (Enunciado 3.3.3)

#### Preguntas guía para el redactor:
1. ¿Cuál es el orden de llenado de la tabla (iterativo ascendente / bottom-up)?
2. ¿Por qué para calcular la ganancia óptima basta con conservar únicamente dos filas (`anterior` y `actual`) en lugar de toda la matriz de números reales?

**Texto a redactar:**  
[COMPLETAR: Descripción del algoritmo bottom-up y justificación de la optimización de memoria en las filas de valores.]

### 4.4. Estructura y algoritmo para reconstruir la solución óptima (Enunciado 3.3.4)

Para reconstruir el vector binario $E = \langle e_0, \dots, e_{n-1} \rangle$, el algoritmo almacena una tabla de decisiones booleanas `decision[i][j]` de dimensiones $(n + 1) \times (R + 1)$, implementada con `bytearray` (1 byte por celda):
- `decision[i][j] = 1` si en el subproblema $(i, j)$ fue estrictamente mejor moderar al agente $i-1$.
- `decision[i][j] = 0` si fue mejor no moderarlo.

**Algoritmo de reconstrucción:**
1. Inicializar $E = [0, 0, \dots, 0]$ y capacidad restante $j = R$.
2. Para $i$ desde $n$ descendiendo hasta 1:
   - Si `decision[i][j] == 1`:
     - Asignar $E[i-1] = 1$.
     - Descontar el costo: $j = j - c_{i-1}$.
3. Retornar $E$, el esfuerzo consumido y el extremismo final.

**Texto a redactar:**  
[COMPLETAR: Explicación detallada del paso de reconstrucción hacia atrás y su complejidad temporal $O(n)$.]

### 4.5. Análisis de Complejidad (Enunciado 3.3.5)

#### Puntos clave obligatorios:
- **Complejidad Temporal:** $\Theta(n \cdot R)$, donde $R = \min(R_{\max}, \sum c_i)$.
  - Argumentar: Se llenan $(n+1)$ filas y cada una itera sobre $(R+1)$ columnas realizando operaciones en tiempo constante $O(1)$. La reconstrucción toma $O(n)$. Por tanto, el tiempo está acotado por $\Theta(n \cdot R)$.
  - Aclarar el carácter **pseudopolinomial**: es polinomial respecto al valor numérico de $R_{\max}$, pero exponencial respecto al número de bits de su representación binaria.
- **Complejidad Espacial:**
  - Valores numéricos: $O(R)$ usando dos filas.
  - Tabla de decisiones para reconstrucción: $\Theta(n \cdot R)$ celdas.

**Texto a redactar:**  
[COMPLETAR: Desarrollo formal de las complejidades temporal y espacial.]

### 4.6. Análisis práctico con $n = 2^k$ (Enunciado 3.3.5)

> **Parámetros del enunciado:**
> - Capacidad de procesamiento: $3 \times 10^8$ operaciones por minuto ($5 \times 10^6$ ops/seg).
> - Almacenamiento: $4$ bytes por celda de memoria.
> - Equivalencias sugeridas: $1 \text{ año} = 518400 \text{ minutos}$. $2^{10} \text{ B} = 1 \text{ KB}$, $2^{10} \text{ KB} = 1 \text{ MB}$, $2^{10} \text{ MB} = 1 \text{ GB} \approx 10^3 \text{ MB}$.
> - Aproximaciones: $n+1 \approx n$, $A+1 \approx A$.

> **[DECIDIR: Supuesto sobre el presupuesto $R$ en función de $n$]**  
> El enunciado pide analizar la complejidad en términos de $n = 2^k$, pero la complejidad real depende de $n \cdot R$. Para resolver esta ambigüedad, el grupo debe justificar el comportamiento de $R$:
> - **Opción A (Recomendada - Peor caso acotado):** Cada agente tiene un costo máximo de $\lceil 100 \cdot 1.0 \cdot 3.0 \rceil = 300$. Por tanto, $\sum c_i \le 300n$. En el peor caso, $R = \min(R_{\max}, 300n) \approx 300 \cdot 2^k$. Esto genera una tabla de $n \cdot R \approx 300 \cdot 2^{2k}$ celdas.
> - **Opción B (Presupuesto constante fijo):** Si $R_{\max}$ es una constante fija independiente de $n$ (ej. $R_{\max} = 500$), la complejidad sería $O(n)$, lo cual no refleja el crecimiento del problema en redes grandes.
> - *Decisión adoptada:* Se asume la **Opción A**, pues modela una red donde el presupuesto escala proporcionalmente al número de agentes.

#### Tabla de escalabilidad práctica ($R \approx 300 \cdot 2^k$):

| $k$ | $n = 2^k$ | $R \approx 300 \cdot 2^k$ | Celdas ($n \cdot R \approx 300 \cdot 2^{2k}$) | Operaciones estimadas | Tiempo estimado | Memoria ($4 \text{ bytes} \times \text{celdas}$) | Veredicto práctico |
|---|---|---|---|---|---|---|---|
| $k = 5$ | 32 | 9,600 | $\approx 3.07 \times 10^5$ | $\approx 3.07 \times 10^5$ | $\approx 0.06$ seg ($10^{-3}$ min) | $\approx 1.17$ MB | **Aceptable** |
| $k = 10$ | 1,024 | 307,200 | $\approx 3.14 \times 10^8$ | $\approx 3.14 \times 10^8$ | $\approx 1.05$ minutos | $\approx 1.17$ GB | **Aceptable** |
| $k = 15$ | 32,768 | $\approx 9.83 \times 10^6$ | $\approx 3.22 \times 10^{11}$ | $\approx 3.22 \times 10^{11}$ | $\approx 1073$ min ($\approx 17.9$ horas) | $\approx 1.20$ TB | **Inaceptable** (por memoria) |
| $k = 20$ | 1,048,576 | $\approx 3.14 \times 10^8$ | $\approx 3.29 \times 10^{14}$ | $\approx 3.29 \times 10^{14}$ | $\approx 1.1 \times 10^6$ min ($\approx 2.1$ años) | $\approx 1.23$ PB | **Inaceptable** (tiempo y memoria) |

#### Preguntas guía para la conclusión de aceptabilidad:
1. ¿A partir de qué valor exacto de $k$ la memoria requerida supera la capacidad de una estación de trabajo típica (ej. 16 GB - 32 GB RAM)?
2. ¿A partir de qué valor de $k$ el tiempo de ejecución excede una espera razonable para una aplicación interactiva (ej. > 5 minutos)?
3. Si en lugar de 4 bytes se usa la implementación con `bytearray` (1 byte por celda), ¿cambia significativamente el límite de $k$?

**Texto a redactar:**  
[COMPLETAR: Argumentación detallada de los límites prácticos de $k$ en tiempo y memoria.]

---

## 5. Comparación de los Tres Algoritmos

> **Responsable:** Integrante D (Integración y comparación)  
> **Qué pide el enunciado:** Sección 4 (Criterio 1 de calificación: sección dedicada a comparar los resultados de las tres soluciones usando tablas, diseñando casos de prueba y documentando cómo se diseñaron).  
> **Hechos verificados del código:** Casos disponibles en [casos_prueba/](file:///casos_prueba/). Ejecución por lotes automatizada mediante [pruebas.py](file:///pruebas.py). Resultados generados en `resultados_pruebas.txt` y `resultados_fb20.txt`.

### 5.1. Diseño y caracterización de los casos de prueba

| Archivo / Caso | Propósito del diseño | $n$ | $R_{\max}$ | Categoría |
|---|---|---|---|---|
| `ejemplo1.txt` | Caso base del enunciado (Sección 2.3.1). Valida correctitud contra datos oficiales. | 3 | 55 | Oficial |
| `ejemplo2.txt` | Caso base del enunciado (Sección 2.3.2). Valida empate y agentes con receptividad variable. | 3 | 35 | Oficial |
| `borde_n1.txt` | Caso borde mínimo ($n = 1$). Evalúa comportamiento con un único agente. | 1 | 40 | Borde |
| `borde_rmax0.txt` | Caso borde sin presupuesto ($R_{\max} = 0$). Verifica que no se aplique esfuerzo mayor a 0. | 3 | 0 | Borde |
| `borde_opiniones_cero.txt` | Caso borde donde todos tienen opinión 0 (neutrales, costo/beneficio nulo). | 3 | 20 | Borde |
| `borde_presupuesto_total.txt` | Caso donde $R_{\max}$ excede el costo de moderar a todos los agentes de la red. | 4 | 10000 | Borde |
| `voraz_falla1.txt` | Contraejemplo donde el Voraz selecciona un agente y bloquea una mejor combinación. | 3 | 100 | Heurística |
| `voraz_falla2.txt` | Segundo contraejemplo donde Voraz prefiere elementos de alta razón pero menor impacto global. | 3 | 60 | Heurística |
| `aleatorio_n8.txt` | Caso aleatorio pequeño para contraste rápido entre las tres soluciones. | 8 | 150 | Rendimiento |
| `aleatorio_n10.txt` | Caso aleatorio intermedio para observar crecimiento del árbol en FB. | 10 | 250 | Rendimiento |
| `aleatorio_n15.txt` | Límite práctico estándar de FB ($2^{15} = 32,768$ combinaciones). | 15 | 400 | Rendimiento |
| `aleatorio_n20.txt` | Caso en el límite superior de FB ($2^{20} = 1,048,576$ combinaciones). | 20 | 600 | Escala |
| `grande_n1000.txt` | Caso masivo ($n = 1000$) para evaluar escalabilidad de PD y Voraz (FB omitido). | 1000 | 20000 | Escala |

**Texto a redactar:**  
[COMPLETAR: Justificación metodológica de la selección de casos, cubriendo correctitud, casos frontera, trampas heurísticas y estrés de rendimiento.]

### 5.2. Tabla comparativa de resultados empíricos

> Los datos de esta tabla provienen de las ejecuciones reales realizadas con `pruebas.py` en el repositorio.

| Caso | $n$ | $R_{\max}$ | $Ext_{\text{FB}}$ | $\text{Esf}_{\text{FB}}$ | $t_{\text{FB}}$ (s) | $Ext_{\text{V}}$ | $\text{Esf}_{\text{V}}$ | $t_{\text{V}}$ (s) | $Ext_{\text{PD}}$ | $\text{Esf}_{\text{PD}}$ | $t_{\text{PD}}$ (s) | ¿Voraz Óptimo? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ejemplo1.txt` | 3 | 55 | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | Sí |
| `ejemplo2.txt` | 3 | 35 | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | Sí |
| `borde_n1.txt` | 1 | 40 | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | Sí |
| `borde_rmax0.txt` | 3 | 0 | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | Sí |
| `borde_opiniones_cero.txt` | 3 | 20 | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | Sí |
| `borde_presupuesto_total.txt` | 4 | 10000 | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | Sí |
| `voraz_falla1.txt` | 3 | 100 | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | No |
| `voraz_falla2.txt` | 3 | 60 | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | No |
| `aleatorio_n8.txt` | 8 | 150 | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` |
| `aleatorio_n10.txt` | 10 | 250 | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` |
| `aleatorio_n15.txt` | 15 | 400 | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` |
| `aleatorio_n20.txt` | 20 | 600 | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` |
| `grande_n1000.txt` | 1000 | 20000 | - | - | Omitido | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` | `[MEDIR]` |

### 5.3. Análisis e interpretación de los resultados

#### Preguntas guía para el análisis:
1. **Calidad de la solución:** ¿En qué porcentaje de los casos aleatorios la solución voraz logró el óptimo global? Cuando no lo logró, ¿cuál fue la desviación porcentual promedio respecto al óptimo de PD?
2. **Escalabilidad temporal:** ¿Cómo se comporta el tiempo de FB a medida que $n$ pasa de 10 a 15 y luego a 20? ¿A qué tasa crece en comparación con PD?
3. **Comportamiento en casos extremos:** ¿Cómo respondieron los algoritmos ante presupuesto nulo ($R_{\max} = 0$) y presupuesto excedente?
4. **Relación calidad/tiempo:** ¿Es justificable usar la heurística voraz cuando $n > 1000$?

**Texto a redactar:**  
[COMPLETAR: Discusión fundamentada en los valores empíricos registrados en la tabla anterior.]

---

## 6. Conclusiones

> **Responsable:** Integrante D (con aportes de A, B y C)  
> **Qué pide el enunciado:** Sección 4 (Criterio 1: sección dedicada a concluir sobre las ventajas y desventajas de usar en la práctica los diferentes enfoques).

### 6.1. Ventajas y desventajas de cada enfoque

#### Fuerza Bruta
- **Ventajas:** Simplicidad conceptual; garantiza el óptimo global sin suposiciones de estructura matemática; sirve como oráculo de verificación para validar algoritmos más sofisticados.
- **Desventajas:** Crecimiento exponencial $\Theta(n \cdot 2^n)$; inviable en la práctica para $n > 20$.

#### Algoritmo Voraz
- **Ventajas:** Alta velocidad de cómputo ($O(n \log n)$); bajo consumo de memoria ($O(n)$); fácil de implementar; adecuado para respuestas en tiempo real en sistemas de gran escala.
- **Desventajas:** No garantiza la solución óptima; puede quedar atrapado en malas decisiones al ignorar la indivisibilidad del presupuesto (capacidad residual).

#### Programación Dinámica
- **Ventajas:** Garantiza la solución óptima de manera eficiente en problemas con presupuestos moderados; tiempo y espacio pseudopolinomial $\Theta(n \cdot R)$; aprovechamiento de subestructura óptima.
- **Desventajas:** Depende fuertemente del valor de $R_{\max}$; si el presupuesto es gigantesco, la memoria puede desbordar la capacidad física del equipo.

### 6.2. Conclusión general y recomendaciones prácticas

#### Preguntas guía para la síntesis:
1. En un escenario real de una red social con millones de usuarios y decisiones en tiempo real, ¿cuál enfoque se recomendaría y por qué?
2. ¿Cómo podría combinarse la programación dinámica con técnicas voraces o de aproximación (FPTAS) para mitigar el costo de memoria en presupuestos altos?

**Texto a redactar:**  
[COMPLETAR: Párrafo de conclusiones generales y cierre del informe técnico.]

---

## 7. Anexos

> **Responsable:** Integrante D  
> **Qué pide el enunciado:** Instrucciones de ejecución, estructura de archivos y detalles técnicos para la evaluación.

### 7.1. Instrucciones de ejecución
Para ejecutar la aplicación interactiva:
```bash
python main.py
```
*(En entornos Windows donde `python` invoque el alias de la Microsoft Store, usar: `py main.py`)*

Para ejecutar la suite completa de pruebas automatizadas:
```bash
py pruebas.py
```
Opciones adicionales:
- `py pruebas.py --fb-max 20`: Ejecuta Fuerza Bruta hasta $n = 20$.
- `py pruebas.py --aleatorios 50`: Evalúa 50 casos aleatorios adicionales.

### 7.2. Estructura de archivos entregados
- `main.py`: Punto de entrada que lanza la interfaz gráfica.
- `gui.py`: Interfaz de usuario (Tkinter/ttk) y módulo de entrada/salida.
- `modexfb.py`: Algoritmo de Fuerza Bruta (`modexFB`).
- `modexv.py`: Algoritmo Voraz (`modexV`).
- `modexpd.py`: Algoritmo de Programación Dinámica (`modexPD`).
- `utils.py`: Fórmulas matemáticas de extremismo y costos.
- `generador.py`: Generador de casos de prueba aleatorios.
- `pruebas.py`: Verificación automatizada e independiente de optimalidad.
- `README.md`: Documentación del repositorio en Markdown.
- `Readme.txt`: Manual de entrega e instrucciones en texto plano.
- `casos_prueba/`: Directorio con 13 casos de prueba en formato `.txt`.
- `INFORME.md`: Esqueleto y contenido técnico del informe del proyecto.

---

## Pendientes por Sección

Lista de chequeo para finalizar el informe antes de exportar a PDF:

- [ ] **Portada:** Completar códigos de estudiante de Sebastian Marulanda y Mateo Noguera.
- [ ] **Sección 1 (Intro):** Redactar el párrafo de contextualización social del modelo ModEx.
- [ ] **Sección 2 (FB):** Desarrollar la argumentación formal de complejidad $\Theta(n \cdot 2^n)$ y la demostración de corrección por exhaustividad.
- [ ] **Sección 3 (Voraz):** 
  - [ ] Redactar la justificación de la heurística y los pasos del algoritmo.
  - [ ] Llenar con valores `[MEDIR]` la tabla de las 4 entradas adicionales (`borde_n1`, `borde_rmax0`, `voraz_falla1`, `voraz_falla2`).
  - [ ] Desarrollar el análisis de complejidad $O(n \log n)$ y la discusión de cuándo acierta y cuándo falla.
- [ ] **Sección 4 (PD):**
  - [ ] Demostrar formalmente la propiedad de subestructura óptima.
  - [ ] Explicar la recurrencia y la reconstrucción con `bytearray`.
  - [ ] Redactar la conclusión sobre la aceptabilidad de $k$ en la tabla de $n = 2^k$.
- [ ] **Sección 5 (Comparación):**
  - [ ] Copiar los tiempos y resultados de `resultados_pruebas.txt` y `resultados_fb20.txt` en la tabla de la Sección 5.2.
  - [ ] Redactar el análisis comparativo de calidad, tiempos y escalabilidad.
- [ ] **Sección 6 (Conclusiones):** Redactar las reflexiones finales del equipo y recomendaciones de ingeniería.
- [ ] **Exportación:** Convertir `INFORME.md` a PDF manteniendo formato limpio para la entrega final.
