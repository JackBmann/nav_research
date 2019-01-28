from Graph import Graph, Vertex, Edge
from SearchAlgorithms import dfs, dijkstra, djikstra_heuristic, a_star_heuristic
import GraphDisplay
from networkx import read_shp
from OSMParser import parse_osm
from datetime import datetime

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

start = datetime.now()
dfs_list = dfs(Garph, Garph.get_vertex(0), Garph.get_vertex(8))
end = datetime.now()
delta = end - start
dfs_list = dfs_list[::-1]
dfs_str = str(dfs_list[0])
for entry in dfs_list[1:]:
    dfs_str += ", " + str(entry)
print("Depth First Search (" + str(delta.seconds) + ":" + str(delta.microseconds) + " seconds): " + dfs_str)
print(dfs_list)
Garph.color_graph(dfs_list)
L = Garph.convert_networkx()
print(L.edges(data=True))
GraphDisplay.draw_graph(L)

Garph.clear_colors()
Garph.seen = set()
start = datetime.now()
dijkstra_list = dijkstra(Garph, Garph.get_vertex(0), Garph.get_vertex(8), djikstra_heuristic)
end = datetime.now()
delta = end - start
dijkstra_list = dijkstra_list[::-1]
dijkstra_str = str(dijkstra_list[0])
for entry in dijkstra_list[1:]:
    dijkstra_str += ", " + str(entry)
print("Dijkstra (" + str(delta.seconds) + ":" + str(delta.microseconds) + " seconds):           ", dijkstra_str)

Garph.seen = set()
start = datetime.now()
a_star_list = dijkstra(Garph, Garph.get_vertex(0), Garph.get_vertex(8), a_star_heuristic)
end = datetime.now()
delta = end - start
a_star_list = a_star_list[::-1]
a_star_str = str(a_star_list[0])
for entry in a_star_list[1:]:
    a_star_str += ", " + str(entry)
print("A* (" + str(delta.seconds) + ":" + str(delta.microseconds) + " seconds):                 ", a_star_str)
print()

# K = read_shp(r"shapefiles\OSMCampus.shp", False)
K = parse_osm('shapefiles/OSMCampus.osm')
L = K.convert_networkx()
print(L.edges(data=True))
#GraphDisplay.draw_graph(L)
