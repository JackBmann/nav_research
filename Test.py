from Graph import Graph
from SearchAlgorithms import Bfs
Garph = Graph({(1, 2): 5, (2, 3): 3, (3, 9): 2, (1, 4): 1, (4, 6): 4, (4, 5): 6, (6, 7): 9, (5, 8): 1, (8, 9): 1})
print(Garph.connections)
print(Garph.vertices)
print(Garph.edges)
print(Bfs(Garph, 1, 9))