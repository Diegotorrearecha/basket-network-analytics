# BasketNetwork — Análisis de redes de pase en baloncesto

Toolkit en **Python** para construir y analizar **redes de pases** a partir de un CSV de eventos. Genera grafos dirigidos/ponderados con **NetworkX**, detecta **comunidades (Louvain)**, calcula **métricas de centralidad**, produce **heatmaps** (player→player), tendencias **temporales** y **comparativas** entre jugadores. Pensado para *scouting*, docencia y análisis exploratorio.

> Proyecto académico evolucionado a herramienta reutilizable. No incluye datos sensibles; se provee un CSV de ejemplo mínimo en `examples/`.

---

##  Características

- Construcción de **red de pases** (dirigida y ponderada, peso = nº de pases).
- **Detección de comunidades** (Louvain) + visualización por clúster.
- **Métricas de red**: in/out-degree (peso y no peso), betweenness, eigenvector, PageRank.
- **Matriz de adyacencia** y **heatmap** de frecuencias de pase.
- **Análisis temporal** por cuarto o ventana móvil (*rolling*).
- **Comparación de jugadores** con KPIs de red y uso del balón.
- Exporta **figuras (PNG)**, **tablas (CSV)** y **grafos (GEXF)** compatibles con **Gephi**.

---

## Instalación

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt


## **Formato del CSV (esquema de datos)**

El toolkit espera un CSV con al menos estas columnas (nombres exactos o renómbralas a estos):

Columna	Tipo	Obligatoria	Descripción
player_from	string	✅	Jugador que realiza el pase
player_to	string	✅	Jugador que recibe el pase
team	string	✅	Equipo del que procede el pase
timestamp	float/str	✅*	Tiempo del evento en segundos (o mm:ss). Alternativa: usar quarter,minute,second
quarter	int	✅*	1–4 (y/o 5+ para prórrogas)
minute	int	✅*	Minuto del cuarto (si no usas timestamp)
second	int	✅*	Segundo del cuarto (si no usas timestamp)
possession_id	int/string	opcional	Identificador de posesión
x_from,y_from	float	opcional	Coordenadas de origen (si existen)
x_to,y_to	float	opcional	Coordenadas de destino (si existen)
result	string	opcional	Éxito del pase, pérdida, tiro, etc.

Debes proporcionar timestamp o el trío (quarter,minute,second).

Ejemplo mínimo (examples/CSV_definitive.csv)
team,player_from,player_to,quarter,minute,second,possession_id
URDANETA,Javi,Herrán,1,9,12,101
URDANETA,Herrán,Unai,1,9,10,101
URDANETA,Unai,Lucas,1,9,08,101
URDANETA,Lucas,Javi,1,7,55,102
URDANETA,Javi,Unai,1,7,52,102
URDANETA,Unai,Lucas,1,7,50,102

Los nombres pueden variar; si cambian, ajústalos en los scripts (variables al inicio).

Se recomienda filtrar eventos no-pase y player_from != player_to.



Resultados (resumen de salidas)
Módulo	Salidas clave	Para qué sirve
create_pass_network.py	network.gexf, edge_list.csv, node_metrics.csv, PNG	Ver estructura global, nodos/aristas clave; abrir en Gephi
community_analysis.py	communities.csv, modularity.txt, community_graph.png	Detectar subgrupos funcionales de pase (quintetos/roles)
heatmap_analysis.py	adjacency.csv, heatmap.png	Frecuencias A→B; detectar conexiones infra/sobre-utilizadas
temporal_analysis.py	temporal_metrics.csv, temporal_trends.png	Evolución por cuartos o en el tiempo; rachas y cambios de distribución de pases
player_comparison.py	players_compare.csv, players_compare.png	Comparar perfiles de red y uso del balón entre jugadores
cluster_plot.py	players_features.csv, cluster_plot.png, clusters.csv	Agrupar jugadores por rol/estilo a partir de métricas de red
