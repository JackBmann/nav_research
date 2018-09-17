from Graph import Graph
from SearchAlgorithms import dfs, dijkstra


Garph = Graph({(1, 2): 5, (2, 3): 3, (3, 9): 2, (1, 4): 1, (4, 6): 4, (4, 5): 6, (6, 7): 9, (5, 8): 1, (8, 9): 3})

print(Garph.connections)
print(Garph.vertices)
print(Garph.edges)
print(dfs(Garph, 1, 9))
Garph.seen = set()
print(dijkstra(Garph, 1, 9))
