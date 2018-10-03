from kivy.app import App
from kivy.uix.widget import Widget
from Graph import Graph


class GraphDisplayWidget(Widget):
    pass


class GraphDisplayApp(App):
    def build(self):
        return DisplayVertex()


class DisplayVertex(Widget):
    x_position = 25  # roughly corresponds to the longitude of a vertex, but can be adjusted for display purposes
    y_position = 25  # roughly corresponds to the latitude of a vertex, but can be adjusted for display purposes
    vertex_number = "1492"  # the id of the vertex

    def parse_vertex(self, vertex):
        """
        A sort of constructor for a display vertex
        :param vertex: the vertex to be parsed into a display vertex
        :return: NULL
        """
        self.x_position = vertex.get_longitude()
        self.y_position = vertex.get_latitude()
        self.vertex_number = str(vertex.get_identifier())


def graph_to_kv(Graph):
    with open("GraphDisplay.kv", "wt") as out_kv:
        out_kv.write("")


if __name__ == '__main__':
    GraphDisplayApp().run()