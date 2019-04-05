# Generates and displays a networkx graph to an html file
# Based off of code found here: https://plot.ly/python/network-graphs/

import plotly
import plotly.graph_objs as go
import networkx as nx
from sys import maxsize


def generate_graph(graph):
    g = nx.Graph()
    pos = {}
    min_latitude = maxsize
    min_longitude = maxsize
    n = graph.get_num_vertices()
    for vertex in graph.vertices:
        vertex_object = graph.vertices[vertex]
        if vertex_object.get_latitude() < min_latitude:
            min_latitude = vertex_object.get_latitude()
        if vertex_object.get_longitude() < min_longitude:
            min_longitude = vertex_object.get_longitude()
    for vertex in graph.vertices:
        vertex_object = graph.vertices[vertex]
        g.add_node(vertex_object.get_identifier())
        pos[vertex_object.get_identifier()] = [(vertex_object.get_longitude() - min_longitude) / n,
                                               (vertex_object.get_latitude() - min_latitude) / n]
    for edge in graph.edges:
        g.add_edge(edge[0].get_identifier(), edge[1].get_identifier())
    nx.set_node_attributes(g, pos, 'pos')
    return g


def get_color(key):
    """
    gets the color for a node based on its integer value representation
    :param key: an integer value
    :return: (r,g,b), where r,g,b are ints between 0 and 256
    """
    r = (key & 0xFF0000) >> 16
    g = (key & 0x00FF00) >> 8
    b = (key & 0x0000FF)
    return r, g, b


def draw_graph(graph, title, filename):
    # g = generate_graph(graph)
    g = graph
    # print(g.edges)
    pos = nx.get_node_attributes(g, 'pos')
    dmin = 1
    # ncenter = 0
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5) ** 2 + (y - 0.5) ** 2
        if d < dmin:
            # ncenter = n
            dmin = d

    # p = nx.single_source_shortest_path_length(g, ncenter)

    edge_trace = []

    for edge in g.edges(data=True):
        x0, y0 = edge[0]
        x1, y1 = edge[1]
        jam_or_path = edge[2].get('color')
        # No Jam, no path
        color = 'black'
        # If an edge is jammed it is colored red
        if jam_or_path == 1:
            color = 'red'
        # Path 1, 2, 3, 4 all have different colored edges
        elif jam_or_path == 2:
            color = 'green'
        elif jam_or_path == 3:
            color = 'blue'
        elif jam_or_path == 4:
            color = 'yellow'
        elif jam_or_path == 5:
            color = 'purple'
        weight = "Edge Weight: " + str(edge[2].get('weight'))
        edge_trace.append(go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode='lines',
            text=weight,
            hoverinfo='text',
            line=dict(width=5, color=color)))
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # Color scale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis'
            colorscale='Jet',
            reversescale=True,
            color=[],
            size=20,
            colorbar=dict(
                thickness=15,
                title='Discover Time',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in g.nodes():
        # x, y = g.node[node]['pos']
        x, y = node
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    node_hash = {}
    max_node = 0
    done = set()
    for node, adjacencies in enumerate(g.adjacency()):
        node_info = "Node "
        n = adjacencies[0]
        identifier = ""
        if n in node_hash:
            identifier = node_hash[n]
        else:
            node_hash[n] = max_node
            identifier = max_node
            max_node += 1

        if identifier in done:
            print("NEW NODE, SAME GPS", identifier)
        else:
            done.add(identifier)
        node_info += str(identifier)
        node_info += ": connected to "
        for item in adjacencies[1]:
            node_number = ""
            if item in node_hash:
                node_number = node_hash[item]
            else:
                node_hash[item] = max_node
                node_number = max_node
                max_node += 1
            node_info += str(node_number)
            node_info += ", "
        node_info = node_info[:-2]
        # change color stuff
        node_trace['marker']['color'] += tuple([g.nodes[n]['color']])
        #  node_info = '# of connections: ' + str(len(adjacencies[1]))
        node_trace['text'] += tuple([node_info])

    trace = edge_trace
    trace.append(node_trace)
    fig = go.Figure(data=trace,
                    layout=go.Layout(
                        title="<br>"+title,
                        titlefont=dict(size=16),
                        showlegend=False,
                        hovermode='closest',
                        hoverdistance=50,
                        margin=dict(b=5, l=5, r=5, t=5),
                        annotations=[dict(
                            text="Created by Michael Bolot, Jack Baumann, and Dr. David Andrews using "
                                 "<a href='https://plot.ly/python/network-graphs/'>plotly.networkx</a>.",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    plotly.offline.plot(fig, filename='./graph_displays/generated/'+filename+'.html')
