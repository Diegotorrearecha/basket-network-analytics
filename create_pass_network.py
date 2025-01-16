import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

file_path = "CSV_definitive.csv"  # Path to the CSV file
data = pd.read_csv(file_path)  # Load the CSV data into a DataFrame

# Create a directed graph with weighted edges
G = nx.DiGraph()
for index, row in data.iterrows():  # Loop through each row in the DataFrame
    player1 = str(row['Player1'])  # Source node (player)
    player2 = str(row['Player2'])  # Target node (player)
    result = row.get('ResultAction', 'neutral')  # Get the result of the action, default to 'neutral'
    weight = 1.5 if result == 'success' else 1  # Assign higher weight for successful actions
    if G.has_edge(player1, player2):  # If the edge already exists, increase the weight
        G[player1][player2]['weight'] += weight
    else:  # Otherwise, add a new edge with the initial weight
        G.add_edge(player1, player2, weight=weight)

# Analyze the graph by quarters (if applicable)
quarters = data['Cuarter'].unique()  # Get unique quarters from the data
for quarter in quarters:  # Loop through each quarter
    quarter_data = data[data['Cuarter'] == quarter]  # Filter data for the current quarter
    quarter_graph = nx.DiGraph()  # Create a new graph for the quarter
    for index, row in quarter_data.iterrows():  # Build the quarter graph
        player1 = str(row['Player1'])
        player2 = str(row['Player2'])
        result = row.get('ResultAction', 'neutral')
        weight = 1.5 if result == 'success' else 1
        if quarter_graph.has_edge(player1, player2):
            quarter_graph[player1][player2]['weight'] += weight
        else:
            quarter_graph.add_edge(player1, player2, weight=weight)

    density = nx.density(quarter_graph)  # Calculate the density of the quarter graph
    clustering_coefficient = nx.average_clustering(quarter_graph, weight='weight')  # Average clustering coefficient
    print(f"\n--- Analysis for Quarter {quarter} ---")  # Print analysis results for the quarter
    print(f"Density: {density:.4f}")
    print(f"Average Clustering Coefficient: {clustering_coefficient:.4f}")

# Centrality metrics for the entire graph
print("\nCentrality Metrics:")
for node in G.nodes:  # Loop through all nodes in the graph
    in_degree = G.in_degree(node, weight='weight')  # Calculate weighted in-degree
    out_degree = G.out_degree(node, weight='weight')  # Calculate weighted out-degree
    closeness_centrality = nx.closeness_centrality(G, u=node, distance='weight')  # Closeness centrality
    betweenness_centrality = nx.betweenness_centrality(G, weight='weight')[node]  # Betweenness centrality
    print(f"{node} -> In-Degree: {in_degree}, Out-Degree: {out_degree}, Closeness: {closeness_centrality:.4f}, Betweenness: {betweenness_centrality:.4f}")

# Shortest paths to the basket ("BASKET")
print("\nShortest paths to the basket (BASKET):")
for node in G.nodes:
    if node != "BASKET":  # Skip the "BASKET" node itself
        try:
            shortest_path = nx.shortest_path(G, source=node, target="BASKET", weight='weight')  # Find the shortest path
            print(f"Shortest path from {node} to BASKET: {shortest_path}")
        except nx.NetworkXNoPath:  # Handle cases where no path exists
            print(f"No path from {node} to BASKET")

# Team cohesion (clustering coefficients)
print("\nTeam Cohesion:")
avg_clustering = nx.average_clustering(G, weight='weight')  # Calculate the average clustering coefficient
for node in G.nodes:
    clustering_coefficient = nx.clustering(G, node, weight='weight')  # Node-specific clustering coefficient
    print(f"{node} -> Clustering Coefficient: {clustering_coefficient:.4f}")
print(f"Average Clustering Coefficient: {avg_clustering:.4f}")

# Network density
density = nx.density(G)  # Calculate graph density
print(f"Network Density: {density:.4f}")

# Weighted degree (in, out, and total)
print("\nWeighted Degree (in, out, total):")
for node in G.nodes:
    in_degree = G.in_degree(node, weight='weight')  # Weighted in-degree
    out_degree = G.out_degree(node, weight='weight')  # Weighted out-degree
    total_degree = in_degree + out_degree  # Total degree (in + out)
    print(f"{node} -> In: {in_degree}, Out: {out_degree}, Total: {total_degree}")

# Betweenness centrality
print("\nBetweenness Centrality:")
betweenness = nx.betweenness_centrality(G, weight='weight')  # Calculate betweenness centrality for all nodes
for node, centrality in betweenness.items():
    print(f"{node}: {centrality:.4f}")

# Strongest connections (highest weight edges)
print("\nStrongest Connections (highest weight edges):")
strongest_edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)[:20]  # Top 20 strongest edges
for u, v, data in strongest_edges:
    print(f"{u} -> {v}: {data['weight']} passes")

# Export metrics to a CSV file
metrics = []  # Store metrics for all nodes
for node in G.nodes:
    in_degree = G.in_degree(node, weight='weight')
    out_degree = G.out_degree(node, weight='weight')
    total_degree = in_degree + out_degree
    closeness_centrality = nx.closeness_centrality(G, u=node, distance='weight')
    betweenness_centrality = nx.betweenness_centrality(G, weight='weight')[node]
    clustering_coefficient = nx.clustering(G, node, weight='weight')
    metrics.append({  # Add metrics to the list
        "Node": node,
        "In-Degree": in_degree,
        "Out-Degree": out_degree,
        "Total-Degree": total_degree,
        "Closeness Centrality": closeness_centrality,
        "Betweenness Centrality": betweenness_centrality,
        "Clustering Coefficient": clustering_coefficient
    })
metrics_df = pd.DataFrame(metrics)  # Convert the metrics list to a DataFrame
metrics_df.to_csv("player_metrics_weighted.csv", index=False)  # Save the metrics to a CSV file
print(f"\nResults exported to: player_metrics_weighted.csv")  # Confirm export
