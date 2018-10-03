"""
Created By Michael Bolot and John (Jack) Baumann for 2018 research
"""


class Graph:
    """
    Graph Class
    :field vertices: A list of vertices contained by the graph (uses vertex objects)
    :field edges: A dictionary of the edges. Key is a tuple of (src, dest) and value is distance, an int
    :field connections: a dictionary of edges. Key is source, value is destination
    :field seen: a set of seen vertices
    """
    vertices = {}  # list of vertices contained by the graph
    edges = {}  # dictionary of edges in the graph. Key is a tuple of (src,dest) and value is distance, an int
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
            first_vertex = edge[0]
            second_vertex = edge[1]

            if first_vertex.getID() not in vertices:
                vertices[first_vertex.getID()] = first_vertex
            else:
                first_vertex = vertices[first_vertex.getID()]

            if second_vertex.getID() not in vertices:
                vertices[second_vertex.getID()] = second_vertex
            else:
                second_vertex = vertices[second_vertex.getID()]

            if first_vertex not in connections:
                connections[first_vertex] = [second_vertex]
            else:
                connections[first_vertex].append(second_vertex)

            parsed_edges[(first_vertex, second_vertex)] = edges[edge]
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
        :return: int dist, which is non-zero unless src == dest or connected(src,dest) == False
        """
        if not self.connected(src, dest):
            return 0
        else:
            return self.edges[(src, dest)]


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
        return "{0} @ 0x{1}".format(str(self.identifier), str(hex(identifier(self))).upper())

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

    def __init___(self, first_vertex, second_vertex, weight):
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

