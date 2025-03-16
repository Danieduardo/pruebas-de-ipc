# InterfazGrafiza.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from SistemaAtencionClientes import SistemaAtencionClientes

class InterfazGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Atención al Cliente")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # Instancia del sistema de atención al cliente
        self.sistema = SistemaAtencionClientes()

        # Crear pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Pestaña de Configuración
        self.tab_configuracion = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_configuracion, text="Configuración")

        self.btn_cargar_config = tk.Button(self.tab_configuracion, text="Cargar Configuración", command=self.cargar_configuracion, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.btn_cargar_config.pack(pady=10)

        self.btn_cargar_estado = tk.Button(self.tab_configuracion, text="Cargar Estado Inicial", command=self.cargar_estado_inicial, bg="#2196F3", fg="white", font=("Arial", 12))
        self.btn_cargar_estado.pack(pady=10)

        # Pestaña de Simulación
        self.tab_simulacion = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_simulacion, text="Simulación")

        self.lbl_tiempo_simulacion = tk.Label(self.tab_simulacion, text="Tiempo de Simulación (minutos):", font=("Arial", 12))
        self.lbl_tiempo_simulacion.pack(pady=10)

        self.entry_tiempo_simulacion = tk.Entry(self.tab_simulacion, font=("Arial", 12))
        self.entry_tiempo_simulacion.pack(pady=10)

        self.btn_simular = tk.Button(self.tab_simulacion, text="Simular Atención", command=self.simular_atencion, bg="#FF9800", fg="white", font=("Arial", 12))
        self.btn_simular.pack(pady=10)

        # Pestaña de Estadísticas
        self.tab_estadisticas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_estadisticas, text="Estadísticas")

        self.text_estadisticas = tk.Text(self.tab_estadisticas, wrap=tk.WORD, font=("Arial", 12))
        self.text_estadisticas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.btn_actualizar_estadisticas = tk.Button(self.tab_estadisticas, text="Actualizar Estadísticas", command=self.mostrar_estadisticas, bg="#9C27B0", fg="white", font=("Arial", 12))
        self.btn_actualizar_estadisticas.pack(pady=10)

    def cargar_configuracion(self):
        """Carga el archivo de configuración del sistema."""
        ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos XML", "*.xml")])
        if ruta_archivo:
            if self.sistema.cargar_configuracion(ruta_archivo):
                messagebox.showinfo("Éxito", "Configuración cargada correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo cargar la configuración.")

    def cargar_estado_inicial(self):
        """Carga el archivo de estado inicial del sistema."""
        ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos XML", "*.xml")])
        if ruta_archivo:
            if self.sistema.cargar_configuracion_inicial(ruta_archivo):
                messagebox.showinfo("Éxito", "Estado inicial cargado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo cargar el estado inicial.")

    def simular_atencion(self):
        """Simula la atención de clientes durante un tiempo específico."""
        try:
            tiempo_simulacion = int(self.entry_tiempo_simulacion.get())
            if tiempo_simulacion <= 0:
                messagebox.showerror("Error", "El tiempo de simulación debe ser mayor que 0.")
                return

            self.sistema.simular_actividad(tiempo_simulacion)
            messagebox.showinfo("Éxito", f"Simulación completada durante {tiempo_simulacion} minutos.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor válido para el tiempo de simulación.")

    def mostrar_estadisticas(self):
        """Muestra las estadísticas de los puntos de atención."""
        self.text_estadisticas.delete(1.0, tk.END)  # Limpiar el texto anterior

        if not self.sistema.empresas.primero:
            self.text_estadisticas.insert(tk.END, "No hay empresas cargadas.")
            return

        actual_empresa = self.sistema.empresas.primero
        while actual_empresa:
            self.text_estadisticas.insert(tk.END, f"Empresa: {actual_empresa.dato.nombre}\n", "titulo")

            actual_punto = actual_empresa.dato.puntos_atencion.primero
            while actual_punto:
                self.text_estadisticas.insert(tk.END, f"  Punto de Atención: {actual_punto.dato.nombre}\n", "subtitulo")
                estadisticas = actual_punto.dato.obtener_estadisticas()
                for key, value in estadisticas.items():
                    self.text_estadisticas.insert(tk.END, f"    {key}: {value}\n")
                actual_punto = actual_punto.siguiente

            actual_empresa = actual_empresa.siguiente

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazGrafica(root)
    root.mainloop()