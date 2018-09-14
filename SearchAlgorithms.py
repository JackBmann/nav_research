"""
Created by Michael Bolot and John (Jack) Baumann for 2018 research
Designed to house the search algorithms to be used on the graph
"""

from Graph import Graph
from sys import maxsize


def path_distance(graph, path):
    """
    Finds the distance of a path
    :param graph: the graph the path is on
    :param path: the path whose distance is to be evaluated
    :return: distance, an int/float whose value represents the distance from the start of the path to the end of the path
    """
    distance = 0
    current = 0
    while current != len(path)-1:
        distance += graph.edges((path[current], path[current + 1]))
        current += 1
    return distance


def bfs(graph, src, dest):
    """
    Searches for a path from src to dest, using a naive breadth first search
    :param graph: The graph object, with specifications of Graph.py
    :param src: The source vertex to search from
    :param dest: The destination vertex to find
    :return: best_path, a path from src to dest (list of vertices, in order of route)
    """
    best_path = []
    best_path_length = maxsize
    for connection in graph.connections[src]:
        path = []
        if connection == dest:
            path.append(connection)
            return path
        else:
            if connection in Graph.seen:
                return []
            Graph.seen.add(connection)
            path = bfs(graph, connection, dest)
            if path == []:
                continue
            pDistance = path_distance(graph, path)
            if pDistance < best_path_length:
                path.append(connection)
                best_path = path
                best_path_length = pDistance
    return best_path


def a_star(graph, src, dest):
    """
    Searches for a path from src to dest
    :param graph: the graph object, with specifications of Graph.py
    :param src: the source vertex to search from
    :param dest: The destination vertex to find
    :return: path, a path from src to dest (list of vertices, in order of route)
    """
    path = []

    return path


if __name__ == "__main__":
    # do some testing here
    print("Hello")
