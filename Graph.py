

'''
Created By Michael Bolot and John (Jack) Baumann for 2018 research
'''


class Graph:
    '''
    Graph Class
    :field verticies: A list of verticies contained by the graph
    :field edges: A dictionary of the edges. Key is a tuple of (src, dest) and value is distance, an int
    :field connections: a dictionary of edges. Key is source, value is destination
    :field seen: a set of seen verticies
    '''
    verticies = []  # list of verticies contained by the graph
    edges = {}  # dictionary of edges in the graph. Key is a tuple of (src,dest) and value is distance, an int
    connections = {}  # dictionary of edges. Key is src, value is dest
    seen = set()

    def __init__(self, edges):
        '''
        Constructor for the Graph Class
        :param edges: A list of edges in the graph
        :return void
        '''
        verticies = set()
        connections = {}
        self.edges = edges
        for edge in edges:
            if edge[0] not in verticies:
                verticies.add(edge[0])
            if edge[1] not in verticies:
                verticies.add(edge[1])

            if edge[0] not in connections:
                connections[edge[0]] = [edge[1]]
            else:
                connections[edge[0]].append(edge[1])
            if edge[1] not in connections:
                connections[edge[1]] = [edge[0]]
            else:
                connections[edge[1]].append(edge[0])

        self.verticies = list(verticies)
        self.connections = connections

    def connnected(self, src, dest):
        '''
        Checks if two verticies are immediately connected in the graph
        :param src: the source vertex
        :param dest: the destination vertex
        :return: boolean connected
        '''
        if dest in self.connections[src]:
            return True
        return False

    def distance(self, src, dest):
        '''
        Finds the distance between two connected verticies
        :param src: the source vertex
        :param dest: the destination vertex
        :return: int dist, which is non-zero unless src == dest or connected(src,dest) == False
        '''
        if not self.connected(src, dest):
            return 0
        else:
            return self.edges[(src, dest)]

