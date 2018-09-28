from kivy.app import App
from kivy.uix.widget import Widget


class GraphDisplayWidget(Widget):
    pass


class DisplayApp(App):
    def build(self):
        return GraphDisplayWidget()


if __name__ == '__main__':
    DisplayApp().run()