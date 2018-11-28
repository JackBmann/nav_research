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
            for node in nds:
                vertex = vertices[node.attrib['ref']]
                if prev_vertex:
                    edges.append(Edge(prev_vertex, vertex, abs(haversine(prev_vertex, vertex))))
                prev_vertex = vertex

            # Iterate through the tags of each node to parse its associated metadata
            # for tag in tags:
            #     print(tag.tag, tag.attrib)

        # elif child.tag == "relation":
        #     print(child.tag, child.attrib)
        #     for grandchild in child:
        #         if grandchild.tag == "nd":
        #             print(grandchild.tag, grandchild.attrib)
        #         elif grandchild.tag == "tag":
        #             print(grandchild.tag, grandchild.attrib)

    return Graph(edges)
