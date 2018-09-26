from Graph import Graph
from SearchAlgorithms import dfs, dijkstra, djikstra_heuristic, a_star_heuristic


Garph = Graph({(1, 2): 5, (2, 3): 3, (3, 9): 2, (1, 4): 1, (4, 6): 4, (4, 5): 6, (6, 7): 9, (5, 8): 1, (8, 9): 3})

print("Garph Connections: ", Garph.connections)
print("Garph Vertices:    ", Garph.vertices)
print("Garph Edges:       ", Garph.edges)
print()

dfs_list = dfs(Garph, Garph.getVertex(1), Garph.getVertex(9))
dfs_str = "" + str(dfs_list[0])
for entry in dfs_list[1:]:
    dfs_str += ", " + str(entry)
print("Depth First Search: ", dfs_str)

Garph.seen = set()
dijkstra_list = dijkstra(Garph, Garph.getVertex(1), Garph.getVertex(9), djikstra_heuristic)
dijkstra_str = "" + str(dijkstra_list[0])
for entry in dijkstra_list[1:]:
    dijkstra_str += ", " + str(entry)
print("Dijkstra:           ", dijkstra_str)

Garph.seen = set()
a_star_list = dijkstra(Garph, Garph.getVertex(1), Garph.getVertex(9), a_star_heuristic)
a_star_str = "" + str(a_star_list[0])
for entry in a_star_list[1:]:
    a_star_str += ", " + str(entry)
print("A*:                 ", a_star_str)
