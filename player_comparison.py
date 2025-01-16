import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV file
file_path = "CSV_definitive.csv"
data = pd.read_csv(file_path)

# Initialize results
quarter_results = []
quarters = data['Cuarter'].unique()

for quarter in quarters:
    quarter_data = data[data['Cuarter'] == quarter]
    G = nx.DiGraph()  # Create a directed graph for the quarter
    
    # Build the graph based on player interactions
    for index, row in quarter_data.iterrows():
        player1 = str(row['Player1'])
        player2 = str(row['Player2'])
        result = row.get('ResultAction', 'neutral')  # Check action result
        weight = 1.5 if result == 'success' else 1  # Assign higher weight to successful actions
        if G.has_edge(player1, player2):
            G[player1][player2]['weight'] += weight  # Update weight if the edge exists
        else:
            G.add_edge(player1, player2, weight=weight)  # Create a new edge with the weight

    # Calculate network metrics
    density = nx.density(G)  # Network density
    clustering_coefficient = nx.average_clustering(G, weight='weight')  # Weighted clustering coefficient
    betweenness = nx.betweenness_centrality(G, weight='weight')  # Weighted betweenness centrality
    closeness = nx.closeness_centrality(G, distance='weight')  # Weighted closeness centrality
    total_interactions = sum([d['weight'] for _, _, d in G.edges(data=True)])  # Total weighted interactions

    # Identify the most active player based on weighted degree
    degrees = [(node, G.degree(node, weight='weight')) for node in G.nodes()]
    most_active_player = max(degrees, key=lambda x: x[1])

    # Store the results for the quarter
    quarter_results.append({
        "Quarter": quarter,
        "Density": density,
        "Clustering": clustering_coefficient,
        "Total Interactions": total_interactions,
        "Most Active Player": most_active_player[0],
        "Most Active Player Degree": most_active_player[1]
    })

    # Print quarter analysis
    print(f"\n--- Analysis for Quarter {quarter} ---")
    print(f"Density: {density:.4f}")
    print(f"Average Clustering Coefficient: {clustering_coefficient:.4f}")
    print(f"Total Interactions: {total_interactions}")
    print(f"Most Active Player: {most_active_player[0]} (Degree: {most_active_player[1]:.2f})")

# Create a DataFrame with the results for each quarter
quarter_df = pd.DataFrame(quarter_results)
print("\nSummary by Quarter:")
print(quarter_df)

# Plot density and clustering trends
plt.figure(figsize=(10, 6))
plt.plot(quarter_df['Quarter'], quarter_df['Density'], marker='o', label='Density')  # Plot density
plt.plot(quarter_df['Quarter'], quarter_df['Clustering'], marker='s', label='Avg Clustering')  # Plot clustering
plt.xlabel("Quarter")
plt.ylabel("Metric")
plt.title("Density and Clustering Trends by Quarter")
plt.legend()
plt.grid()
plt.show()

# Export results to a CSV file
quarter_df.to_csv("quarter_analysis.csv", index=False)  # Save to CSV
print("\nResults exported to quarter_analysis.csv")
