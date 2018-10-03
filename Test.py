from Graph import Graph, Vertex
from SearchAlgorithms import dfs, dijkstra, djikstra_heuristic, a_star_heuristic

one = Vertex(1, 0, 0)
two = Vertex(2, 0, 0)
three = Vertex(3, 0, 0)
four = Vertex(4, 0, 0)
five = Vertex(5, 0, 0)
six = Vertex(6, 0, 0)
seven = Vertex(7, 0, 0)
eight = Vertex(8, 0, 0)
nine = Vertex(9, 0, 0)
Garph = Graph({(one, two): 5, (two, three): 3, (three, nine): 2, (one, four): 1, (four, six): 4, (four, five): 6,
               (six, seven): 9, (five, eight): 1, (eight, nine): 3})

print("Garph Connections: ", Garph.connections)
print("Garph Vertices:    ", Garph.vertices)
print("Garph Edges:       ", Garph.edges)
print()

dfs_list = dfs(Garph, Garph.get_vertex(1), Garph.get_vertex(9))
dfs_str = "" + str(dfs_list[0])
for entry in dfs_list[1:]:
    dfs_str += ", " + str(entry)
print("Depth First Search: ", dfs_str)

Garph.seen = set()
dijkstra_list = dijkstra(Garph, Garph.get_vertex(1), Garph.get_vertex(9), djikstra_heuristic)
dijkstra_str = "" + str(dijkstra_list[0])
for entry in dijkstra_list[1:]:
    dijkstra_str += ", " + str(entry)
print("Dijkstra:           ", dijkstra_str)

Garph.seen = set()
a_star_list = dijkstra(Garph, Garph.get_vertex(1), Garph.get_vertex(9), a_star_heuristic)
a_star_str = "" + str(a_star_list[0])
for entry in a_star_list[1:]:
    a_star_str += ", " + str(entry)
print("A*:                 ", a_star_str)
