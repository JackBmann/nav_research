from Graph import Graph, Vertex, Edge
from SearchAlgorithms import dfs, dijkstra, djikstra_heuristic, a_star_heuristic

one = Vertex(0, 0, 0)
two = Vertex(1, 0, 0)
oneToTwo = Edge(one, two, 5)
three = Vertex(2, 0, 0)
twoToThree = Edge(two, three, 3)
four = Vertex(3, 0, 0)
oneToFour = Edge(one, four, 1)
five = Vertex(4, 0, 0)
fourToFive = Edge(four, five, 6)
six = Vertex(5, 0, 0)
fourToSix = Edge(four, six, 4)
seven = Vertex(6, 0, 0)
sixToSeven = Edge(six, seven, 9)
eight = Vertex(7, 0, 0)
fiveToEight = Edge(five, eight, 1)
nine = Vertex(8, 0, 0)
eightToNine = Edge(eight, nine, 3)
threeToNine = Edge(three, nine, 2)
Garph = Graph([oneToTwo, oneToFour, twoToThree, fourToFive, fourToSix,
               sixToSeven, fiveToEight, eightToNine, threeToNine])
Garph.write_graph("Test.txt")
NewGraph = Graph.read_graph("none", "Test.txt")
print(NewGraph.connections)
print(NewGraph.vertices)
print(NewGraph.edges)
NewGraph.write_graph("Test.txt")

print("Garph Connections: ", Garph.connections)
print("Garph Vertices:    ", Garph.vertices)
print("Garph Edges:       ", Garph.edges)
print()

dfs_list = dfs(Garph, Garph.get_vertex(0), Garph.get_vertex(8))
dfs_str = "" + str(dfs_list[0])
for entry in dfs_list[1:]:
    dfs_str += ", " + str(entry)
print("Depth First Search: ", dfs_str)

Garph.seen = set()
dijkstra_list = dijkstra(Garph, Garph.get_vertex(0), Garph.get_vertex(8), djikstra_heuristic)
dijkstra_str = "" + str(dijkstra_list[0])
for entry in dijkstra_list[1:]:
    dijkstra_str += ", " + str(entry)
print("Dijkstra:           ", dijkstra_str)

Garph.seen = set()
a_star_list = dijkstra(Garph, Garph.get_vertex(0), Garph.get_vertex(8), a_star_heuristic)
a_star_str = "" + str(a_star_list[0])
for entry in a_star_list[1:]:
    a_star_str += ", " + str(entry)
print("A*:                 ", a_star_str)
