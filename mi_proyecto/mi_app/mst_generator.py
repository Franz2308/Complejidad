import matplotlib.pyplot as plt
import networkx as nx

# --- Datos de ejemplo de los distritos con distancias ---
edges = [
    ("San Isidro", "Magdalena", 7),
    ("San Isidro", "Miraflores", 4),
    ("Miraflores", "Barranco", 3),
    ("Magdalena", "San Miguel", 6),
]

def generar_grafo_mst():
    G = nx.Graph()

    # agregar aristas con peso
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    # obtener MST
    mst = nx.minimum_spanning_tree(G)

    # dibujar
    pos = nx.spring_layout(mst)
    plt.figure(figsize=(6, 4))
    nx.draw(mst, pos, with_labels=True, node_size=3000)
    
    weights = nx.get_edge_attributes(mst, 'weight')
    nx.draw_networkx_edge_labels(mst, pos, edge_labels=weights)

    # guardar archivo en static/
    plt.savefig("static/mst.png")
    plt.close()
