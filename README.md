# BasketNetwork — Pass Network Analytics for Basketball

Scripts to build and analyze **basketball passing networks** from play-by-play / event data.
It creates pass networks with **NetworkX**, detects **communities (Louvain)**, computes centrality metrics, and generates **heatmaps**, **temporal trends**, and **player comparisons**.

> Coursework project evolved into a reusable toolkit.

## Features
- Build directed/weighted **pass networks** from a CSV.
- **Community detection** (Louvain) and clustering visualizations.
- Centrality metrics: degree, weighted degree, betweenness, eigenvector.
- **Heatmap** of pass frequencies (player→player).
- **Temporal analysis** per quarter/time window.
- Simple **player comparison** reports.

## Quickstart
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
