"""
Created By Michael Bolot and John (Jack) Baumann for Fall 2018 - Spring 2019 research
"""
import networkx
from sys import maxsize


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
    optimal_color = 0  # 0 means the edge is on an optimal path, one means it is not
    edge_correlation = []

    def __init__(self, edges):
        """
        Constructor for the Graph Class
        Currently are bidirectional paths
        :param edges: A list of edges in the graph
        """
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
        self.edge_correlation = [[None] * len(self.edges)] * len(self.edges)  # first fill in the array for the entries
        # we will arbitrarily fill in the list, so it is necessary to have a properly filled array
        self.create_correlations()

    def edge_distance(self, source_edge, dest_edge, scanned):
        """
        gives the distance between two edges
        :param source_edge: the source edge
        :param dest_edge: the destination edge
        :param scanned: a dict of things already scanned
        :return: dist, an int representing the distance between the two edges, or none
        """
        dist = None
        if source_edge.second_vertex == dest_edge.first_vertex:
            dist = 1
            scanned[(source_edge, dest_edge)] = 1
            scanned[(dest_edge, source_edge)] = 1
        else:
            best = maxsize
            for end_point in self.connections[source_edge.second_vertex]:
                new_edge = self.edges[(end_point, source_edge.second_vertex)]
                if (new_edge, dest_edge) in scanned:
                    if scanned[(new_edge, dest_edge)] < best:
                        best = scanned[(new_edge, dest_edge)] + 1
                dist = self.edge_distance(new_edge, dest_edge, scanned)
                if dist:
                    dist += 1
                    if dist < best:
                        best = dist
            for start_point in self.connections[source_edge.first_vertex]:
                new_edge = self.edges[(start_point, source_edge.first_vertex)]
                if (new_edge, dest_edge) in scanned:
                    if scanned[(new_edge, dest_edge)] < best:
                        best = scanned[(new_edge, dest_edge)] + 1
                dist = self.edge_distance(new_edge, dest_edge, scanned)
                if dist:
                    dist += 1
                    if dist < best:
                        best = dist
            if best != maxsize:
                dist = best
        scanned[(source_edge, dest_edge)] = dist
        scanned[(dest_edge, source_edge)] = dist

        return dist

    def create_correlations(self):
        """
        Spreads the correlations out through the whole graph
        Currently very slow, distances are being re-calculated
        Can be solved by passing in a dict in this function
        :return: None
        """
        scanned = {}
        for edge in self.edges:
            for other_edge in self.edges:
                if (edge, other_edge) in scanned:
                    distance = scanned[(edge, other_edge)]
                    corr = 1 - (distance * 0.1)
                    if corr < 0.09:
                        corr = 0
                    self.edge_correlation[edge.get_id()][other_edge.get_id()] = corr

                if edge == other_edge:
                    continue

                distance = self.edge_distance(edge, other_edge, scanned)
                corr = 1 - (distance * 0.1)
                self.edge_correlation[edge.get_id()][other_edge.get_id()] = corr

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

    def color_graph(self, path):
        """
        Colors a graph's edges and vertices
        :param path: the optimal path to be highlighted in the display
        :return: void, all changes will be made to structures in the graph object
        """
        self.node_colors = self.seen  # seen already contains information that can be used to color the nodes
        if len(path) < 2:
            # if the path doesn't have at least 2 nodes, it is maleformed
            return
        current_edge = (path[0], path[1])
        self.edge_colors[current_edge] = self.optimal_color
        for i in range(2, len(path)):
            current_edge = (current_edge[1], path[i])
            self.edge_colors[current_edge] = self.optimal_color

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
            if self.edges[edge].get_speed_limit() > 0:
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
            edge_color = 1
            if (edge_obj.first_vertex, edge_obj.second_vertex) in self.edge_colors or \
                    (edge_obj.second_vertex, edge_obj.first_vertex) in self.edge_colors:
                edge_color = 0
            new_graph.add_edge(first_vertex, second_vertex, weight=edge_obj.weight, color=edge_color)
            new_graph[first_vertex][second_vertex]['weight'] = edge_obj.weight

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
            vertices_flag = 0
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

                if edge_flag == 1:
                    #  if we are in the edges block, read in the edges
                    parsed_line = tuple(map(int, line.split(",")))
                    edges.append(Edge(vertices[parsed_line[0]], vertices[parsed_line[1]], parsed_line[2]))

                if vertices_flag == 1:
                    #  if we are in the vertices block, read in the vertices
                    parsed_line = tuple(map(int, line.split(",")))
                    vertices.append(Vertex(parsed_line[0], parsed_line[1], parsed_line[2]))

            return Graph(edges)

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
            for pair in self.edges:
                edge = self.edges[pair]
                output_string += str(edge.first_vertex)
                output_string += ','
                output_string += str(edge.second_vertex)
                output_string += ','
                output_string += str(edge.weight)
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
    edge_identifier_iterator = 0  # basic initialization for id, should not be left at 0
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
    :field weight: the weight of the edge, an int/float
    :field speed_limit: the speed limit on this edge
    :field average_speed: the average speed of traffic across this edge
    :field standard_deviation_speed: the standard deviation of speeds across this edge
    """
    first_vertex = None
    second_vertex = None
    weight = None
    speed_limit = 0
    average_speed = 0
    standard_deviation_speed = 0
    id = None

    def __init__(self, first_vertex, second_vertex, weight, speed_limit=0, average_speed=0, standard_deviation_speed=0):
        """
        Constructor for the edge class
        :param first_vertex: The first vertex of the edge, a vertex object
        :param second_vertex: The second vertex of the edge, a vertex object
        :param weight: the weight of the edge, an int/float
        :param speed_limit: the speed limit on this edge
        :param average_speed: the average speed of traffic across this edge
        :param standard_deviation_speed: the standard deviation of speeds across this edge
        """
        global edge_identifier_iterator
        self.id = edge_identifier_iterator
        edge_identifier_iterator += 1
        self.first_vertex = first_vertex
        self.second_vertex = second_vertex
        self.weight = weight
        self.speed_limit = speed_limit
        self.average_speed = average_speed
        self.standard_deviation_speed = standard_deviation_speed

    def __repr__(self):
        return "{0} -> {1} @ {2}".format(str(self.first_vertex), str(self.second_vertex), str(self.speed_limit))

    def get_id(self):
        return self.id

    def get_speed_limit(self):
        return self.speed_limit

    def get_average_speed(self):
        return self.average_speed

    def get_standard_deviation_speed(self):
        return self.standard_deviation_speed

