import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

file_path = "CSV_definitive.csv"  
data = pd.read_csv(file_path)  

G = nx.DiGraph()  # Create a directed graph
for index, row in data.iterrows():  # Loop through each row of the DataFrame
    player1 = str(row['Player1'])  
    player2 = str(row['Player2'])  
    result = row.get('ResultAction', 'neutral')  
    weight = 1.5 if result == 'SUCCESS' else 1  # Assign weight based on success or not
    if G.has_edge(player1, player2):  
        G[player1][player2]['weight'] += weight
    else:  #ht
        G.add_edge(player1, player2, weight=weight)

shooting_weights = []  # This will store shot weights for each player
for node in G.nodes: 
    if node == "BASKET":  # Skip the "BASKET" node
        continue
    out_edges = G.out_edges(node, data=True)  # Get all outgoing edges from the node
    shot_weight = sum([d['weight'] for u, v, d in out_edges if v == "BASKET"])  
    shooting_weights.append(shot_weight) 

mean_shots = np.mean(shooting_weights)  # Calculate the average shot weight

passers = []  # List for players classified as passers and shooters
shooters = []  
for node in G.nodes:  # Loop through each node again
    if node == "BASKET":  
        continue
    out_edges = G.out_edges(node, data=True)  
    shot_weight = sum([d['weight'] for u, v, d in out_edges if v == "BASKET"])  
    if shot_weight > mean_shots:  
        shooters.append(node)  
    else:
        passers.append(node)  

print("\nPlayer classification:")  
print(f"Passers: {passers}")  
print(f"Shooters (above average): {shooters}") 

color_map = {}  # Dictionary to map nodes to colors
for node in passers:  # Assign a color for passers
    color_map[node] = '#A2D5F2'  # Light blue for passers
for node in shooters:  # Assign a color for shooters
    color_map[node] = '#B6EFA1'  # Light green for shooters
color_map["BASKET"] = '#F2A2A2'  # Assign red for the "BASKET" node

colors = [color_map[node] for node in G.nodes]  # Create a list of colors for each node

weights = [G[u][v]['weight'] for u, v in G.edges()]  # List of edge weights to vary edge thickness

pos = nx.spring_layout(G, seed=42)  # Generate graph layout using spring layout
pos["BASKET"] = (0.5, 0.5)  

plt.figure(figsize=(12, 10))  # Set the figure size for the plot

node_sizes = [700 + 300 * nx.degree(G, node) for node in G.nodes]  # Adjust node sizes based on degree

nx.draw(  
    G, pos, with_labels=True,  
    node_color=colors, edge_color='gray', width=[w * 0.5 for w in weights], node_size=node_sizes 
)

edge_labels = nx.get_edge_attributes(G, 'weight') 
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)  

legend_elements = [  
    Line2D([0], [0], marker='o', color='w', label='Passers', markerfacecolor='#A2D5F2', markersize=10),  
    Line2D([0], [0], marker='o', color='w', label='Shooters', markerfacecolor='#B6EFA1', markersize=10),  
    Line2D([0], [0], marker='o', color='w', label='BASKET', markerfacecolor='#F2A2A2', markersize=10)  
]
plt.legend(handles=legend_elements, loc='upper right')  

plt.title("Passers and Shooters Classification (BASKET Centered)", fontsize=16)  
plt.show()  

plt.savefig("player_roles_basket_centered.png", dpi=300)  # Save the graph as an image with high resolution
