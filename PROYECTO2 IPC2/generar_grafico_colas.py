# graphviz_utils.py
from graphviz import Digraph

def generar_grafico_colas(punto_atencion, nombre_archivo="cola_clientes"):
    """
    Genera un gráfico de la cola de clientes en un punto de atención.
    """
    dot = Digraph(comment='Cola de Clientes')
    actual = punto_atencion.clientes_espera.primero
    while actual:
        dot.node(str(actual.dato.dpi), f"Cliente: {actual.dato.nombre}")
        if actual.siguiente:
            dot.edge(str(actual.dato.dpi), str(actual.siguiente.dato.dpi))
        actual = actual.siguiente
    dot.render(nombre_archivo, format='png', cleanup=True)
    print(f"Gráfico generado: {nombre_archivo}.png")

def generar_grafico_escritorios(punto_atencion, nombre_archivo="escritorios_activos"):
    """
    Genera un gráfico de los escritorios activos en un punto de atención.
    """
    dot = Digraph(comment='Escritorios Activos')
    actual = punto_atencion.escritorios.primero
    while actual:
        if actual.dato.activo:
            dot.node(str(actual.dato.id), f"Escritorio: {actual.dato.identificacion}")
            if actual.dato.cliente_actual:
                dot.edge(str(actual.dato.id), str(actual.dato.cliente_actual.dpi))
        actual = actual.siguiente
    dot.render(nombre_archivo, format='png', cleanup=True)
    print(f"Gráfico generado: {nombre_archivo}.png")