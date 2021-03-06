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


def valid_feature(tags):
    """
    Determines if the feature represented by the given tags is valid, i.e. a road
    :param tags: a list of tags from an OSM feature
    :return: true if the feature is valid, false otherwise
    """
    if len(tags) == 0:
        return True
    invalid_roads = ["footpath", "pedestrian", "track", "bus_guideway", "raceway", "bridleway", "steps", "path",
                     "proposed", "footway"]
    for tag in tags:
        if (tag.attrib["k"] == "highway" and tag.attrib["v"] not in invalid_roads) or \
           (tag.attrib["k"] == "route" and tag.attrib["v"] != "road"):
            return True
    return False


def is_oneway(tags):
    """
    Determines if the way represented by the given tags is one-way
    :param tags: a list of tags from an OSM way
    :return: true if the way is one-way, false otherwise
    """
    for tag in tags:
        if tag.attrib["k"] == "oneway" and tag.attrib["v"] == "yes":
            return True
    return False


def max_speed(tags):
    """
    Determines if the way represented by the given tags is one-way
    :param tags: a list of tags from an OSM way
    :return: the max_speed (in mph) of the given way, or 0 if none is specified
    """
    for tag in tags:
        if tag.attrib["k"] == "maxspeed":
            speed = tag.attrib["v"].split()
            if len(speed) > 1 and speed[1] == "mph":
                return int(speed[0])
            if len(speed) > 1 and speed[1] == "knots":
                return int(speed[0]) * 1.15078
            else:
                return int(speed[0]) * 0.6213712

    return 0


def parse_osm(path):
    """
    Given a path to an OSM extract, read the file line by line and construct a graph from nodes and ways (edges).
    :param path: a path to an .osm file relative to this file.
    :return: A Graph.py representation of a graph.
    """
    vertices = {}
    edges = []
    ways = {}

    root = elementTree.parse(path).getroot()
    for child in root:

        if child.tag == "node":
            # A list of all of the metadata of this node that is used to filter out unwanted nodes and store metadata
            tags = child.findall('tag')

            if not valid_feature(tags):
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
            # Boolean flag to handle two-way edge flipping.
            oneway = is_oneway(tags)
            # The speed limit of the way, or 0 if there is not one specified
            speed = max_speed(tags)

            if not valid_feature(tags):
                continue

            prev_vertex = None
            first_vertex = None
            for node in nds:
                ''' 
                There can be nodes that were filtered out already still in these ways, so if they are not in the
                vertices dictionary, we'll need to skip them. 
                For example if a road and a railway intersect, the point at which they intersect could still be
                in a way representing a road, even though it's a railway node.
                '''
                if node.attrib['ref'] not in vertices:
                    continue

                vertex = vertices[node.attrib['ref']]
                if prev_vertex:
                    # The haversine distance between the two vertexes
                    distance = abs(haversine(prev_vertex, vertex))
                    edges.append(Edge(prev_vertex, vertex, distance, speed))

                    # If the way is one-way, flip the edge and append it
                    if not oneway:
                        edges.append(Edge(vertex, prev_vertex, distance, speed))
                else:
                    first_vertex = vertex
                prev_vertex = vertex

            ways[child.attrib['id']] = (first_vertex, prev_vertex)  # store the first and last vertex of the way

            # Iterate through the tags of each way to parse its associated metadata
            # for tag in tags:
            #     print(tag.tag, tag.attrib)

        elif child.tag == "relation":
            # A list of ids of members (either ways or nodes) in this relation
            members = child.findall('member')
            # A list of all of the metadata of this relation that is used to filter out unwanted ways and store metadata
            tags = child.findall('tag')

            if not valid_feature(tags):
                continue

            prev_vertex = None
            for member in members:
                mem_type = member.attrib['type']
                mem_id = member.attrib['ref']
                ''' 
                There can be nodes that were filtered out already still in these ways, so if they are not in the
                vertices dictionary, we'll need to skip them. 
                For example if a road and a railway intersect, the point at which they intersect could still be
                in a way representing a road, even though it's a railway node.
                '''
                if mem_id not in vertices and mem_id not in ways:
                    continue

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

            # Iterate through the tags of each relation to parse its associated metadata
            # for tag in tags:
            #     print(tag.tag, tag.attrib)
    return Graph(edges)
