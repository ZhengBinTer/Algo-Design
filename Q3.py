import pandas as pd
import heapq
import matplotlib.pyplot as plt
import networkx as nx

# Function to load data from a file
def load_data(filename):
    with open(filename, 'r') as file:
        data = pd.read_csv(file, skiprows=1, sep='\s+')
    return data

# Load data
stars_df = load_data('stars_data.txt')  # Assuming the stars data has the same structure
routes_df = load_data('routes_data.txt')  # Assuming the routes data has the same structure

# Creating the graph from routes data
graph = {}
for index, row in routes_df.iterrows():
    graph.setdefault(row['Star_1'], {})[row['Star_2']] = row['Distance']
    graph.setdefault(row['Star_2'], {})[row['Star_1']] = row['Distance']

# -------------------------------------Above is the Load data used by this 2 sub question-------------------------------------#

# Dijkstra's Algorithm
def dijkstra(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    previous_vertices = {vertex: None for vertex in graph}
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))
    return distances, previous_vertices

# Reconstruct the shortest path from start to end
def get_shortest_path(previous_vertices, start, end):
    path = []
    current_vertex = end
    while current_vertex is not None:
        path.append(current_vertex)
        current_vertex = previous_vertices[current_vertex]
    path = path[::-1]
    if path[0] == start:
        return path
    else:
        return []

# Compute shortest paths from StarA to StarB and save the output
start_node = 'StarA'
end_node = 'StarB'  # Specify the end node
shortest_paths, previous_vertices = dijkstra(graph, start_node)
shortest_path = get_shortest_path(previous_vertices, start_node, end_node)
shortest_distance = shortest_paths[end_node]


# Compute shortest paths from StarA and save all distances to a file
shortest_paths, previous_vertices = dijkstra(graph, 'StarA')
with open('shortest_paths.txt', 'w') as f:
    for star, distance in shortest_paths.items():
        if star != start_node:  # Avoid duplicating the start node's path
            path = get_shortest_path(previous_vertices, start_node, star)
            if path:
                f.write(f"Shortest path from {start_node} to {star}: {' -> '.join(path)}\n")
                f.write(f"Total distance: {distance:.2f}\n")
            else:
                f.write(f"No path from {start_node} to {star} found.\n")

# -------------------------------------Second Question in the Q3 -------------------------------------#

# Kruskal's Algorithm
def find(parent, i):
    if parent[i] == i:
        return i
    return find(parent, parent[i])

def union(parent, rank, x, y):
    root_x = find(parent, x)
    root_y = find(parent, y)
    if rank[root_x] < rank[root_y]:
        parent[root_x] = root_y
    elif rank[root_x] > rank[root_y]:
        parent[root_y] = root_x
    else:
        parent[root_y] = root_x
        rank[root_x] += 1

def kruskal(graph):
    edges = [(u, v, w) for u, adj in graph.items() for v, w in adj.items() if u < v]
    parent = {node: node for node in graph}
    rank = {node: 0 for node in graph}
    mst = []
    for u, v, w in sorted(edges, key=lambda x: x[2]):
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            mst.append((u, v, w))
    return mst

# Compute the Minimum Spanning Tree
mst = kruskal(graph)

# Save the MST to a file
with open('mst.txt', 'w') as f:
    for u, v, weight in mst:
        f.write(f"{u} - {v}: {weight}\n")


def draw_graph(edges, title, label_edges=True):
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    pos = nx.spring_layout(G, k=1500, iterations=155)
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_weight='bold')
    
    if label_edges:
        edge_labels = {(u, v): f"{d:.2f}" for u, v, d in edges}
        ax = plt.gca()
        
        for (u, v, w) in edges:
            (x1, y1), (x2, y2) = pos[u], pos[v]
            # Position the label at the end of the edge
            label_pos = (0.8 * x2 + 0.2 * x1, 0.8 * y2 + 0.2 * y1)
            ax.text(label_pos[0], label_pos[1], f"{w:.2f}", size=10, color='black', ha='center', va='center')

    plt.title(title)
    plt.show()

shortest_path_edges = [(prev, vert, graph[prev][vert]) for vert, prev in previous_vertices.items() if prev]
draw_graph(shortest_path_edges, "Shortest Paths from StarA")

# Drawing the MST graph
draw_graph(mst, "Minimum Spanning Tree")


