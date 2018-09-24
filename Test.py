from Graph import Graph
from SearchAlgorithms import dfs, dijkstra, djikstra_heuristic


Garph = Graph({(1, 2): 5, (2, 3): 3, (3, 9): 2, (1, 4): 1, (4, 6): 4, (4, 5): 6, (6, 7): 9, (5, 8): 1, (8, 9): 3})

print(Garph.connections)
print(Garph.vertices)
print(Garph.edges)
print("0 is : ", Garph.connections[Garph.getVertex(1)])
print("1 is: ", Garph.getVertex(2))
dfs_List = dfs(Garph, Garph.getVertex(1), Garph.getVertex(9))
print("Depth First Search: ")
for entry in dfs_List:
    print(entry.getID())
Garph.seen = set()

lister = dijkstra(Garph, Garph.getVertex(1), Garph.getVertex(9), djikstra_heuristic)
print("Dijkstra:           ")
for entry in lister:
    print(entry.getID())
