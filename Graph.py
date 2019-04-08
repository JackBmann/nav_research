"""
Created By Michael Bolot and John (Jack) Baumann for Fall 2018 - Spring 2019 research
"""
import networkx
from sys import maxsize
from random import choice


class Graph:
    """
    Graph Class
    :field vertices: A list of vertices contained by the graph (uses vertex objects)
    :field edges: A dictionary of the edges. Key is a tuple of (src, dest) and value is distance, an int
    :field connections: a dictionary of edges. Key is source, value is destination
    :field seen: a table of seen vertices
    """
    vertices = {}  # list of vertices contained by the graph
    edges = {}  # dictionary of edges in the graph. Key is a tuple of (src,dest) and value is an edge object
    connections = {}  # dictionary of edges. Key is src, value is dest
    seen = {}
    node_colors = {}
    edge_colors = {}
    current_node = 0
    optimal_color = 2  # 2 means the edge is on an optimal path, 1 means it is a jam, 0 means it is just an edge
    edge_correlation = []
    jams = set()    # set of the jammed edges, for traffic model evaluation

    def __init__(self, edges, correlations=None):
        """
        Constructor for the Graph Class
        Currently are bidirectional paths
        :param edges: A list of edges in the graph
        """

        # first, reset any coloring or edge_identifiers that are left over
        global edge_identifier_iterator
        self.clear_colors()
        edge_identifier_iterator = 0
        self.jams = set()

        vertices = {}
        connections = {}
        parsed_edges = {}
        for edge in edges:
            first_vertex = edge.first_vertex
            second_vertex = edge.second_vertex

            if first_vertex.get_identifier() not in vertices:
                vertices[first_vertex.get_identifier()] = first_vertex
            else:
                first_vertex = vertices[first_vertex.get_identifier()]

            if second_vertex.get_identifier() not in vertices:
                vertices[second_vertex.get_identifier()] = second_vertex
            else:
                second_vertex = vertices[second_vertex.get_identifier()]

            if first_vertex not in connections:
                connections[first_vertex] = [second_vertex]
            else:
                connections[first_vertex].append(second_vertex)

            parsed_edges[(first_vertex, second_vertex)] = edge
        self.edges = parsed_edges
        self.vertices = vertices
        self.connections = connections
        if self.positive_speed_limit():
            #  if we have at least one speed that we can expand off of, then extrapolate the speeds
            self.expand_speeds()
            self.calculate_travel_times()
        if not correlations or len(correlations) == 0:
            self.edge_correlation = [[None for i in range(len(self.edges))]for j in range(len(self.edges))]  # first fill in the array for the entries
            # we will arbitrarily fill in the list, so it is necessary to have a properly filled array
            self.create_correlations()
        else:
            self.edge_correlation = correlations

        self.create_jams(int(len(self.edges) * 0.05)) # jam 5% of roads (rounded down)

    def create_edge_connections(self):
        """
        views the vertexes as edges and the edges as vertexes
        constructs adjacencies based on that view
        :return: a dict from an edge to a set of edges representing these adjacencies
        """
        connections = {}
        for edge in self.edges:
            edge_obj = self.edges[edge]
            if edge_obj.identifier not in connections:
                connections[edge_obj.identifier] = set()
            second_vert = edge_obj.second_vertex
            if second_vert not in self.connections:
                continue
            for third_vert in self.connections[second_vert]:
                connected_edge = self.edges[(second_vert, third_vert)]
                connections[edge_obj.identifier].add(connected_edge.identifier)
                if connected_edge.identifier not in connections:
                    connections[connected_edge.identifier] = set()
                connections[connected_edge.identifier].add(edge_obj.identifier)
        return connections

    def edge_distance(self):
        """
        Uses floyd-warshall to fill in the distances
        :return: void
        """
        connections = self.create_edge_connections()
        distances = [[maxsize for i in range(len(self.edges))] for j in range(len(self.edges))]
        for start_edge in connections:
            for end_edge in connections[start_edge]:
                distances[start_edge][end_edge] = 1
        for edge in self.edges:
            edge_obj = self.edges[edge]
            distances[edge_obj.identifier][edge_obj.identifier] = 0
        for edge in self.edges:
            k = self.edges[edge].identifier
            for second_edge in self.edges:
                i = self.edges[second_edge].identifier
                for third_edge in self.edges:
                    j = self.edges[third_edge].identifier
                    if distances[i][j] > distances[i][k] + distances[k][j]:
                        distances[i][j] = distances[i][k] + distances[k][j]
        return distances

    def create_correlations(self):
        """
        Spreads the correlations out through the whole graph
        Currently very slow, distances are being re-calculated
        Can be solved by passing in a dict in this function
        :return: None
        """
        distances = self.edge_distance()
        print("Distances is: ", distances)
        for edge in self.edges:
            first_edge = self.edges[edge]
            for other_edge in self.edges:
                second_edge = self.edges[other_edge]
                distance = distances[first_edge.get_identifier()][second_edge.get_identifier()]
                if not distance:
                    corr = 0
                else:
                    corr = 0.9**float(distance)
                self.edge_correlation[first_edge.get_identifier()][second_edge.get_identifier()] = corr

    def connected(self, src, dest):
        """
        Checks if two vertices are immediately connected in the graph
        :param src: the source vertex
        :param dest: the destination vertex
        :return: boolean connected
        """
        if dest in self.connections[src]:
            return True
        return False

    def get_vertex(self, vertex_id):
        """
        Returns the vertex object associated with the id
        :param vertex_id: the id of the vertex
        :return: vertex, the found vertex
        """
        vertex = self.vertices[vertex_id]
        return vertex

    def distance(self, src, dest):
        """
        Finds the distance between two connected vertices
        :param src: the source vertex
        :param dest: the destination vertex
        :return: number dist, which is non-zero unless src == dest or connected(src,dest) == False
        """
        if not self.connected(src, dest):
            return 0
        else:
            return self.edges[(src, dest)].weight

    def add_seen(self, vertex):
        if vertex not in self.seen:
            self.seen[vertex] = self.current_node
            self.current_node += 1

    def color_graph(self, paths):
        """
        Colors a graph's edges and vertices
        :param paths: the optimal paths to be highlighted in the display (list of lists)
        :return: void, all changes will be made to structures in the graph object
        """
        self.node_colors = self.seen  # seen already contains information that can be used to color the nodes
        if len(paths) > 1:
            self.node_colors = {}
        for j in range(len(paths)):
            path = paths[j]
            if len(path) < 2:
                # if the path doesn't have at least 2 nodes, it is malformed
                continue
            current_edge = (path[0], path[1])
            self.edge_colors[current_edge] = self.optimal_color
            for i in range(2, len(path)):
                current_edge = (current_edge[1], path[i])
                self.edge_colors[current_edge] = self.optimal_color + j
        for jam in self.jams:
            self.edge_colors[jam.get_first_vertex(), jam.get_second_vertex()] = 1

    def zero_speed_limit(self):
        """
        finds if any roads have no speed_limit
        :return: boolean (true if exists, false otherwise)
        """
        for edge in self.edges:
            if self.edges[edge].get_speed_limit() == 0:
                return True
        return False

    def positive_speed_limit(self):
        """
        finds if any road has a speed_limit
        :return: boolean (true if exists, false otherwise)
        """
        for edge in self.edges:
            if self.edges[edge].get_speed_limit():
                return True
        return False

    def expand_speeds(self):
        """
        expands the speed limit of valid roads to 0-marked roads
        :return: None
        """
        while self.zero_speed_limit():
            for vertex_id, first_vert in enumerate(self.vertices):
                if first_vert not in self.connections:
                    continue
                for second_vert in self.connections[first_vert]:
                    start_edge = self.edges[(first_vert, second_vert)]
                    if start_edge.get_speed_limit() == 0:
                        if second_vert not in self.connections:
                            continue
                        for third_vert in self.connections[second_vert]:
                            current_limit = self.edges[(second_vert, third_vert)].get_speed_limit()
                            if current_limit == 0:
                                continue
                            if current_limit > 40:
                                current_limit -= 5
                                if current_limit < 40:
                                    current_limit = 40
                            start_edge.speed_limit = current_limit
                            break
                    else:
                        if second_vert not in self.connections:
                            continue
                        current_limit = start_edge.get_speed_limit()
                        if current_limit > 40:
                            current_limit -= 5
                            if current_limit < 40:
                                current_limit = 40
                        for third_vert in self.connections[second_vert]:
                            if self.edges[(second_vert, third_vert)].get_speed_limit() == 0:
                                self.edges[(second_vert, third_vert)].speed_limit = current_limit

    def calculate_travel_times(self):
        for edge in self.edges:
            if not self.edges[edge].get_average_time():
                speed = self.edges[edge].get_speed_limit()
                distance = self.edges[edge].get_distance()
                travel_time = distance / speed
                self.edges[edge].set_average_time(travel_time)

    def create_jam(self):
        # this code found at: https://stackoverflow.com/questions/4859292/how-to-get-a-random-value-in-python-dictionary
        vert_edge = choice(list(self.edges.keys()))
        true_edge = self.edges[vert_edge]
        while true_edge in self.jams:
            vert_edge = choice(list(self.edges.keys()))
            true_edge = self.edges[vert_edge]
        self.jams.add(true_edge)

    def create_jams(self, num_jams):
        for i in range(num_jams):
            self.create_jam()

    def clear_colors(self):
        """
        clears the seen hash_table which marks nodes
        :return: void
        """
        self.seen = {}
        self.edge_colors = {}
        self.node_colors = {}
        self.optimal_color = 0
        self.current_node = 0

    def convert_networkx(self):
        """
        Converts a graph into a networkx graph
        :return: A networkx graph object
        """
        new_graph = networkx.DiGraph()
        for vertex in self.vertices:
            vertex_obj = self.vertices[vertex]
            node_color = 0
            if vertex_obj in self.node_colors:
                node_color = self.node_colors[vertex_obj]
            new_graph.add_node((vertex_obj.get_latitude(), vertex_obj.get_longitude()), color=node_color)
        for edge in self.edges:
            edge_obj = self.edges[edge]
            first_vertex = (edge_obj.first_vertex.get_latitude(), edge_obj.first_vertex.get_longitude())
            second_vertex = (edge_obj.second_vertex.get_latitude(), edge_obj.second_vertex.get_longitude())
            edge_color = 0
            if (edge_obj.first_vertex, edge_obj.second_vertex) in self.edge_colors:
                edge_color = self.edge_colors[edge[0], edge[1]]
            elif (edge_obj.second_vertex, edge_obj.first_vertex) in self.edge_colors:
                edge_color = self.edge_colors[edge[1], edge[0]]
            new_graph.add_edge(first_vertex, second_vertex, weight=edge_obj.distance, color=edge_color)
            new_graph[first_vertex][second_vertex]['weight'] = edge_obj.distance

        return new_graph

    @staticmethod
    def networkx_convert(graph):
        """
        Converts a networkx digraph into a Graph Object
        :param graph: The NetworkX Digraph to be parsed
        :return: a Graph object
        """
        identifier = 0
        vertices = {}  # hash of positional vertex tuples to vertex objects
        edges = []
        for edge in graph.edges(data='SHAPE_LENG'):
            start_lat = edge[0][0]
            start_long = edge[0][1]
            pos_vert = (start_long, start_lat)
            start_vert = vertices[pos_vert]
            if pos_vert not in vertices:
                start_vert = Vertex(identifier, start_lat, start_long)
                vertices[pos_vert] = start_vert
                identifier += 1

            end_lat = edge[1][0]
            end_long = edge[1][1]
            pos_vert = (end_long, end_lat)
            end_vert = vertices[pos_vert]
            if pos_vert not in vertices:
                end_vert = Vertex(identifier, end_lat, end_long)
                vertices[pos_vert] = end_vert
                identifier += 1
            current_edge = Edge(start_vert, end_vert, edge[2])
            edges.append(current_edge)
        parsed_graph = Graph(edges)
        return parsed_graph

    @staticmethod
    def read_graph(file_name):
        """
        Reads in a graph stored in a .txt file with the name fileName
        :param file_name: the path to a .txt file
        :return: a Graph object
        """
        with open(file_name, 'r') as input_file:
            edges = []
            edge_flag = 0
            vertices = []  # ordered list of vertices
            correlations = None
            vertices_flag = 0
            corr_flag = 0
            for line in input_file:
                line = line.strip()

                if line == '':
                    continue

                if line == "VERTICES":
                    edge_flag = 0
                    vertices_flag = 1
                    continue

                if line == "EDGES":
                    edge_flag = 1
                    vertices_flag = 0
                    continue

                if line == "CORRELATIONS":
                    edge_flag = 0
                    vertices_flag = 0
                    corr_flag = 1
                    correlations = []

                if edge_flag == 1:
                    #  if we are in the edges block, read in the edges
                    parsed_line = tuple(map(int, line.split(",")))
                    num_data = len(parsed_line)
                    edge = Edge(vertices[parsed_line[0]], vertices[parsed_line[1]], parsed_line[2])
                    if num_data > 3:
                        edge.set_average_time(parsed_line[3])
                    if num_data > 4:
                        edge.set_standard_deviation_time(parsed_line[4])
                    if num_data > 5:
                        edge.set_speed_limit(parsed_line[5])
                    if num_data > 6:
                        edge.set_average_speed(parsed_line[6])
                    if num_data > 7:
                        edge.set_standard_deviation_speed(parsed_line[7])
                    edges.append(edge)

                if vertices_flag == 1:
                    #  if we are in the vertices block, read in the vertices
                    parsed_line = tuple(map(int, line.split(",")))
                    vertices.append(Vertex(parsed_line[0], parsed_line[1], parsed_line[2]))

                if corr_flag == 1:
                    #  if we are in the correlations block, read in the correlations
                    val = line.split(",")
                    val.remove(' ')
                    parsed_line = tuple(map(float, val))
                    correlations.append(parsed_line)

            return Graph(edges, correlations)

    def write_graph(self, file_name):
        """
        Writes a graph to a file, so that it can be retrieved later
        :param file_name: the name of the file to be written out
        :return: Null
        """
        with open(file_name, 'w+') as write_file:
            output_string = "VERTICES" + '\n'
            number_vertices = self.get_num_vertices()
            for i in range(number_vertices):
                current_vertex = self.vertices[i]
                output_string += str(current_vertex.get_identifier())
                output_string += ","
                output_string += str(current_vertex.get_latitude())
                output_string += ","
                output_string += str(current_vertex.get_longitude())
                output_string += '\n'
            output_string += '\n'
            output_string += '\n'
            output_string += "EDGES"
            output_string += '\n'
            out_edges = sorted(self.edges.values())
            for edge in out_edges:
                output_string += str(edge.first_vertex)
                output_string += ','
                output_string += str(edge.second_vertex)
                output_string += ','
                output_string += str(edge.weight)
                output_string += ','
                output_string += str(edge.speed_limit)
                output_string += ','
                output_string += str(edge.average_speed)
                output_string += ','
                output_string += str(edge.standard_deviation_speed)
                output_string += '\n'
            output_string += "CORRELATIONS"
            output_string += '\n'
            for edge_list in self.edge_correlation:
                for value in edge_list:
                    output_string += str(value)
                    output_string += ','
                output_string += '\n'
            write_file.write(output_string)

    def get_num_vertices(self):
        """
        Gets the number of vertices in the graph.
        Since the vertices are ordered by ID, taking the max works for this
        :return: an int, the number of vertices
        """
        return max(self.vertices.keys()) + 1


class Vertex:
    """
    Vertex object for use in the graph
    :field identifier: the identifier value, an int
    :field latitude: the first gps coordinate in the pair
    :field longitude: the second gps coordinate in the pair
    """
    identifier = 0  # basic initialization for id, should not be left at 0
    latitude = 0.0  # basic initialization for latitude, should not be left at 0.0
    longitude = 0.0  # basic initialization for longitude, should not be left at 0.0

    def __init__(self, identifier, latitude, longitude):
        """
        Constructor for a vertex
        :param identifier: the id for the vertex
        :param latitude: the latitude coordinate for the vertex
        :param longitude: the longitude coordinate for the vertex
        """
        self.identifier = identifier
        self.latitude = latitude
        self.longitude = longitude

    def __hash__(self):
        return hash((self.identifier, self.latitude, self.longitude))

    def __eq__(self, other):
        return (self.get_identifier() == other.get_identifier()) and \
               (self.get_latitude() == other.get_latitude()) and \
               (self.get_longitude() == other.get_longitude())

    def __repr__(self):
        return "{0}".format(str(self.identifier))

    def __str__(self):
        return str(self.identifier)

    def get_identifier(self):
        """
        Gets the id for the vertex
        :return: id
        """
        return self.identifier

    def get_latitude(self):
        """
        Gets the latitude value for the vertex
        :return: latitude
        """
        return self.latitude

    def get_longitude(self):
        """
        Gets the longitude value for the vertex
        :return: longitude
        """
        return self.longitude


edge_identifier_iterator = 0


class Edge:
    """
    Edge object for use in the Graph
    :field first_vertex: The first vertex of the edge, a vertex object
    :field second_vertex: The second vertex of the edge, a vertex object
    :field distance: the distance of the edge, an int/float
    :field speed_limit: the speed limit on this edge
    :field average_speed: the average speed of traffic across this edge
    :field standard_deviation_speed: the standard deviation of speeds across this edge
    """
    identifier = None
    first_vertex = None
    second_vertex = None
    distance = None
    average_time = None
    standard_deviation_time = None
    speed_limit = None
    average_speed = None
    standard_deviation_speed = None

    def __init__(self, first_vertex, second_vertex, distance, average_time=None, standard_deviation_time=None,
                 speed_limit=None, average_speed=None, standard_deviation_speed=None):
        """
        Constructor for the edge class
        :param first_vertex: The first vertex of the edge, a vertex object
        :param second_vertex: The second vertex of the edge, a vertex object
        :param distance: the distance of the edge, an int/float
        :param average_time: the average total time to travel across this edge
        :param standard_deviation_time: the standard deviation of travel time across this edge
        :param speed_limit: the speed limit on this edge
        :param average_speed: the average speed of traffic across this edge
        :param standard_deviation_speed: the standard deviation of speeds across this edge
        """
        global edge_identifier_iterator
        self.identifier = edge_identifier_iterator
        edge_identifier_iterator += 1
        self.first_vertex = first_vertex
        self.second_vertex = second_vertex
        self.distance = distance
        self.average_time = average_time
        self.standard_deviation_time = standard_deviation_time
        self.speed_limit = speed_limit
        self.average_speed = average_speed
        self.standard_deviation_speed = standard_deviation_speed

    def __repr__(self):
        return "{0} -> {1} @ {2}".format(str(self.first_vertex), str(self.second_vertex), str(self.speed_limit))

    def __cmp__(self, other):
        if self.identifier < other.id:
            return -1
        if self.identifier == other.id:
            return 0
        if self.identifier > other.id:
            return 1

    def get_identifier(self):
        return self.identifier

    def get_first_vertex(self):
        return self.first_vertex

    def get_second_vertex(self):
        return self.second_vertex

    def get_distance(self):
        return self.distance

    def get_average_time(self):
        return self.average_time

    def get_standard_deviation_time(self):
        return self.standard_deviation_time

    def get_speed_limit(self):
        return self.speed_limit

    def get_average_speed(self):
        return self.average_speed

    def get_standard_deviation_speed(self):
        return self.standard_deviation_speed

    def set_distance(self, d):
        self.distance = d

    def set_average_time(self, avg_time):
        self.average_time = avg_time

    def set_standard_deviation_time(self, std_dev_time):
        self.standard_deviation_time = std_dev_time

    def set_speed_limit(self, spd_limit):
        self.speed_limit = spd_limit

    def set_average_speed(self, avg_spd):
        self.average_speed = avg_spd

    def set_standard_deviation_speed(self, std_dev_spd):
        self.standard_deviation_speed = std_dev_spd
