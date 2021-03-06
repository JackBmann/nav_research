"""
Created by Michael Bolot and John (Jack) Baumann for 2018-19 research
Houses the search algorithms and heuristic functions to be run on a graph
"""
from queue import PriorityQueue
from sys import maxsize
from math import sqrt
from scipy.stats import norm


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
        distance += graph.edges[(path[current], path[current-1])].get_distance()
        current -= 1
    return distance


def reconstruct_path(parents, src, dest):
    """
    Helper function to reconstruct the path from dest to source
    :param parents: A dictionary of a vertex mapped to its optimal parent node
    :param src: the source vertex for the path
    :param dest: the destination vertex for the path
    :return: path, a list of the vertices in order
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
                continue
            graph.add_seen(connection)
            path = dfs(graph, connection, dest)
            if not path:
                continue
            path.append(src)
            p_dist = path_distance(graph, path)
            if p_dist <= best_path_length:
                best_path = path
                best_path_length = p_dist
    return best_path


def dijkstra(graph, src, dest, heuristic, deadline=None):
    """
    :param graph: graph that will be used to find optimal path
    :param src: the source vertex to search from
    :param dest: the destination vertex to search to
    :param heuristic: the heuristic function used as a weight. Returns 0 for Djikstra's, and non-zero for a*
    :param deadline: the target deadline value used in heuristic functions
    :return: a list which is the optimal path
    """
    distance = {}  # the distance value of each vertex
    parents = {}  # the parent of each vertex, with respect to optimal path
    q = PriorityQueue()
    graph.set_deadline(deadline)
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
            best_move = distance[current_vertex] + heuristic(graph, current_vertex, connection, parents)
            if best_move < distance[connection]:
                distance[connection] = best_move
                parents[connection] = current_vertex
                q.put((best_move, connection.get_identifier()))


def djikstra_heuristic(graph, src, dest, parents):
    """
    Heuristic for Djikstra's, just returns the distance between src and dest
    :param graph: the graph
    :param src: source vertex
    :param dest: dest vertex
    :param parents: unused for this function; included so that the more sophisticated heuristics can also be passed
    :return: the edge weight between src and dest, a number (float)
    """
    return graph.edges[(src, dest)].get_distance()


def a_star_heuristic(graph, src, dest, parents):
    """
    Heuristic function for A*
    Currently just calculates the euclidean distance between src and dest to inform its decision
    :param graph: The graph for the function, not used
    :param src: the source vertex (a vertex object)
    :param dest: the destination vertex (a vertex object)
    :param parents: unused for this function; included so that the more sophisticated heuristics can also be passed
    :return: distance, a number (float) value that represents the distance between src and dest
    """
    distance = sqrt((src.get_latitude() - dest.get_latitude())**2 + (src.get_longitude() - dest.get_longitude())**2)
    return distance


def mean_heuristic(graph, src, dest, parents):
    """
    Heuristic function that works off of the following methodology:
    If you are going close to the speed limit (based on mean speed), then find a correlated edge
    If you are not going close to the speed limit (based on mean speed), then find an uncorrelated edge
    :param graph: the graph for the function
    :param src: the src node (a vertex object)
    :param dest: the destination node (a vertex object)
    :param parents: the parents graph used to find the current edge that will be used for correlation matching
    :return: distance, a number (float) value that represents the distance between src and dest
    """
    current_weight = graph.edges[(src, dest)].get_distance()  # the current weight with no modification
    SPEED_THRESH = 0.15
    distance = 0
    if src not in parents:
        # if this is the first edge in the path, don't bother with correlations
        distance = current_weight
        return distance
    current_edge = graph.edges[(parents[src], src)]
    next_edge = graph.edges[(src, dest)]
    average = current_edge.average_speed
    speed_limit = current_edge.speed_limit
    if average is None or speed_limit is None:
        distance = current_weight
        return distance
    if average/speed_limit < SPEED_THRESH:
        '''
        if we are going fast, we want to stay on a similarly correlated edge
        the correlation is inverted because we want a lower weight for more correlated edges
        so an edge with a weight 10 correlated with previous edge at .9 would result in weight 1 with inversion
        without inversion, it would be at 9, which is potentially unfavorable
        '''
        distance = current_weight * (1 - graph.edge_correlation[current_edge.identifier][next_edge.identifier])
    else:
        distance = current_weight * (graph.edge_correlation[current_edge.identifier][next_edge.identifier])

    return distance


def deviation_heuristic(graph, src, dest, parents):
    """
    Heuristic functionality based on the std deviation and the mean (speed on both accounts)
    Functions similarly to the mean heuristic until the end, where it looks at std_deviation
    :param graph: the graph for the function
    :param src: the src node (a vertex obj)
    :param dest: the dest node (a vertex obj)
    :param parents: the parents graph used to find the current edge that will be used for correlation matching
    :return: distance, a number (float) that represents the distance between src and dest
    """
    current_weight = graph.edges[(src, dest)].get_distance()  # the current weight with no modification
    # arbitrarily defined constants
    SPEED_THRESH = 0.15
    DEV_THRESH = 0.05
    REDUCE = 0.7

    distance = 0
    if src not in parents:
        # if this is the first edge in the path, don't bother with correlations
        distance = current_weight
        return distance
    current_edge = graph.edges[(parents[src], src)]
    next_edge = graph.edges[(src, dest)]
    average = current_edge.average_speed
    speed_limit = current_edge.speed_limit

    if average is None or speed_limit is None:
        distance = current_weight
        return distance

    if average / speed_limit < SPEED_THRESH:
        '''
        if we are going fast, we want to stay on a similarly correlated edge
        the correlation is inverted because we want a lower weight for more correlated edges
        so an edge with a weight 10 correlated with previous edge at .9 would result in weight 1 with inversion
        without inversion, it would be at 9, which is potentially unfavorable
        '''
        distance = current_weight * (1 - graph.edge_correlation[current_edge.identifier][next_edge.identifier])
        # In addition, if this next edge has a good standard deviation, reduce the weight further
        if current_edge.standard_deviation_speed < DEV_THRESH*average:
            distance *= REDUCE

    else:
        distance = current_weight * (graph.edge_correlation[current_edge.identifier][next_edge.identifier])
        # In addition, if this next edge has a good standard deviation, reduce the weight further
        if current_edge.standard_deviation_speed < DEV_THRESH * average:
            distance *= REDUCE
    return distance


def single_traffic_heuristic(graph, src, dest, parents):
    """
    A heuristic for just using traffic jams, correlations, and times to calculate a path
    :param graph: the input graph
    :param src: the source node
    :param dest: the destination node
    :param parents: the parents hash, unused
    :return: distance, an int/float detailing the weight of the evaluated edge
    """
    distance = 0
    true_edge = graph.edges[(src, dest)]
    max_corr = 0
    for jam in graph.jams:
        # for each jam, see the correlation between the jammed edge and the evaluated edge
        # looking for the maximum jam
        jam_corr = graph.edge_correlation[true_edge.identifier][jam.identifier]
        if jam_corr > max_corr:
            max_corr = jam_corr
    current_weight = true_edge.average_time
    distance = (current_weight * max_corr) + current_weight
    return distance


def normal_dist_traffic(graph, src, dest, parents):
    """
    Heuristic that uses a normal distribution to determine the probability that a route will take you to a
    given destination in the time allotted (business logic overview)
    :param graph: the graph to be used by the algorithm
    :param src: the source node for the newly evaluated edge
    :param dest: the destination node for the newly evaluated edge
    :param parents: the parents graph which allows the route's normal distribution to be created
    :return: total_weight a numerical (int/double) value representing the weight of the newly evaluated edge
    """
    current = None
    # if we have no parents, then just proceed as normal
    if src in parents:
        current = parents[src]
    else:
        return graph.edges[(src, dest)].get_average_time()
    path = [src]
    while current:
        path.append(current)
        if current in parents:
            current = parents[current]
        else:
            current = None

    path = path[::-1]   # reverse the path for ease of traversal
    normal_mean = 0
    normal_var = 0
    edges = []
    for i in range(1, len(path)):
        edge = graph.edges[(path[i-1], path[i])]
        normal_mean += edge.average_time
        edges.append(edge)
    for i in range(len(edges)):
        start_edge = edges[i]
        normal_var += (start_edge.standard_deviation_time ** 2)
        for j in range(i, len(edges)):
            end_edge = edges[j]
            normal_var += (2 * start_edge.standard_deviation_time * end_edge.standard_deviation_time *
                           graph.edge_correlation[start_edge.identifier][end_edge.identifier])
    normal_var = sqrt(normal_var)

    # Get the probability that this route meets the deadline using the probability density function (PDF) of the
    # normal distribution of normal_mean and normal_var
    p = norm(loc=normal_mean, scale=normal_var).pdf(graph.deadline)
    # total_weight = graph.edges[(src, dest)].get_average_time()
    # total_weight += total_weight * (1-p)
    total_weight = 1 - p
    return total_weight
