# grafo.py
class Grafo:
    def __init__(self, aristas=[]):
        self.aristas = []  # lista de tuplas: (peso, u, v)
        self.nodos = set()
        for u, v, peso in aristas:
            self.agregar_arista(u, v, peso)

    def agregar_arista(self, u, v, peso):
        self.aristas.append((peso, u, v))
        self.nodos.add(u)
        self.nodos.add(v)

    # Dijkstra para calcular minutos entre distritos
    def dijkstra(self, inicio, fin):
        import heapq
        adj = {n: [] for n in self.nodos}
        for peso, u, v in self.aristas:
            adj[u].append((v, peso))
            adj[v].append((u, peso))  # grafo no dirigido

        heap = [(0, inicio)]
        dist = {n: float('inf') for n in self.nodos}
        dist[inicio] = 0

        while heap:
            d, nodo = heapq.heappop(heap)
            if nodo == fin:
                return d
            if d > dist[nodo]:
                continue
            for vecino, peso in adj[nodo]:
                if dist[nodo] + peso < dist[vecino]:
                    dist[vecino] = dist[nodo] + peso
                    heapq.heappush(heap, (dist[vecino], vecino))
        return float('inf')

    # Kruskal para MST
    def kruskal(self):
        aristas_ordenadas = sorted(self.aristas)
        padre = {n: n for n in self.nodos}

        def find(n):
            if padre[n] != n:
                padre[n] = find(padre[n])
            return padre[n]

        def union(a, b):
            padre[find(a)] = find(b)

        mst = []
        for peso, u, v in aristas_ordenadas:
            if find(u) != find(v):
                union(u, v)
                mst.append((u, v, peso))
        return mst


# Distancias entre distritos (ejemplo completo)
DISTANCIAS_DISTRITOS = [
    ("Miraflores", "San Miguel", 15),
    ("Miraflores", "San Isidro", 10),
    ("Miraflores", "Surco", 20),
    ("Miraflores", "Los Olivos", 30),
    ("Miraflores", "La Molina", 25),
    ("Miraflores", "Comas", 28),
    ("Miraflores", "Magdalena", 8),

    ("San Miguel", "San Isidro", 12),
    ("San Miguel", "Surco", 22),
    ("San Miguel", "Los Olivos", 18),
    ("San Miguel", "La Molina", 30),
    ("San Miguel", "Comas", 15),
    ("San Miguel", "Magdalena", 5),

    ("San Isidro", "Surco", 18),
    ("San Isidro", "Los Olivos", 25),
    ("San Isidro", "La Molina", 20),
    ("San Isidro", "Comas", 22),
    ("San Isidro", "Magdalena", 7),

    ("Surco", "Los Olivos", 27),
    ("Surco", "La Molina", 12),
    ("Surco", "Comas", 25),
    ("Surco", "Magdalena", 18),

    ("Los Olivos", "La Molina", 10),
    ("Los Olivos", "Comas", 8),
    ("Los Olivos", "Magdalena", 20),

    ("La Molina", "Comas", 28),
    ("La Molina", "Magdalena", 22),

    ("Comas", "Magdalena", 25),
]


# Función auxiliar para cargar MST directamente
def cargar_mst():
    g = Grafo(DISTANCIAS_DISTRITOS)
    return g.kruskal()
