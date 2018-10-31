"""
Created By Michael Bolot and John (Jack) Baumann for 2018 research
"""
import networkx

class Graph:
    """
    Graph Class
    :field vertices: A list of vertices contained by the graph (uses vertex objects)
    :field edges: A dictionary of the edges. Key is a tuple of (src, dest) and value is distance, an int
    :field connections: a dictionary of edges. Key is source, value is destination
    :field seen: a set of seen vertices
    """
    vertices = {}  # list of vertices contained by the graph
    edges = {}  # dictionary of edges in the graph. Key is a tuple of (src,dest) and value is an edge object
    connections = {}  # dictionary of edges. Key is src, value is dest
    seen = set()

    def __init__(self, edges):
        """
        Constructor for the Graph Class
        Currently are bidrectional paths
        :param edges: A list of edges in the graph
        :return void
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

    def convert_networkx(self):
        """
        Converts a graph into a networkx graph
        :return: A networkx graph object
        """
        newGraph = networkx.DiGraph()
        for vertex in self.vertices:
            vertex_obj = self.vertices[vertex]
            newGraph.add_node((vertex_obj.get_latitude(), vertex_obj.get_longitude()))
        for edge in self.edges:
            edge_obj = self.edges[edge]
            first_vertex = (edge_obj.first_vertex.get_latitude(), edge_obj.first_vertex.get_longitude())
            second_vertex = (edge_obj.second_vertex.get_latitude(), edge_obj.second_vertex.get_longitude())
            newGraph.add_edge(first_vertex, second_vertex)
            newGraph[first_vertex][second_vertex]['weight'] = edge_obj.weight
        return newGraph

    @staticmethod
    def networkx_convert(graph):
        """
        Converts a networkx digraph into a Graph Object
        :param graph: The NetworkX Digraph to be parsed
        :return: a Graph obejct
        """
        identifier = 0
        vertices = {}  # hash of positional vertex tuples to vertex objects
        edges = []
        for edge in graph.edges(data='SHAPE_LENG'):
            start_lat = edge[0][0]
            start_long = edge[0][1]
            pos_vert = (start_long, start_lat)
            start_vert = ""
            if pos_vert in vertices:
                start_vert = vertices[pos_vert]
            else:
                start_vert = Vertex(identifier, start_lat, start_long)
                vertices[pos_vert] = start_vert
                identifier += 1

            end_long = edge[1][0]
            end_lat = edge[1][1]
            pos_vert = (end_long, end_lat)
            end_vert = ""
            if pos_vert in vertices:
                end_vert = vertices[pos_vert]
            else:
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
    :field id: the identifier value, an int
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
        return "{0} @ 0x{1}".format(str(self.identifier), str(hex(self.identifier)).upper())

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


class Edge:
    """
    Edge object for use in the Graph
    :field first_vertex: The first vertex of the edge, a vertex object
    :field second_vertex: The second vertex of the edge, a vertex object
    :field weight: the weight of the edge, an int/float
    """
    first_vertex = None
    second_vertex = None
    weight = None

    def __init__(self, first_vertex, second_vertex, weight):
        """
        Constructor for the edge class
        :param first_vertex: The first vertex of the edge, a vertex object
        :param second_vertex: The second vertex of the edge, a vertex object
        :param weight: the weight of the edge, an int/float
        :return: nothing, because its a constructor
        """
        self.first_vertex = first_vertex
        self.second_vertex = second_vertex
        self.weight = weight
