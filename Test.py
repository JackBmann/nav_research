from Graph import Graph, Vertex, Edge
from SearchAlgorithms import dfs, dijkstra, djikstra_heuristic, a_star_heuristic
import GraphDisplay
from networkx import read_shp

one = Vertex(0, 0, 0)
two = Vertex(1, 10, 2)
oneToTwo = Edge(one, two, 5)
three = Vertex(2, 20, 65)
twoToThree = Edge(two, three, 3)
four = Vertex(3, 32, 30)
oneToFour = Edge(one, four, 1)
five = Vertex(4, 9, 40)
fourToFive = Edge(four, five, 6)
six = Vertex(5, 50, 44)
fourToSix = Edge(four, six, 4)
seven = Vertex(6, 60, 5)
sixToSeven = Edge(six, seven, 9)
eight = Vertex(7, 0, 70)
fiveToEight = Edge(five, eight, 1)
nine = Vertex(8, 9, 80)
eightToNine = Edge(eight, nine, 3)
threeToNine = Edge(three, nine, 2)

Garph = Graph([oneToTwo, oneToFour, twoToThree, fourToFive, fourToSix,
               sixToSeven, fiveToEight, eightToNine, threeToNine])
print("Garph Connections: ", Garph.connections)
print("Garph Vertices:    ", Garph.vertices)
print("Garph Edges:       ", Garph.edges)
print()
Garph.write_graph("Test.txt")

NewGraph = Graph.read_graph("Test.txt")
print("Connections:       ", NewGraph.connections)
print("Vertices:          ", NewGraph.vertices)
print("Edges:             ", NewGraph.edges)
print()
NewGraph.write_graph("Test.txt")

dfs_list = dfs(Garph, Garph.get_vertex(0), Garph.get_vertex(8))
dfs_list = dfs_list[::-1]
dfs_str = str(dfs_list[0])
for entry in dfs_list[1:]:
    dfs_str += ", " + str(entry)
print("Depth First Search: ", dfs_str)

Garph.seen = set()
dijkstra_list = dijkstra(Garph, Garph.get_vertex(0), Garph.get_vertex(8), djikstra_heuristic)
dijkstra_list = dijkstra_list[::-1]
dijkstra_str = str(dijkstra_list[0])
for entry in dijkstra_list[1:]:
    dijkstra_str += ", " + str(entry)
print("Dijkstra:           ", dijkstra_str)

Garph.seen = set()
a_star_list = dijkstra(Garph, Garph.get_vertex(0), Garph.get_vertex(8), a_star_heuristic)
a_star_list = a_star_list[::-1]
a_star_str = str(a_star_list[0])
for entry in a_star_list[1:]:
    a_star_str += ", " + str(entry)
print("A*:                 ", a_star_str)

# GraphDisplay.draw_graph(Garph)
GraphDisplay.draw_graph(read_shp(r"C:\Users\wavej\Documents\Research\Campus.shp"))
