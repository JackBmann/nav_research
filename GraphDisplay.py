from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

from Graph import Vertex

root = Builder.load_string("""
Screen:
    FloatLayout:
""")


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



class GraphDisplayApp(App):
    """

    """

    vertices = []

    def build(self):
        f = FloatLayout()
        for vertex in self.vertices:
            v = Button(text = str(vertex.get_identifier()), font_size = 20, size_hint = (.1, .1))
            v.pos = (vertex.get_longitude()*4, vertex.get_latitude()*4)
            f.add_widget(v)
        return f

    def set_vertices(self, vertices):
        self.vertices = vertices

if __name__ == '__main__':
    newApp = GraphDisplayApp()
    newApp.set_vertices([Vertex(1, 70, 70), Vertex(2, 50, 50)])
    newApp.run()
