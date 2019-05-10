from Graph import Graph, Vertex, Edge
from SearchAlgorithms import dfs, dijkstra, djikstra_heuristic, a_star_heuristic, \
    mean_heuristic, deviation_heuristic, single_traffic_heuristic, normal_dist_traffic
from GraphDisplay import draw_graph
from networkx import read_shp
from OSMParser import parse_osm
from datetime import datetime


def get_test_graph():
    """
    Creates and returns a simple test graph
    :return: a Graph.py representation of a set graph
    """
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
    """
    Tests the file saving functionality by getting a test graph, writing it to a file,
    and then reading a Graph from that file.
    """
    graph = get_test_graph()
    print_graph(graph)
    graph.write_graph("Test.txt")
    new_graph = Graph.read_graph("test.txt")
    print_graph(new_graph)
    new_graph.write_graph("test.txt")


def print_graph(graph):
    """
    Prints details (connections, vertices, edges, correlations) about the given Graph
    :param graph: a Graph.py representation of a graph
    """
    print("Graph Connections: ", graph.connections)
    print("Graph Vertices:    ", graph.vertices)
    print("Graph Edges:       ", graph.edges)
    print("Graph Correlations:       ", graph.edge_correlation)


def test_graph_algorithm(graph, algorithm, src, dest, name="Path: ", heuristic=None, deadline=None):
    """
    Runs the given algorithm and heuristic on the given graph from src to dest and displays prints and returns the path
    :param graph: a Graph.py representation of a graph
    :param algorithm: an algorithm function from SearchAlgorithms.py
    :param src: a node in graph
    :param dest: a node in graph
    :param name: the name of the path to print out
    :param heuristic: a heuristic function if algorithm accepts one, None otherwise
    :param deadline: a deadline if the algorithm accepts one, None otherwise
    :return: the path from src to dest in graph found by the algorithm, a list of ints
    """
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
    """
    Color the given graph, then convert it to networkx and draw it
    :param graph: a Graph.py representation of a graph
    :param paths: the paths to color on the graph
    :param name: the title to display on the generated graph display
    :param filename: the filename to save the graph display as
    """
    graph.color_graph(paths)
    networkx_graph = graph.convert_networkx()
    draw_graph(networkx_graph, name, filename)


def test_dfs(graph, start, end):
    """
    Run dfs on the given graph from start to dest and display the path.
    :param graph: a Graph.py representation of a graph
    :param start: a vertex in graph
    :param end: a vertex in graph
    """
    paths = [test_graph_algorithm(graph, dfs, start, end, "Depth First Search")]
    color_convert_draw_graph(graph, paths, "Depth First Search", "dfs")
    graph.clear_colors()


def test_dijkstra(graph, start, end):
    """
    Run dijkstra's algorithm w/ dijkstra_heuristic on the given graph from start to dest and display the path.
    :param graph: a Graph.py representation of a graph
    :param start: a vertex in graph
    :param end: a vertex in graph
    """
    paths = [test_graph_algorithm(graph, dijkstra, start, end, "Dijkstra", djikstra_heuristic)]
    color_convert_draw_graph(graph, paths, "Dijkstra", "dijkstra")
    graph.clear_colors()


def test_a_star(graph, start, end):
    """
    Run dijkstra's algorithm w/ a_star_heuristic on the given graph from start to dest and display the path.
    :param graph: a Graph.py representation of a graph
    :param start: a vertex in graph
    :param end: a vertex in graph
    """
    paths = [test_graph_algorithm(graph, dijkstra, start, end, "A*", a_star_heuristic)]
    color_convert_draw_graph(graph, paths, "A*", "a_star")
    graph.clear_colors()


def test_parse_osm(osm_path, title, filename):
    """
    Parse the given osm file, convert it into networkx and display it.
    :param osm_path: a path to an .osm file
    :param title: the title to display on the generated graph display
    :param filename: the filename to save the graph display as
    :return: the generated Graph.py representation of the graph in the .osm file
    """
    # networkx.read_shp("path_to_shapefile") is a way to read shapefiles (.shp extension) but is slow and doesn't
    # get all of the metadata.  It works if you need to clean up an OSM extract and save it as a shapefile.
    # graph = read_shp(osm_path, False)
    graph = parse_osm(osm_path)
    networkx_graph = graph.convert_networkx()
    draw_graph(networkx_graph, title, filename)
    return graph


def test_box_roads():
    """
    Read the graph represented by BoxRoads.txt (a simple city block with individual lanes represented at intersections)
    and run a several algorithms on the graph to show the different outcomes, then color and display it.
    """
    graph = Graph.read_graph("BoxRoads.txt")
    print_graph(graph)
    start = graph.get_vertex(0)
    end = graph.get_vertex(33)
    graph.specify_jams([((10, 0), (0, 10))])
    paths = [test_graph_algorithm(graph, dijkstra, start, end, "Box Roads A*", a_star_heuristic),
             # test_graph_algorithm(graph, dijkstra, start, end, "Box Roads Mean", mean_heuristic),
             # test_graph_algorithm(graph, dijkstra, start, end, "Box Roads Deviation", deviation_heuristic),
             test_graph_algorithm(graph, dijkstra, start, end, "Box Roads Deviation", single_traffic_heuristic),
             test_graph_algorithm(graph, dijkstra, start, end, "Box Roads Normal Dist", normal_dist_traffic, 30)]
    color_convert_draw_graph(graph, paths, "Box Roads", "box_roads")


# Run some algorithms on the test graph
test_graph = get_test_graph()
print_graph(test_graph)
start = test_graph.get_vertex(0)
end = test_graph.get_vertex(8)
test_dfs(test_graph, start, end)
test_dijkstra(test_graph, start, end)
test_a_star(test_graph, start, end)

# Run some algorithms on an OSM extract of UD's Irving campus
osm_graph = test_parse_osm('shapefiles/OSMCampus.osm', "OSM Campus", "osm_campus")
print_graph(osm_graph)
start = osm_graph.get_vertex(list(osm_graph.vertices.keys())[0])
end = osm_graph.get_vertex(list(osm_graph.vertices.keys())[47])
test_dfs(osm_graph, start, end)
test_dijkstra(osm_graph, start, end)
test_a_star(osm_graph, start, end)

# Run some algorithms on the BoxRoads test graph
test_box_roads()
