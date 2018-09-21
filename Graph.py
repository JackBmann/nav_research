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
    vertices = []  # list of vertices contained by the graph
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
        vertices = set()
        connections = {}
        self.edges = edges
        for edge in edges:
            if edge[0] not in vertices:
                vertices.add(edge[0])
            if edge[1] not in vertices:
                vertices.add(edge[1])

            if edge[0] not in connections:
                connections[edge[0]] = [edge[1]]
            else:
                connections[edge[0]].append(edge[1])
            #if edge[1] not in connections:
            #    connections[edge[1]] = [edge[0]]
            #else:
            #    connections[edge[1]].append(edge[0])

        self.vertices = list(vertices)
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
