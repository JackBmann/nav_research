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
    vertices = {} # list of vertices contained by the graph
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
            first_vertex = Vertex(edge[0], 0, 0)
            second_vertex = Vertex(edge[1], 0, 0)

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

    def getVertex(self, vertex_id):
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
    :field x: the first gps coordinate in the pair
    :field y: the second gps coordinate in the pair
    """
    id = 0  # basic initialization for id, should not be left at 0
    x = 0.0  # basic initialization for x, should not be left at 0.0
    y = 0.0  # basic initialization for y, should not be left at 0.0

    def __init__(self, id, x, y):
        """
        Constructor for a vertex
        :param id: the id for the vertex
        :param x: the x coordinate for the vertex
        :param y: the y coordinate for the vertex
        """
        self.id = id
        self.x = x
        self.y = y

    def getID(self):
        """
        Gets the id for the vertex
        :return: id
        """
        return self.id

    def getX(self):
        """
        Gets the x value for the vertex
        :return: x
        """
        return self.x

    def getY(self):
        """
        Gets the y value for the vertex
        :return: y
        """
        return self.y
