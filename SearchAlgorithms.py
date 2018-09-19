"""
Created by Michael Bolot and John (Jack) Baumann for 2018 research
Designed to house the search algorithms to be used on the graph
"""
from queue import PriorityQueue
from sys import maxsize


def path_distance(graph, path):
    """
    Finds the distance of a path
    :param graph: the graph the path is on
    :param path: the path whose distance is to be evaluated
    :return: distance, an int/float whose value represents the distance
             from the start of the path to the end of the path
    """
    distance = 0
    current = len(path)-1
    while current != 0:
        distance += graph.edges[(path[current], path[current-1])]
        current -= 1
    return distance

def reconstruct_path(parents, src, dest):
    """
    Helper function to reconstruct the path from dest to source
    :param parents: A dictionary of a vertex mapped to its optimal parent node
    :param src: the source vertex for the path
    :param dest: the destination vertex for the path
    :return: path, a list of the verticies in order
    """
    path = []
    added = dest
    while added != src:
        path.append(added)
        added = parents[added]
    path.append(added)
    return path

def dfs(graph, src, dest):
    """
    Searches for a path from src to dest, using a naive breadth first search
    :param graph: The graph object, with specifications of Graph.py
    :param src: The source vertex to search from
    :param dest: The destination vertex to find
    :return: best_path, a path from src to dest (list of vertices, in order of route)
    """
    best_path = []
    best_path_length = maxsize
    graph.seen.add(src)
    if src not in graph.connections:
        return []
    for connection in graph.connections[src]:
        path = []
        if connection == dest:
            path.append(connection)
            path.append(src)
            return path
        else:
            if connection in graph.seen:
                continue
            graph.seen.add(connection)
            path = dfs(graph, connection, dest)
            if not path:
                continue
            p_dist = path_distance(graph, path)
            if p_dist < best_path_length:
                path.append(src)
                best_path = path
                best_path_length = p_dist
    return best_path


def dijkstra(graph, src, dest):
    """
    :param graph: graph that will be used to find optimal path
    :return: a list which is the optimal path
    :param src: the source vertex to search from
    :param dest: the destination vertex to search to
    """
    distance = {}  # the distance value of each vertex
    parents = {}  # the parent of each vertex, with respect to optimal path
    q = PriorityQueue()
    for vertex in graph.vertices:
        if vertex == src:
            distance[vertex] = 0
            q.put((0, src))
            continue
        distance[vertex] = maxsize
        parents[vertex] = None
        q.put((maxsize, vertex))

    while not q.empty():
        current_vertex = q.get()[1]
        if current_vertex == dest:
            return reconstruct_path(parents, src, dest)
        if current_vertex not in graph.connections:
            continue
        for connection in graph.connections[current_vertex]:
            best_move = distance[current_vertex] + graph.edges[(current_vertex, connection)]
            if best_move < distance[connection]:
                distance[connection] = best_move
                parents[connection] = current_vertex


def a_star(graph, src, dest):
    """
    Searches for a path from src to dest
    :param graph: the graph object, with specifications of Graph.py
    :param src: the source vertex to search from
    :param dest: The destination vertex to find
    :return: path, a path from src to dest (list of vertices, in order of route)
    """
    path = []
    Q = PriorityQueue
    distance = {}
    parents = {}
    for vertex in graph.vertices:
        if vertex == src:
            distance[vertex] = 0
            continue
        distance[vertex] = maxsize
        Q.put((distance[vertex], vertex))
        parents[vertex] = None

    while not Q.empty():
        current_vertex = Q.get()[1]
        if current_vertex == dest:
            return reconstruct_path(parents, src, dest)
        path.append(current_vertex)
        for connection in graph.connections[current_vertex]:
            if connection in path:
                continue
            path.append(connection)
            best_move = graph.edges([(current_vertex, connection)]) + distance[current_vertex]
            if best_move >= distance[connection]:
                continue
            distance[connection] = best_move
            parents[connection] = current_vertex

    return path


if __name__ == "__main__":
    # do some testing here
    print("Hello")
