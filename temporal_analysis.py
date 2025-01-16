import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

file_path = "CSV_definitive.csv"  # Path to the CSV file
data = pd.read_csv(file_path)  # Load the CSV into a DataFrame

quarter_results = []  # Initialize a list to store results for each quarter
quarters = data['Cuarter'].unique()  # Get the unique quarters from the data

for quarter in quarters:  # Loop through each quarter
    quarter_data = data[data['Cuarter'] == quarter]  
    G = nx.DiGraph()  # Create a directed graph for the quarter

    for index, row in quarter_data.iterrows():  # Iterate through each row of the quarter's data
        player1 = str(row['Player1'])  
        player2 = str(row['Player2'])  # Target player for the interaction
        result = row.get('ResultAction', 'neutral')  
        weight = 1.5 if result == 'success' else 1  
        if G.has_edge(player1, player2):  # If the edge already exists, increase its weight
            G[player1][player2]['weight'] += weight
        else:  
            G.add_edge(player1, player2, weight=weight)

    density = nx.density(G)  # Calculate the density of the graph
    clustering_coefficient = nx.average_clustering(G, weight='weight')  # Calculate the average clustering coefficient
    betweenness = nx.betweenness_centrality(G, weight='weight')  
    closeness = nx.closeness_centrality(G, distance='weight')  # Calculate closeness centrality for nodes
    total_interactions = sum([d['weight'] for _, _, d in G.edges(data=True)])
    
    degrees = [(node, G.degree(node, weight='weight')) for node in G.nodes()]  
    most_active_player = max(degrees, key=lambda x: x[1])  # Find the node with the highest weighted degree

    quarter_results.append({  # Store the results for the current quarter
        "Quarter": quarter,  
        "Density": density, 
        "Clustering": clustering_coefficient,  # Average clustering coefficient
        "Total Interactions": total_interactions,  
        "Most Active Player": most_active_player[0],  
        "Most Active Player Degree": most_active_player[1]  # Highest degree value
    })

    # Print a summary of the current quarter
    print(f"\n--- Análisis para el Cuarto {quarter} ---")
    print(f"Densidad: {density:.4f}")
    print(f"Coeficiente de Clustering Promedio: {clustering_coefficient:.4f}")
    print(f"Interacciones Totales: {total_interactions}")
    print(f"Jugador más activo: {most_active_player[0]} (Grado: {most_active_player[1]:.2f})")

quarter_df = pd.DataFrame(quarter_results)  # Create a DataFrame with the results of all quarters
print("\nResumen por Cuarto:")
print(quarter_df)

plt.figure(figsize=(10, 6))  # Set the figure size for the trend plot
plt.plot(quarter_df['Quarter'], quarter_df['Density'], marker='o', label='Densidad')  
plt.plot(quarter_df['Quarter'], quarter_df['Clustering'], marker='s', label='Clustering Promedio')  
plt.xlabel("Cuarto") 
plt.ylabel("Métrica")  
plt.title("Tendencia de Densidad y Clustering por Cuarto")  
plt.legend() 
plt.grid() 
plt.show() 

quarter_df.to_csv("quarter_analysis.csv", index=False)
print("\nResultados exportados a quarter_analysis.csv")  
