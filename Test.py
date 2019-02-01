from Graph import Graph, Vertex, Edge
from SearchAlgorithms import dfs, dijkstra, djikstra_heuristic, a_star_heuristic
import GraphDisplay
from networkx import read_shp
from OSMParser import parse_osm
from datetime import datetime


def get_test_graph():
    one = Vertex(0, 0, 0)
    two = Vertex(1, 10, 2)
    one_two = Edge(one, two, 5)
    three = Vertex(2, 20, 65)
    two_three = Edge(two, three, 3)
    four = Vertex(3, 32, 30)
    one_four = Edge(one, four, 1)
    five = Vertex(4, 9, 40)
    four_five = Edge(four, five, 6)
    six = Vertex(5, 50, 44)
    four_six = Edge(four, six, 4)
    seven = Vertex(6, 60, 5)
    six_seven = Edge(six, seven, 9)
    eight = Vertex(7, 0, 70)
    five_eight = Edge(five, eight, 1)
    nine = Vertex(8, 9, 80)
    eight_nine = Edge(eight, nine, 3)
    three_nine = Edge(three, nine, 2)
    return Graph([one_two, one_four, two_three, four_five, four_six, six_seven, five_eight, eight_nine, three_nine])


def test_save_graph_to_file():
    graph = get_test_graph()
    print("Graph Connections: ", graph.connections)
    print("Graph Vertices:    ", graph.vertices)
    print("Graph Edges:       ", graph.edges)
    print()
    graph.write_graph("Test.txt")
    new_graph = Graph.read_graph("test.txt")
    print("Connections:       ", new_graph.connections)
    print("Vertices:          ", new_graph.vertices)
    print("Edges:             ", new_graph.edges)
    print()
    new_graph.write_graph("test.txt")


def test_dfs():
    graph = get_test_graph()
    test_graph_algorithm(graph, dfs, graph.get_vertex(0), graph.get_vertex(8), None, "Depth First Search")


def test_dijkstra():
    graph = get_test_graph()
    test_graph_algorithm(graph, dijkstra, graph.get_vertex(0), graph.get_vertex(8), djikstra_heuristic, "Dijkstra")


def test_a_star():
    graph = get_test_graph()
    test_graph_algorithm(graph, dijkstra, graph.get_vertex(0), graph.get_vertex(8), a_star_heuristic, "A*")


def test_graph_algorithm(graph, algorithm, src, dest, heuristic, name):
    start = datetime.now()
    if heuristic:
        path = algorithm(graph, src, dest, heuristic)
    else:
        path = algorithm(graph, src, dest)
    end = datetime.now()
    delta = end - start
    path = path[::-1]
    path_str = str(path[0])
    for entry in path[1:]:
        path_str += ", " + str(entry)
    print(name + " (" + str(delta.seconds) + ":" + str(delta.microseconds) + " seconds): ", path_str)
    graph.color_graph(path)
    networkx_graph = graph.convert_networkx()
    GraphDisplay.draw_graph(networkx_graph, name)
    graph.clear_colors()


def test_osm():
    # graph = read_shp(r"shapefiles/OSMCampus.shp", False)
    graph = parse_osm('shapefiles/OSMCampus.osm')
    networkx_graph = osm.convert_networkx()
    GraphDisplay.draw_graph(networkx_graph, "OSM Campus")


test_dfs()
test_dijkstra()
test_a_star()
test_osm()
