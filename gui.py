import math
import os
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Importación limpia de los módulos independientes
from modexfb import modexFB
from modexv import modexV
from modexpd import modexPD
from utils import calcular_extremismo, costo_moderar
from generador import generar_caso, guardar_caso

# Límites para no congelar la aplicación con entradas grandes
LIMITE_N_FB = 20                 # con n grande explora 2^n combinaciones y puede tardar mucho
LIMITE_CELDAS_PD = 200_000_000   # n * R efectivo = celdas de la tabla de PD


class ModExApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ModEx - Moderación de Extremismo (Proyecto ADA II)")
        self.root.geometry("1100x620")

        # Estado de la aplicación
        self.n = 0
        self.agentes = []
        self.costos = []
        self.r_max = 0
        self.extremismo_inicial = None
        self.resultado_actual = None
        self.algo_actual = None

        self.crear_interfaz()

    # ------------------------------------------------------------------
    # Construcción de la interfaz
    # ------------------------------------------------------------------
    def crear_interfaz(self):
        # PANEL IZQUIERDO (Controles)
        panel_izq = ttk.Frame(self.root, padding="10")
        panel_izq.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(panel_izq, text="1. Entrada de Datos", font=("TkDefaultFont", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        ttk.Button(panel_izq, text="Cargar Archivo .txt", command=self.cargar_archivo).pack(fill=tk.X, pady=5)
        ttk.Button(panel_izq, text="Generar Caso de Prueba", command=self.abrir_generador).pack(fill=tk.X, pady=5)
        self.lbl_archivo = ttk.Label(panel_izq, text="Ningún archivo cargado")
        self.lbl_archivo.pack(anchor=tk.W, pady=(0, 20))

        ttk.Label(panel_izq, text="2. Seleccionar Algoritmo", font=("TkDefaultFont", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.var_algo = tk.StringVar(value="FB")
        ttk.Radiobutton(panel_izq, text="Fuerza Bruta (FB)", variable=self.var_algo, value="FB").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(panel_izq, text="Algoritmo Voraz (V)", variable=self.var_algo, value="V").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(panel_izq, text="Prog. Dinámica (PD)", variable=self.var_algo, value="PD").pack(anchor=tk.W, pady=2)

        ttk.Button(panel_izq, text="Ejecutar", command=self.ejecutar).pack(fill=tk.X, pady=(15, 5))
        ttk.Button(panel_izq, text="Comparar los 3", command=self.comparar).pack(fill=tk.X, pady=5)

        ttk.Label(panel_izq, text="3. Exportar Resultados", font=("TkDefaultFont", 10, "bold")).pack(anchor=tk.W, pady=(15, 5))
        ttk.Button(panel_izq, text="Guardar Salida .txt", command=self.guardar_salida).pack(fill=tk.X, pady=5)

        ttk.Separator(panel_izq, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)

        # PANEL DERECHO (Visualización)
        panel_der = ttk.Frame(self.root, padding="10")
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        frame_resumen = ttk.LabelFrame(panel_der, text="Métricas Generales", padding="10")
        frame_resumen.pack(fill=tk.X, pady=(0, 10))

        self.lbl_n = ttk.Label(frame_resumen, text="Agentes (n): -")
        self.lbl_n.grid(row=0, column=0, padx=10, sticky=tk.W)
        self.lbl_rmax = ttk.Label(frame_resumen, text="Presupuesto (R_max): -")
        self.lbl_rmax.grid(row=0, column=1, padx=10, sticky=tk.W)
        self.lbl_ext_inicial = ttk.Label(frame_resumen, text="Extremismo Inicial: -")
        self.lbl_ext_inicial.grid(row=0, column=2, padx=10, sticky=tk.W)

        self.lbl_algo = ttk.Label(frame_resumen, text="Algoritmo: -")
        self.lbl_algo.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.lbl_esfuerzo = ttk.Label(frame_resumen, text="Esfuerzo Aplicado: -")
        self.lbl_esfuerzo.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        self.lbl_ext = ttk.Label(frame_resumen, text="Extremismo Final: -")
        self.lbl_ext.grid(row=1, column=2, padx=10, pady=10, sticky=tk.W)

        # Verificación independiente de la salida (punto 3.4 del enunciado)
        frame_verif = ttk.LabelFrame(panel_der, text="Verificación de la Solución", padding="10")
        frame_verif.pack(fill=tk.X, pady=(0, 10))
        self.lbl_verif_esf = ttk.Label(frame_verif, text="Esfuerzo recalculado: -")
        self.lbl_verif_esf.pack(anchor=tk.W)
        self.lbl_verif_aplic = ttk.Label(frame_verif, text="Aplicable (Esfuerzo ≤ R_max): -")
        self.lbl_verif_aplic.pack(anchor=tk.W)
        self.lbl_verif_ext = ttk.Label(frame_verif, text="Extremismo recalculado: -")
        self.lbl_verif_ext.pack(anchor=tk.W)

        frame_tabla = ttk.LabelFrame(panel_der, text="Datos de la Red Social", padding="10")
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        columnas = ("id", "opinion", "receptividad", "influencia",
                    "costo", "aporte", "estado", "op_final")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        encabezados = {
            "id": ("ID", 50),
            "opinion": ("Opinión", 70),
            "receptividad": ("Receptividad", 90),
            "influencia": ("Influencia", 80),
            "costo": ("Costo ⌈|o|(1-r)inf⌉", 130),
            "aporte": ("Aporte o²·inf", 100),
            "estado": ("Estado", 110),
            "op_final": ("Opinión final", 90),
        }
        for col, (texto, ancho) in encabezados.items():
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, anchor=tk.CENTER)

        # Filas moderadas resaltadas en verde
        self.tabla.tag_configure("moderado", background="#d9f2e3")

        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabla.configure(yscrollcommand=scrollbar.set)

    # ------------------------------------------------------------------
    # Carga de datos
    # ------------------------------------------------------------------
    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not ruta:
            return

        try:
            n, agentes, r_max = leer_entrada(ruta)
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo de entrada:\n{e}")
            return

        self.cargar_red(n, agentes, r_max, os.path.basename(ruta))
        messagebox.showinfo("Éxito", "Datos cargados correctamente.")

    def cargar_red(self, n, agentes, r_max, nombre):
        """Carga una red en memoria y la muestra en la tabla."""
        self.n = n
        self.agentes = agentes
        self.r_max = r_max
        self.costos = [costo_moderar(a) for a in agentes]
        self.extremismo_inicial = calcular_extremismo(agentes, [0] * n)
        self.resultado_actual = None
        self.algo_actual = None

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for i, (op, rec, inf) in enumerate(agentes):
            aporte = op * op * inf
            self.tabla.insert("", "end", values=(
                i, op, rec, inf, self.costos[i], f"{aporte:.2f}", "No moderado (0)", op))

        self.lbl_archivo.config(text=nombre)
        self.lbl_n.config(text=f"Agentes (n): {n}")
        self.lbl_rmax.config(text=f"Presupuesto (R_max): {r_max}")
        self.lbl_ext_inicial.config(text=f"Extremismo Inicial: {self.extremismo_inicial:.4f}")
        self.lbl_algo.config(text="Algoritmo: -")
        self.lbl_esfuerzo.config(text="Esfuerzo Aplicado: -")
        self.lbl_ext.config(text="Extremismo Final: -")
        self.limpiar_verificacion()

    # ------------------------------------------------------------------
    # Ejecución de un algoritmo
    # ------------------------------------------------------------------
    def ejecutar(self):
        if self.n == 0:
            messagebox.showwarning("Advertencia", "Por favor, carga un archivo .txt primero.")
            return

        algo = self.var_algo.get()
        motivo = self.motivo_no_ejecutable(algo)
        if motivo and not messagebox.askyesno(
                "Entrada grande", f"{motivo}\n\nPuede tardar mucho o quedarse sin memoria. ¿Ejecutar de todas formas?"):
            return

        self.root.config(cursor="watch")
        self.root.update()
        try:
            resultado, segundos = ejecutar_algoritmo(algo, self.n, self.agentes, self.r_max)
        finally:
            self.root.config(cursor="")

        self.resultado_actual = resultado
        self.algo_actual = algo
        self.mostrar_resultado(resultado, algo, segundos)

    def mostrar_resultado(self, resultado, algo, segundos):
        E, esfuerzo, ext = resultado
        nombres = {"FB": "Fuerza Bruta", "V": "Voraz", "PD": "Prog. Dinámica"}
        self.lbl_algo.config(text=f"Algoritmo: {nombres[algo]} ({segundos:.3f} s)")
        self.lbl_esfuerzo.config(text=f"Esfuerzo Aplicado: {esfuerzo}")
        self.lbl_ext.config(text=f"Extremismo Final: {ext:.4f}")

        for i, item in enumerate(self.tabla.get_children()):
            valores = list(self.tabla.item(item, "values"))
            op = self.agentes[i][0]
            if E[i] == 1:
                valores[6] = "Moderado (1)"
                valores[7] = 0
                self.tabla.item(item, values=valores, tags=("moderado",))
            else:
                valores[6] = "No moderado (0)"
                valores[7] = op
                self.tabla.item(item, values=valores, tags=())

        self.verificar(E, esfuerzo, ext)

    # ------------------------------------------------------------------
    # Verificación independiente
    # ------------------------------------------------------------------
    def verificar(self, E, esfuerzo, ext):
        """
        Recalcula esfuerzo y extremismo a partir de la tabla (costo y aporte
        de cada agente) para comprobar que la salida del algoritmo es correcta.
        """
        esf_rec = sum(self.costos[i] for i in range(self.n) if E[i] == 1)
        suma_aportes = sum(self.agentes[i][0] ** 2 * self.agentes[i][2]
                           for i in range(self.n) if E[i] == 0)
        ext_rec = math.sqrt(suma_aportes) / self.n
        n_mod = sum(E)

        ok_esf = esf_rec == esfuerzo
        ok_aplic = esf_rec <= self.r_max
        ok_ext = abs(ext_rec - ext) < 1e-9

        self.lbl_verif_esf.config(
            text=f"Esfuerzo recalculado: Σ costos de los {n_mod} moderados = {esf_rec}  "
                 f"{'✓ coincide' if ok_esf else '✗ NO coincide con ' + str(esfuerzo)}",
            foreground="green" if ok_esf else "red")
        self.lbl_verif_aplic.config(
            text=f"Aplicable: {esf_rec} ≤ {self.r_max}  {'✓' if ok_aplic else '✗ NO es aplicable'}",
            foreground="green" if ok_aplic else "red")
        self.lbl_verif_ext.config(
            text=f"Extremismo recalculado: √(Σ aportes no moderados) / n = "
                 f"√{suma_aportes:.2f} / {self.n} = {ext_rec:.4f}  "
                 f"{'✓ coincide' if ok_ext else '✗ NO coincide'}",
            foreground="green" if ok_ext else "red")

    def limpiar_verificacion(self):
        self.lbl_verif_esf.config(text="Esfuerzo recalculado: -", foreground="")
        self.lbl_verif_aplic.config(text="Aplicable (Esfuerzo ≤ R_max): -", foreground="")
        self.lbl_verif_ext.config(text="Extremismo recalculado: -", foreground="")

    # ------------------------------------------------------------------
    # Comparación de los tres algoritmos
    # ------------------------------------------------------------------
    def motivo_no_ejecutable(self, algo):
        """Devuelve un texto si la entrada es demasiado grande para el algoritmo."""
        if algo == "FB" and self.n > LIMITE_N_FB:
            return f"Fuerza bruta con n = {self.n} explora 2^{self.n} combinaciones."
        if algo == "PD":
            celdas = self.n * min(self.r_max, sum(self.costos))
            if celdas > LIMITE_CELDAS_PD:
                return f"Prog. dinámica necesita una tabla de ~{celdas:,} celdas."
        return None

    def comparar(self):
        if self.n == 0:
            messagebox.showwarning("Advertencia", "Por favor, carga un archivo .txt primero.")
            return

        self.root.config(cursor="watch")
        self.root.update()
        filas = []
        try:
            for algo, nombre in (("FB", "Fuerza Bruta"), ("V", "Voraz"), ("PD", "Prog. Dinámica")):
                motivo = self.motivo_no_ejecutable(algo)
                if motivo:
                    filas.append((nombre, None, None, None, motivo))
                    continue
                (E, esf, ext), seg = ejecutar_algoritmo(algo, self.n, self.agentes, self.r_max)
                filas.append((nombre, ext, esf, seg, None))
        finally:
            self.root.config(cursor="")

        # El óptimo es el que den FB o PD (ambos son exactos)
        exactos = [f[1] for f in filas if f[0] != "Voraz" and f[1] is not None]
        optimo = exactos[0] if exactos else None

        ventana = tk.Toplevel(self.root)
        ventana.title("Comparación de algoritmos")
        ventana.geometry("820x220")

        cols = ("algoritmo", "ext", "esf", "tiempo", "optimo")
        tabla = ttk.Treeview(ventana, columns=cols, show="headings", height=4)
        for col, texto, ancho in (("algoritmo", "Algoritmo", 130), ("ext", "Extremismo", 110),
                                  ("esf", "Esfuerzo", 90), ("tiempo", "Tiempo (s)", 90),
                                  ("optimo", "¿Óptimo?", 380)):
            tabla.heading(col, text=texto)
            tabla.column(col, width=ancho, anchor=tk.CENTER)
        tabla.tag_configure("si", background="#d9f2e3")
        tabla.tag_configure("no", background="#f8d7da")

        for nombre, ext, esf, seg, motivo in filas:
            if ext is None:
                tabla.insert("", "end", values=(nombre, "-", "-", "-", f"No ejecutado: {motivo}"))
                continue
            if optimo is None:
                estado, tag = "Sin referencia (FB y PD no ejecutados)", ()
            elif abs(ext - optimo) < 1e-9:
                estado, tag = "Sí", ("si",)
            else:
                dif = (ext - optimo) / optimo * 100 if optimo else float("inf")
                estado, tag = f"No (+{dif:.2f}% sobre el óptimo {optimo:.4f})", ("no",)
            tabla.insert("", "end", values=(nombre, f"{ext:.4f}", esf, f"{seg:.3f}", estado), tags=tag)

        tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        ttk.Label(ventana, text=f"Extremismo inicial: {self.extremismo_inicial:.4f}   |   "
                                f"R_max: {self.r_max}   |   n: {self.n}").pack(pady=(0, 10))

    # ------------------------------------------------------------------
    # Generador de casos de prueba
    # ------------------------------------------------------------------
    def abrir_generador(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generar caso de prueba")
        ventana.resizable(False, False)

        frame = ttk.Frame(ventana, padding="15")
        frame.pack()

        ttk.Label(frame, text="Número de agentes (n):").grid(row=0, column=0, sticky=tk.W, pady=5)
        var_n = tk.StringVar(value="10")
        ttk.Entry(frame, textvariable=var_n, width=12).grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="R_max (vacío = 40% del costo total):").grid(row=1, column=0, sticky=tk.W, pady=5)
        var_r = tk.StringVar(value="")
        ttk.Entry(frame, textvariable=var_r, width=12).grid(row=1, column=1, pady=5)

        def generar():
            try:
                n = int(var_n.get())
                r_max = int(var_r.get()) if var_r.get().strip() else None
                if n <= 0 or (r_max is not None and r_max < 0):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "n debe ser un entero positivo y R_max un entero ≥ 0.", parent=ventana)
                return

            ruta = filedialog.asksaveasfilename(parent=ventana, defaultextension=".txt",
                                                initialfile=f"caso_n{n}.txt",
                                                filetypes=[("Text files", "*.txt")])
            if not ruta:
                return

            n, agentes, r_max = generar_caso(n, r_max)
            guardar_caso(ruta, n, agentes, r_max)
            ventana.destroy()
            self.cargar_red(n, agentes, r_max, os.path.basename(ruta))
            messagebox.showinfo("Éxito", f"Caso generado y cargado:\n{ruta}\n(n = {n}, R_max = {r_max})")

        ttk.Button(frame, text="Generar, guardar y cargar", command=generar).grid(
            row=2, column=0, columnspan=2, sticky=tk.EW, pady=(10, 0))

    # ------------------------------------------------------------------
    # Exportar
    # ------------------------------------------------------------------
    def guardar_salida(self):
        if not self.resultado_actual:
            messagebox.showwarning("Advertencia", "Ejecuta un algoritmo primero.")
            return

        ruta = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not ruta:
            return

        try:
            E, esfuerzo, ext = self.resultado_actual
            with open(ruta, 'w') as f:
                f.write(f"{ext}\n")
                f.write(f"{esfuerzo}\n")
                for e in E:
                    f.write(f"{e}\n")
            messagebox.showinfo("Éxito", "Archivo de salida guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la salida:\n{e}")


# ----------------------------------------------------------------------
# Funciones auxiliares (sin interfaz, se pueden probar por separado)
# ----------------------------------------------------------------------
def leer_entrada(ruta):
    """Lee un archivo con el formato del enunciado. Retorna (n, agentes, r_max)."""
    with open(ruta, 'r') as f:
        lineas = [l.strip() for l in f.readlines() if l.strip()]

    n = int(lineas[0])
    agentes = []
    for i in range(1, n + 1):
        datos = lineas[i].split(',')
        op = int(datos[0].strip())
        rec = float(datos[1].strip())
        inf = float(datos[2].strip())
        agentes.append((op, rec, inf))
    r_max = int(lineas[n + 1])
    return n, agentes, r_max


def ejecutar_algoritmo(algo, n, agentes, r_max):
    """Ejecuta FB, V o PD y retorna (resultado, segundos)."""
    funciones = {"FB": modexFB, "V": modexV, "PD": modexPD}
    inicio = time.perf_counter()
    resultado = funciones[algo](n, agentes, r_max)
    return resultado, time.perf_counter() - inicio