from Graph import Graph, Vertex, Edge
from SearchAlgorithms import dfs, dijkstra, djikstra_heuristic, a_star_heuristic, \
    mean_heuristic, deviation_heuristic, single_traffic_heuristic, normal_dist_traffic
from GraphDisplay import draw_graph
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
    print_graph(graph)
    graph.write_graph("Test.txt")
    new_graph = Graph.read_graph("test.txt")
    print_graph(new_graph)
    new_graph.write_graph("test.txt")


def print_graph(graph):
    print("Graph Connections: ", graph.connections)
    print("Graph Vertices:    ", graph.vertices)
    print("Graph Edges:       ", graph.edges)
    print("Graph Correlations:       ", graph.edge_correlation)


def test_graph_algorithm(graph, algorithm, src, dest, heuristic, name, deadline=None):
    start = datetime.now()
    if heuristic:
        path = algorithm(graph, src, dest, heuristic, deadline=deadline)
    else:
        path = algorithm(graph, src, dest)
    end = datetime.now()
    delta = end - start
    path = path[::-1]
    path_str = str(path[0])
    for entry in path[1:]:
        path_str += ", " + str(entry)
    print('{:<15}'.format(name) + " (" + '{:0>5}:{:0>6}'.format(str(delta.seconds), str(delta.microseconds)) +
          " seconds): ", path_str)
    return path


def color_convert_draw_graph(graph, paths, name, filename):
    graph.color_graph(paths)
    networkx_graph = graph.convert_networkx()
    draw_graph(networkx_graph, name, filename)


def test_dfs(graph, start, end):
    paths = [test_graph_algorithm(graph, dfs, start, end, None, "Depth First Search")]
    color_convert_draw_graph(graph, paths, "Depth First Search", "dfs")
    graph.clear_colors()


def test_dijkstra(graph, start, end):
    paths = [test_graph_algorithm(graph, dijkstra, start, end, djikstra_heuristic, "Dijkstra")]
    color_convert_draw_graph(graph, paths, "Dijkstra", "dijkstra")
    graph.clear_colors()


def test_a_star(graph, start, end):
    paths = [test_graph_algorithm(graph, dijkstra, start, end, a_star_heuristic, "A*")]
    color_convert_draw_graph(graph, paths, "A*", "a_star")
    graph.clear_colors()


def test_parse_osm(osm_path):
    # graph = read_shp(osm_path, False)
    graph = parse_osm(osm_path)
    networkx_graph = graph.convert_networkx()
    draw_graph(networkx_graph, "OSM Campus", "osm_campus")
    return graph


def test_osm_dfs(graph, start, end):
    paths = [test_graph_algorithm(graph, dfs, start, end, None, "OSM DFS")]
    color_convert_draw_graph(graph, paths, "OSM DFS", "osm_dfs")
    graph.clear_colors()


def test_osm_dijkstra(graph, start, end):
    paths = [test_graph_algorithm(graph, dijkstra, start, end, djikstra_heuristic, "OSM Dijkstra")]
    color_convert_draw_graph(graph, paths, "OSM Dijkstra", "osm_dijkstra")
    graph.clear_colors()


def test_osm_a_star(graph, start, end):
    paths = [test_graph_algorithm(graph, dijkstra, start, end, a_star_heuristic, "OSM A*")]
    color_convert_draw_graph(graph, paths, "OSM A*", "osm_a_star")
    graph.clear_colors()


def test_box_roads():
    graph = Graph.read_graph("BoxRoads.txt")
    print_graph(graph)
    start = graph.get_vertex(0)
    end = graph.get_vertex(33)
    paths = [test_graph_algorithm(graph, dijkstra, start, end, a_star_heuristic, "Box Roads A*"),
             # test_graph_algorithm(graph, dijkstra, start, end, mean_heuristic, "Box Roads Mean"),
             # test_graph_algorithm(graph, dijkstra, start, end, deviation_heuristic, "Box Roads Deviation"),
             test_graph_algorithm(graph, dijkstra, start, end, single_traffic_heuristic, "Box Roads Deviation"),
             test_graph_algorithm(graph, dijkstra, start, end, normal_dist_traffic, "Box Roads Normal Dist", 100)]
    color_convert_draw_graph(graph, paths, "Box Roads", "box_roads")


def parse_and_prepare_downtown():
    Graph = parse_osm('shapefiles/DowntownDallas.osm')
    Graph.write_graph('DowntownDallas.txt')


# test_graph = get_test_graph()
# print_graph(test_graph)
# start = test_graph.get_vertex(0)
# end = test_graph.get_vertex(8)
# test_dfs(test_graph, start, end)
# test_dijkstra(test_graph, start, end)
# test_a_star(test_graph, start, end)
#
# osm_graph = test_parse_osm('shapefiles/OSMCampus.osm')
# print_graph(osm_graph)
# start = osm_graph.get_vertex(list(osm_graph.vertices.keys())[0])
# end = osm_graph.get_vertex(list(osm_graph.vertices.keys())[47])
# test_osm_dfs(osm_graph, start, end)
# test_osm_dijkstra(osm_graph, start, end)
# test_osm_a_star(osm_graph, start, end)

# test_box_roads()
parse_and_prepare_downtown()
