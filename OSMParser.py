import xml.etree.ElementTree as elementTree
from Graph import Graph, Vertex, Edge
from math import radians, sin, cos, asin, sqrt


def haversine(vertex1, vertex2):
    """
    Calculates the distance in kilometers between the GPS coordinates of the given vertices using the Haversine formula.
    Our code is based off of information and code found here: https://rosettacode.org/wiki/Haversine_formula#Python
    :param vertex1: the first vertex
    :param vertex2: the second vertex
    :return: the distance in kilometers between the two given vertexes
    """
    earth_radius = 6372.8  # Earth radius in kilometers
    lat1 = radians(vertex1.get_latitude())
    lat2 = radians(vertex2.get_latitude())
    delta_lat = lat2 - lat1
    delta_long = radians(vertex2.get_longitude() - vertex1.get_longitude())

    a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_long / 2) ** 2
    c = 2 * asin(sqrt(a))
    return earth_radius * c


def parse_osm(path):
    vertices = {}
    edges = []
    ways = {}

    root = elementTree.parse(path).getroot()
    for child in root:
        if child.tag == "node":
            # A list of all of the metadata of this node that is used to filter out unwanted nodes and store metadata
            tags = child.findall('tag')

            for tag in tags:
                if tag.attrib["k"] in ["railway", "bicycle"]:
                    continue

            attribs = child.attrib
            vert = Vertex(int(attribs['id']), float(attribs['lat']), float(attribs['lon']))
            vertices[attribs['id']] = vert

            # Iterate through the tags of each node to parse its associated metadata
            # for tag in tags:
            #     print(tag.tag, tag.attrib)

        elif child.tag == "way":
            # A list of ids of nodes in this way
            nds = child.findall('nd')
            # A list of all of the metadata of this way that is used to filter out unwanted ways and store metadata
            tags = child.findall('tag')

            for tag in tags:
                if tag.attrib["k"] in ["railway"]:
                    continue
                if tag.attrib["k"] in ["cycleway"] and tag.attrib["v"] == "yes":
                    continue

            prev_vertex = None
            first_vertex = None
            for node in nds:
                vertex = vertices[node.attrib['ref']]
                if prev_vertex:
                    edges.append(Edge(prev_vertex, vertex, abs(haversine(prev_vertex, vertex))))
                else:
                    first_vertex = vertex
                prev_vertex = vertex
            ways[child.attrib['id']] = (first_vertex, prev_vertex)  # captures the first and last vertex of every way

            # Iterate through the tags of each node to parse its associated metadata
            # for tag in tags:
            #     print(tag.tag, tag.attrib)
        elif child.tag == "relation":
            valid = False
            tags = child.findall('tag')
            members = child.findall('member')

            for tag in tags:
                if tag.attrib['k'] not in ['route']:
                    continue
                else:
                    if tag.attrib['v'] not in ['road']:
                        break
                    else:
                        valid = True
                        break
            if valid:
                prev_vertex = None
                for member in members:
                    mem_type = member.attrib['type']
                    mem_id = member.attrib['ref']
                    if prev_vertex:
                        if mem_type in ['way']:
                            way = ways[mem_id]
                            new_edge = Edge(prev_vertex, way[0], abs(haversine(prev_vertex, way[0])))
                            edges.append(new_edge)
                            prev_vertex = way[1]

                        elif mem_type in ['node']:
                            vertex = vertices[mem_id]
                            new_edge = Edge(prev_vertex, vertex, abs(haversine(prev_vertex, vertex)))
                            edges.append(new_edge)
                            prev_vertex = vertex
                    else:
                        if mem_type in ['way']:
                            prev_vertex = ways[mem_id][1]
                        elif mem_type in ['node']:
                            prev_vertex = vertices[mem_id]

    return Graph(edges)
