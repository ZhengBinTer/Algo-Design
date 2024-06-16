import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time

def generate_random_value(digits):
    value = int(''.join(str(random.choice(digits)) for _ in range(3)))
    # Use the current time to seed the random number generator for variability
    random.seed(value + int(time.time()))
    return value

def create_stars(student_ids):
    sum_id = sum(int(id) for id in student_ids)
    digits = list(set(int(digit) for digit in str(sum_id)))    
    
    stars = []
    for i in range(20):
        x = generate_random_value(digits)
        y = generate_random_value(digits)
        z = generate_random_value(digits)
        weight = generate_random_value(digits)
        profit = generate_random_value(digits)
        star = {
            'name': f'Star{chr(65 + i)}',
            'x': x,
            'y': y,
            'z': z,
            'weight': weight,
            'profit': profit
        }
        stars.append(star)
    return stars

def create_edges(stars):
    graph = nx.Graph()
    for star in stars:
        graph.add_node(star['name'], **star)
    
    for star in stars:
        while len(list(graph.neighbors(star['name']))) < 3:
            potential_targets = [s for s in stars if s['name'] != star['name'] and not graph.has_edge(star['name'], s['name'])]
            if potential_targets:
                target = random.choice(potential_targets)
                graph.add_edge(star['name'], target['name'])

    while len(graph.edges) < 54:
        star1, star2 = random.sample(stars, 2)
        if star1['name'] != star2['name'] and not graph.has_edge(star1['name'], star2['name']):
            graph.add_edge(star1['name'], star2['name'])
    
    return graph

def calculate_distances(graph):
    for edge in graph.edges:
        star1 = graph.nodes[edge[0]]
        star2 = graph.nodes[edge[1]]
        distance = np.sqrt((star2['x'] - star1['x'])**2 + (star2['y'] - star1['y'])**2 + (star2['z'] - star1['z'])**2)
        graph.edges[edge]['distance'] = distance

def save_data(stars, graph):
    with open('stars_data.txt', 'w') as f:
        f.write("Stars Data:\n")
        f.write("Name x y z Weight Profit\n")
        for star in stars:
            f.write(f"{star['name']} {star['x']} {star['y']} {star['z']} {star['weight']} {star['profit']}\n")

    with open('routes_data.txt', 'w') as f:
        f.write("Routes Data:\n")
        f.write("Star_1 Star_2 Distance\n")
        for edge in graph.edges:
            f.write(f"{edge[0]} {edge[1]} {graph.edges[edge]['distance']:.2f}\n")

def draw_graph(graph):
    pos = nx.spring_layout(graph)  # You can use other layouts like spring_layout, shell_layout, etc.
    plt.figure(figsize=(12, 8))

    nx.draw(graph, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=15, font_weight='bold', edge_color='gray')
    edge_labels = nx.get_edge_attributes(graph, 'distance')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels={k: f'{v:.2f}' for k, v in edge_labels.items()})

    plt.title("Star Location Design with Routes")
    plt.show()

# Main code
student_ids = ["1211102810", "1211101506", "1211102809"]

start_time = time.time()  # Start time

stars = create_stars(student_ids)
graph = create_edges(stars)
calculate_distances(graph)
save_data(stars, graph)
#draw_graph(graph)

end_time = time.time()  # End time
generation_time = end_time - start_time

# Print the generation time
print(f"Stars and graph generated in {generation_time:.2f} seconds.")
