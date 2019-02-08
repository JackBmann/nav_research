"""
Created by Michael Bolot and John (Jack) Baumann for 2018 research
Designed to house the search algorithms to be used on the graph
"""
from queue import PriorityQueue
from sys import maxsize
from math import sqrt


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
        distance += graph.edges[(path[current], path[current-1])].weight
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
    Searches for a path from src to dest, using a naive depth first search
    :param graph: The graph object, with specifications of Graph.py
    :param src: The source vertex to search from
    :param dest: The destination vertex to find
    :return: best_path, a path from src to dest (list of vertices, in order of route)
    """
    best_path = []
    best_path_length = maxsize
    graph.add_seen(src)
    if src not in graph.connections:
        return []
    for connection in graph.connections[src]:
        path = []
        if connection == dest:
            graph.add_seen(connection)
            path.append(connection)
            path.append(src)
            return path
        else:
            if connection in graph.seen:
                print(src, connection)
                continue
            #graph.add_seen(connection)
            path = dfs(graph, connection, dest)
            if not path:
                continue
            path.append(src)
            p_dist = path_distance(graph, path)
            if p_dist <= best_path_length:
                best_path = path
                best_path_length = p_dist
    return best_path


def dijkstra(graph, src, dest, heuristic):
    """
    :param graph: graph that will be used to find optimal path
    :param src: the source vertex to search from
    :param dest: the destination vertex to search to
    :param heuristic: the heuristic function used as a weight. Returns 0 for djikstra's, and non-zero for a*
    :return: a list which is the optimal path
    """
    distance = {}  # the distance value of each vertex
    parents = {}  # the parent of each vertex, with respect to optimal path
    q = PriorityQueue()
    for vertex in graph.vertices:
        added_vertex = graph.vertices[vertex]
        if added_vertex == src:
            distance[added_vertex] = 0
            q.put((0, vertex))
            continue
        distance[added_vertex] = maxsize
        parents[added_vertex] = None

    while not q.empty():
        current_vertex = graph.vertices[q.get()[1]]
        if current_vertex == dest:
            return reconstruct_path(parents, src, dest)
        if current_vertex not in graph.connections:
            continue
        if current_vertex not in graph.seen:
            graph.add_seen(current_vertex)
        for connection in graph.connections[current_vertex]:
            best_move = distance[current_vertex] + heuristic(graph, current_vertex, connection)
            if best_move < distance[connection]:
                distance[connection] = best_move
                parents[connection] = current_vertex
                q.put((best_move, connection.get_identifier()))


def djikstra_heuristic(graph, src, dest):
    """
    Heuristic for djikstra's, just returns the edge between src and dest
    :param graph: the graph
    :param src: source vertex
    :param dest: dest vertex
    :return: the edge weight between src and dest, a number (float)
    """
    return graph.edges[(src, dest)].weight


def a_star_heuristic(graph, src, dest):
    """
    Heuristic function for a*
    Currently just calculates the euclidean distance between src and dest to inform its decision
    :param graph: The graph for the function, not used
    :param src: the source vertex (a vertex object)
    :param dest: the destination vertex (a vertex object)
    :return: distance, a number (float) value that represents the distance between src and dest
    """
    distance = sqrt((src.get_latitude() - dest.get_latitude())**2 + (src.get_longitude() - dest.get_longitude())**2)
    return distance + graph.edges[(src, dest)].weight


if __name__ == "__main__":
    # do some testing here
    print("Hello")
