"""
Generates and displays a networkx graph to an html file using plotly
Based off of code found here: https://plot.ly/python/network-graphs/
"""
import plotly
import plotly.graph_objs as go
import networkx as nx
from sys import maxsize


def generate_graph(graph):
    """
    Given a Graph.py representation of a graph, creates a networkx graph, g.
    The function adds the vertices and edges in graph to g, translating the graph
    to the origin and scaling its coordinates down by n.
    This function was originally use to convert graphs to networkx before they were
    displayed by draw_graph(), however, it has been replaced by Graph.convert_networkx().
    :param graph: a Graph.py representation of a graph
    :return: a networkx representation of graph, scaled and translated
    """
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
    Returns a unique RGB value given a number.
    Used to color each node uniquely based on its identifier.
    Currently unused
    :param key: an integer value
    :return: (r,g,b), where r,g,b are ints between 0 and 256
    """
    r = (key & 0xFF0000) >> 16
    g = (key & 0x00FF00) >> 8
    b = (key & 0x0000FF)
    return r, g, b


def draw_graph(graph, title, filename):
    """
    Given a networkx graph, display the graph in an interactable HTML file using plotly.
    The HTML file will automatically open after it is generated.
    :param graph: the networkx graph to be displayed
    :param title: the title to display above the graph
    :param filename: the name to save the HTML file as in nav-research/graph_displays/generated/
    """
    # graph = generate_graph(graph)

    edge_trace = []
    for edge in graph.edges(data=True):
        x0, y0 = edge[0]
        x1, y1 = edge[1]

        # Determine the color of the edge based on its previously generated color value
        jam_or_path = edge[2].get('color')
        # If the edge has no Jam and no path then it will be black
        color = 'black'
        # If an edge is jammed it is colored red
        if jam_or_path == 1:
            color = 'red'
        # If an edge is part of a path it will be colored with the same color as the other edges in that path.
        # GraphDisplay currently shows up to 4 uniquely colored paths at a time, more can be shown with additions here.
        elif jam_or_path == 2:
            color = 'green'
        elif jam_or_path == 3:
            color = 'blue'
        elif jam_or_path == 4:
            color = 'yellow'
        elif jam_or_path == 5:
            color = 'purple'

        # Display the weight of an edge when you hover over it on the displayed graph.
        weight = "Edge Weight: " + str(edge[2].get('weight'))

        # Create a scatter plot with just this edge and append it to the list of edges
        edge_trace.append(go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode='lines',
            text=weight,
            hoverinfo='text',
            line=dict(width=5, color=color)))

    # Create a scatter plot of the nodes with a scale based on their discover time
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

    # Append the node coordinates to the node_trace
    for node in graph.nodes():
        x, y = node
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    node_hash = {}
    max_node = 0
    done = set()
    for node, adjacencies in enumerate(graph.adjacency()):
        # Give each node an identifier based when we discover it here, check for duplicate nodes
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

        # Show a node's identifier when you hover over it on the displayed graph
        node_info = "Node " + str(identifier)

        # Append a node's connections to the text to display when you hover over a node on the graph
        node_info += ": connected to: ["
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
        node_info = node_info[:-2] + "]"

        # Append the coordinates of a node to the text that shows when you hover over it
        node_info += " is at: (" + str(n[0]) + "," + str(n[1]) + ")"

        # Append the number of connections it has to the displayed text
        node_info += ' # of connections: ' + str(len(adjacencies[1]))

        node_trace['text'] += tuple([node_info])

        # Color the node based on its given color value
        node_trace['marker']['color'] += tuple([graph.nodes[n]['color']])

    # Put the edges and nodes into one figure, generate the display, and save it at the below path
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
