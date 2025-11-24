# dijkstra_graph.py
import os
import matplotlib.pyplot as plt
import networkx as nx
from django.conf import settings
from .grafo import Grafo, DISTANCIAS_DISTRITOS

def generar_grafo_dijkstra(origen):
    """
    Genera un grafo que muestra los caminos más cortos desde 'origen' hacia todos los demás distritos.
    Devuelve la ruta relativa de la imagen.
    """
    G = nx.Graph()
    
    # Agregamos todos los nodos únicos
    nodos = set()
    for u, v, _ in DISTANCIAS_DISTRITOS:
        nodos.add(u)
        nodos.add(v)
    
    for nodo in nodos:
        G.add_node(nodo)
    
    # Agregamos todas las aristas con peso
    for u, v, w in DISTANCIAS_DISTRITOS:
        G.add_edge(u, v, weight=w)
    
    # Usamos tu clase Grafo para calcular distancias
    grafo = Grafo(DISTANCIAS_DISTRITOS)
    caminos = {}

    # Calculamos el camino más corto a cada distrito desde el origen
    for destino in nodos:
        if destino != origen:
            distancia = grafo.dijkstra(origen, destino)
            caminos[destino] = distancia
    
    # Dibujamos el grafo
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10)
    
    # Dibujar etiquetas de peso para todas las aristas
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
    
    # Resaltar los caminos más cortos desde el origen
    for destino in caminos:
        path = nx.shortest_path(G, source=origen, target=destino, weight='weight')
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color="red")
    
    # Guardar imagen
    ruta_static = os.path.join(settings.BASE_DIR, "mi_app", "static", "RoomFrom")
    os.makedirs(ruta_static, exist_ok=True)
    ruta_archivo = os.path.join(ruta_static, "dijkstra.png")
    plt.savefig(ruta_archivo, bbox_inches="tight")
    plt.close()
    
    return "RoomFrom/dijkstra.png"
