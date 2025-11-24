# mst_generator.py
import os
import matplotlib.pyplot as plt
import networkx as nx
from django.conf import settings

# --- Datos de ejemplo de los distritos con distancias ---
edges = [
    ("San Isidro", "Miraflores", 4),
    ("San Isidro", "Magdalena", 7),
    ("San Isidro", "La Molina", 12),
    ("Miraflores", "Barranco", 3),
    ("Miraflores", "Surco", 10),
    ("Magdalena", "San Miguel", 6),
    ("San Miguel", "Comas", 15),
    ("Surco", "Los Olivos", 8),
    ("Comas", "Los Olivos", 5),
    ("La Molina", "Surco", 7),
]

def generar_grafo_mst():
    G = nx.Graph()
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    mst = nx.minimum_spanning_tree(G)

    # Layout con semilla para reproducibilidad
    pos = nx.spring_layout(mst, seed=42)

    # Figura más grande para mayor claridad
    plt.figure(figsize=(12, 8))

    # Dibujar nodos y aristas
    nx.draw(
        mst, pos,
        with_labels=True,
        node_size=4000,
        node_color="skyblue",
        font_size=12,
        font_weight="bold",
        width=2,
        edge_color="gray"
    )

    # Etiquetas de pesos en las aristas
    weights = nx.get_edge_attributes(mst, 'weight')
    nx.draw_networkx_edge_labels(mst, pos, edge_labels=weights, font_size=10)

    # Crear carpeta static/RoomFrom si no existe
    ruta_static = os.path.join(settings.BASE_DIR, "mi_app", "static", "RoomFrom")
    os.makedirs(ruta_static, exist_ok=True)
    ruta_archivo = os.path.join(ruta_static, "mst.png")

    # Guardar imagen con márgenes ajustados
    plt.savefig(ruta_archivo, bbox_inches="tight")
    plt.close()

    # Devolver ruta relativa para templates
    return "RoomFrom/mst.png"
