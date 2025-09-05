from pudu_ui import Button, ButtonParams, Label, LabelParams, Screen
from pudu_ui.layouts import ListLayoutParams, ListLayout, ListDirection
from pyglet.gl import glClearColor


from components import Setting


class SettingsScreen(Screen):
    def __init__(self):
        super().__init__(name="Settings")

        params = LabelParams(
            x=200, y=650, text="Settings"
        )
        self.title = Label(params, batch=self.batch)

        self.set_x = Setting(
            "x:", 5, 1, 100, batch=self.batch
        )
        self.set_y = Setting(
            "y:", 3,1, 100, batch=self.batch
        )
        self.set_a = Setting(
            "a:", 1, 1, 10, batch=self.batch
        )
        self.set_b = Setting(
            "b:", 2, 1, 10, batch=self.batch
        )

        params = ButtonParams(text="Simulate")
        self.button = Button(params, batch=self.batch)

        params = ListLayoutParams(
            x=200, y=100, width=400, height=550,
            inter_item_spacing=10,
            direction=ListDirection.VERTICAL
        )
        self.list_layout = ListLayout(params, batch=self.batch)
        self.list_layout.add(self.set_x)
        self.list_layout.add(self.set_y)
        self.list_layout.add(self.set_a)
        self.list_layout.add(self.set_b)
        self.list_layout.add(self.button)

        self.list_layout.invalidate()
        # self.list_layout.set_debug_mode()
        self.set_a.set_debug_mode()

        self.widgets.append(self.title)
        self.widgets.append(self.list_layout)
        self.widgets.append(self.set_x)
        self.widgets.append(self.set_y)
        self.widgets.append(self.set_a)
        self.widgets.append(self.set_b)


    def draw(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        super().draw()

    def get_values(self):
        values = {
            'x': int(self.set_x.value),
            'y': int(self.set_y.value),
            'a': int(self.set_a.value),
            'b': int(self.set_b.value)
        }
        return values
