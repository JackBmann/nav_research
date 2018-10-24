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


def draw_graph(graph):
    #g = generate_graph(graph)
    g = graph
    #print(g.edges)
    pos = nx.get_node_attributes(g, 'pos')
    dmin = 1
    ncenter = 0
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5) ** 2 + (y - 0.5) ** 2
        if d < dmin:
            ncenter = n
            dmin = d

    #p = nx.single_source_shortest_path_length(g, ncenter)

    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in g.edges():
        #x0, y0 = g.node[edge[0]]['pos']
        #x1, y1 = g.node[edge[1]]['pos']
        x0, y0 = edge[0]
        x1, y1 = edge[1]
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in g.nodes():
        #x, y = g.node[node]['pos']
        x, y = node
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    for node, adjacencies in enumerate(g.adjacency()):
        node_trace['marker']['color'] += tuple([len(adjacencies[1])])
        node_info = '# of connections: ' + str(len(adjacencies[1]))
        node_trace['text'] += tuple([node_info])

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='<br>Garph',
                        titlefont=dict(size=16),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Created by Michael Bolot, Jack Baumann, and Dr. David Andrews using "
                                 "<a href='https://plot.ly/python/network-graphs/'>plotly.networkx</a>.",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    plotly.offline.plot(fig, filename='GraphDisplay.html')
