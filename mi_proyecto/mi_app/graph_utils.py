# mi_app/graph_utils.py
from math import radians, cos, sin, sqrt, atan2
from heapq import heappush, heappop
from mi_app.utils import distritos



# Utilidades de distancia (Haversine)

def distancia_km(lat1, lon1, lat2, lon2):
    R = 6371  # radio terrestre km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c


# Construcción de un grafo de distritos (completo) a partir de un dict
# dict esperado: {'Miraflores': (-12.1212, -77.0270), ...}
# Devuelve: adjacency dict {node: [(neighbor, weight_km), ...], ...}

def build_district_graph(distritos):
    graph = {}
    keys = list(distritos.keys())
    for i, a in enumerate(keys):
        lat1, lon1 = distritos[a]
        graph.setdefault(a, [])
        for j in range(i+1, len(keys)):
            b = keys[j]
            lat2, lon2 = distritos[b]
            d = distancia_km(lat1, lon1, lat2, lon2)
            graph[a].append((b, d))
            graph.setdefault(b, [])
            graph[b].append((a, d))
    return graph


# Dijkstra: devuelve distancias mínimas en km desde source a todos
# graph formato: {node: [(neighbor, weight), ...], ...}

def dijkstra(graph, source):
    dist = {node: float('inf') for node in graph}
    dist[source] = 0.0
    pq = [(0.0, source)]
    visited = set()
    while pq:
        d, node = heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        for neigh, w in graph.get(node, []):
            nd = d + w
            if nd < dist[neigh]:
                dist[neigh] = nd
                heappush(pq, (nd, neigh))
    return dist  # en km


# Convertir km a minutos aproximados con velocidad media urbana
# speed_kmh default = 25 km/h -> 60/25 = 2.4 min/km
# Puedes ajustar la velocidad según tu criterio.

def km_to_minutes(km, speed_kmh=25):
    if km is None or km == float('inf'):
        return float('inf')
    return km * (60.0 / float(speed_kmh))

# Función helper: minutos mínimos entre dos distritos (usa dijkstra)

def minutos_entre_distritos(distritos, origen, destino, speed_kmh=25):
    graph = build_district_graph(distritos)
    dist_km = dijkstra(graph, origen)
    km = dist_km.get(destino, float('inf'))
    minutos = km_to_minutes(km, speed_kmh=speed_kmh)
    return minutos


# Kruskal: algoritmo para MST sobre grafo de estudiantes
# nodes: iterable de ids (cualquier hashable)
# edges: lista de tuplas (u, v, weight) donde weight es float (menor = mejor)
# devuelve: list of edges_in_mst [(u,v,w), ...]

class UnionFind:
    def __init__(self, elements):
        self.parent = {e: e for e in elements}
        self.rank = {e: 0 for e in elements}
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True

def kruskal_mst(nodes, edges):
    """
    edges: list of (u, v, weight)
    nodes: iterable of nodes
    """
    uf = UnionFind(nodes)
    # ordenar aristas por peso ascendente (menor peso = preferible)
    edges_sorted = sorted(edges, key=lambda x: x[2])
    mst = []
    for u, v, w in edges_sorted:
        if uf.union(u, v):
            mst.append((u, v, w))
    return mst


# Formar grupos a partir del MST
# - Si threshold está definido (peso máximo aceptable), cortamos aristas > threshold.
# - Si target_group_size está definido, cortamos las (n-1) aristas más grandes hasta aproximar tamaño.
# Devuelve lista de componentes (sets de nodos)

def groups_from_mst(nodes, mst_edges, threshold=None, target_group_size=None):
    # Construir adj list desde MST
    adj = {n: set() for n in nodes}
    for u, v, w in mst_edges:
        adj[u].add((v, w))
        adj[v].add((u, w))

    # Si threshold: eliminamos aristas > threshold
    if threshold is not None:
        # eliminar aristas con peso > threshold
        for u, v, w in list(mst_edges):
            if w > threshold:
                # quitar de adj
                adj[u] = {pair for pair in adj[u] if pair[0] != v}
                adj[v] = {pair for pair in adj[v] if pair[0] != u}

    # Si target_group_size: iterativamente eliminar arista de mayor peso hasta aproximar tamaño
    if target_group_size is not None:
        # ordenar aristas MST por peso descendente
        edges_desc = sorted(mst_edges, key=lambda x: x[2], reverse=True)
        # eliminar aristas hasta que el tamaño máximo de componente <= target_group_size
        for u, v, w in edges_desc:
            # si ya todos componentes pequeños, parar
            components = _connected_components_from_adj(adj)
            max_size = max(len(c) for c in components)
            if max_size <= target_group_size:
                break
            # eliminar arista (u,v)
            adj[u] = {pair for pair in adj[u] if pair[0] != v}
            adj[v] = {pair for pair in adj[v] if pair[0] != u}

    # finalmente devolver componentes
    components = _connected_components_from_adj(adj)
    return components

def _connected_components_from_adj(adj):
    seen = set()
    comps = []
    for node in adj:
        if node in seen:
            continue
        stack = [node]
        comp = set()
        while stack:
            n = stack.pop()
            if n in seen:
                continue
            seen.add(n)
            comp.add(n)
            for neigh, _ in adj[n]:
                if neigh not in seen:
                    stack.append(neigh)
        comps.append(comp)
    return comps
