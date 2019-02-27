from Graph import Graph, Vertex, Edge
from SearchAlgorithms import dfs, dijkstra, djikstra_heuristic, a_star_heuristic
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


def test_graph_algorithm(graph, algorithm, src, dest, heuristic, name, filename):
    graph.clear_colors()
    print_graph(graph)
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
    print('{:<15}'.format(name) + " (" + '{:0>5}:{:0>6}'.format(str(delta.seconds), str(delta.microseconds)) +
          " seconds): ", path_str)
    graph.color_graph(path)
    networkx_graph = graph.convert_networkx()
    draw_graph(networkx_graph, name, filename)


def test_dfs(graph):
    test_graph_algorithm(graph, dfs, graph.get_vertex(0), graph.get_vertex(8), None,
                         "Depth First Search", "dfs")


def test_dijkstra(graph):
    test_graph_algorithm(graph, dijkstra, graph.get_vertex(0), graph.get_vertex(8), djikstra_heuristic,
                         "Dijkstra", "dijkstra")


def test_a_star(graph):
    test_graph_algorithm(graph, dijkstra, graph.get_vertex(0), graph.get_vertex(8), a_star_heuristic,
                         "A*", "a_star")


def test_parse_osm(osm_path):
    # graph = read_shp(osm_path, False)
    graph = parse_osm(osm_path)
    networkx_graph = graph.convert_networkx()
    draw_graph(networkx_graph, "OSM Campus", "osm_campus")


def test_osm_dfs(graph):
    test_graph_algorithm(graph, dfs, graph.get_vertex(list(graph.vertices.keys())[0]),
                         graph.get_vertex(list(graph.vertices.keys())[47]), None,
                         "OSM DFS", "osm_dfs")


def test_osm_dijkstra(graph):
    test_graph_algorithm(graph, dijkstra, graph.get_vertex(list(graph.vertices.keys())[0]),
                         graph.get_vertex(list(graph.vertices.keys())[47]), djikstra_heuristic,
                         "OSM Dijkstra", "osm_dijkstra")


def test_osm_a_star(graph):
    test_graph_algorithm(graph, dijkstra, graph.get_vertex(list(graph.vertices.keys())[0]),
                         graph.get_vertex(list(graph.vertices.keys())[47]), a_star_heuristic,
                         "OSM A*", "osm_a_star")


def test_box_roads():
    graph = Graph.read_graph("BoxRoads.txt")
    print_graph(graph)
    test_graph_algorithm(graph, dijkstra, graph.get_vertex(0), graph.get_vertex(33), a_star_heuristic,
                         "Box Roads A*", "box_roads")


def fix_box_roads():
    with open("BoxRoads.txt", 'r') as openFile:
        with open("ModBoxRoads.txt", 'w') as writeFile:
            vert_flag = 0
            edge_flag = 0
            for line in openFile:
                if line == '\n':
                    writeFile.write(line)
                    continue
                line = line.strip()
                if line == "VERTICES":
                    writeFile.write(line + '\n')
                    vert_flag = 1
                    continue
                if line == "EDGES":
                    writeFile.write(line + '\n')
                    vert_flag = 0
                    edge_flag = 1
                    continue
                if vert_flag > 0:
                    parsed = line.split(',')
                    p_line = str(int(parsed[0]) - 1) + ',' + parsed[1] + ',' + parsed[2] + '\n'
                    writeFile.write(p_line)

                if edge_flag > 0:
                    parsed = line.split(',')
                    p_line = str(int(parsed[0]) - 1) + ',' + str(int(parsed[1]) - 1) + ',' + parsed[2] + '\n'
                    writeFile.write(p_line)


# test_graph = get_test_graph()
# test_dfs(test_graph)
# test_dijkstra(test_graph)
# test_a_star(test_graph)
# test_parse_osm('shapefiles/OSMCampus.osm')
# osm_graph = parse_osm('shapefiles/OSMCampus.osm')
# test_osm_dfs(osm_graph)
# test_osm_dijkstra(osm_graph)
# test_osm_a_star(osm_graph)
test_box_roads()
