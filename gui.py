import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Importación limpia de los módulos independientes
from modexfb import modexFB
from modexv import modexV
from modexpd import modexPD

class ModExApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ModEx - Moderación de Extremismo (Proyecto ADA II)")
        self.root.geometry("850x550")
        
        # Estado de la aplicación
        self.n = 0
        self.agentes = []
        self.r_max = 0
        self.resultado_actual = None
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # PANEL IZQUIERDO (Controles)
        panel_izq = ttk.Frame(self.root, padding="10")
        panel_izq.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Label(panel_izq, text="1. Entrada de Datos", font=("TkDefaultFont", 10, "bold")).pack(anchor=tk.W, pady=(0,5))
        ttk.Button(panel_izq, text="Cargar Archivo .txt", command=self.cargar_archivo).pack(fill=tk.X, pady=5)
        self.lbl_archivo = ttk.Label(panel_izq, text="Ningún archivo cargado")
        self.lbl_archivo.pack(anchor=tk.W, pady=(0, 20))
        
        ttk.Label(panel_izq, text="2. Seleccionar Algoritmo", font=("TkDefaultFont", 10, "bold")).pack(anchor=tk.W, pady=(0,5))
        self.var_algo = tk.StringVar(value="FB")
        ttk.Radiobutton(panel_izq, text="Fuerza Bruta (FB)", variable=self.var_algo, value="FB").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(panel_izq, text="Algoritmo Voraz (V)", variable=self.var_algo, value="V").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(panel_izq, text="Prog. Dinámica (PD)", variable=self.var_algo, value="PD").pack(anchor=tk.W, pady=2)
        
        ttk.Button(panel_izq, text="Ejecutar", command=self.ejecutar).pack(fill=tk.X, pady=15)
        
        ttk.Label(panel_izq, text="3. Exportar Resultados", font=("TkDefaultFont", 10, "bold")).pack(anchor=tk.W, pady=(15,5))
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
        
        self.lbl_esfuerzo = ttk.Label(frame_resumen, text="Esfuerzo Aplicado: -")
        self.lbl_esfuerzo.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.lbl_ext = ttk.Label(frame_resumen, text="Extremismo Final: -")
        self.lbl_ext.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        
        frame_tabla = ttk.LabelFrame(panel_der, text="Datos de la Red Social", padding="10")
        frame_tabla.pack(fill=tk.BOTH, expand=True)
        
        columnas = ("id", "opinion", "receptividad", "influencia", "estado")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        self.tabla.heading("id", text="ID")
        self.tabla.heading("opinion", text="Opinión")
        self.tabla.heading("receptividad", text="Receptividad")
        self.tabla.heading("influencia", text="Influencia")
        self.tabla.heading("estado", text="Estado")
        
        self.tabla.column("id", width=40, anchor=tk.CENTER)
        self.tabla.column("opinion", width=80, anchor=tk.CENTER)
        self.tabla.column("receptividad", width=80, anchor=tk.CENTER)
        self.tabla.column("influencia", width=80, anchor=tk.CENTER)
        self.tabla.column("estado", width=100, anchor=tk.CENTER)
        
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not ruta: return
        
        try:
            with open(ruta, 'r') as f:
                lineas = [l.strip() for l in f.readlines() if l.strip()]
                
            self.n = int(lineas[0])
            self.agentes = []
            
            for i in self.tabla.get_children():
                self.tabla.delete(i)
                
            for i in range(1, self.n + 1):
                datos = lineas[i].split(',')
                op = int(datos[0].strip())
                rec = float(datos[1].strip())
                inf = float(datos[2].strip())
                self.agentes.append((op, rec, inf))
                self.tabla.insert("", "end", values=(i-1, op, rec, inf, "No moderado"))
                
            self.r_max = int(lineas[self.n + 1])
            
            self.lbl_archivo.config(text=ruta.split('/')[-1])
            self.lbl_n.config(text=f"Agentes (n): {self.n}")
            self.lbl_rmax.config(text=f"Presupuesto (R_max): {self.r_max}")
            self.resultado_actual = None
            self.lbl_esfuerzo.config(text="Esfuerzo Aplicado: -")
            self.lbl_ext.config(text="Extremismo Final: -")
            
            messagebox.showinfo("Éxito", "Datos cargados correctamente.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo de entrada:\n{e}")

    def ejecutar(self):
        if self.n == 0:
            messagebox.showwarning("Advertencia", "Por favor, carga un archivo .txt primero.")
            return
            
        algo = self.var_algo.get()
        if algo == "FB":
            self.resultado_actual = modexFB(self.n, self.agentes, self.r_max)
        elif algo == "V":
            self.resultado_actual = modexV(self.n, self.agentes, self.r_max)
        elif algo == "PD":
            self.resultado_actual = modexPD(self.n, self.agentes, self.r_max)
            
        if self.resultado_actual:
            E, esfuerzo, ext = self.resultado_actual
            self.lbl_esfuerzo.config(text=f"Esfuerzo Aplicado: {esfuerzo}")
            self.lbl_ext.config(text=f"Extremismo Final: {ext:.2f}")
            
            for i, item in enumerate(self.tabla.get_children()):
                valores = list(self.tabla.item(item, "values"))
                valores[4] = "Moderado (1)" if E[i] == 1 else "No moderado (0)"
                self.tabla.item(item, values=valores)

    def guardar_salida(self):
        if not self.resultado_actual:
            messagebox.showwarning("Advertencia", "Ejecuta un algoritmo primero.")
            return
            
        ruta = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not ruta: return
        
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