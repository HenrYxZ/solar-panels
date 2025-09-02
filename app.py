from pudu_ui import App
from pudu_ui.utils import fit_screen
from pyglet.math import Vec2
from pyglet.graphics import Group


from components import Panel, Roof


class PanelsApp(App):
    def __init__(self, roof_x, roof_y, panels: list[tuple[Vec2, Vec2]]):
        super().__init__(caption="Solar Panels")
        self.canvas_max_width = int(self.width * 0.8)
        self.canvas_max_height = int(self.height * 0.75)

        self.back_group = Group(order=0)
        self.front_group = Group(order=1)

        roof, pixel_size = self.create_roof(roof_x, roof_y)
        self.create_panels(roof, panels, pixel_size)
        if len(roof.children) > 0:
            roof.children[0].show_dims()

    def create_roof(self, x: float, y: float):
        if x > y:
            pixel_size = self.canvas_max_width // x
        else:
            pixel_size = self.canvas_max_height // y

        roof_width = int(pixel_size * x)
        roof_height = int(pixel_size * y)
        roof_width, roof_height = fit_screen(
            self.canvas_max_width, self.canvas_max_height,
            roof_width, roof_height
        )
        pixel_size = int(roof_width / x)

        roof_x = self.width // 2 - roof_width // 2
        roof_y = self.height // 2 - roof_height // 2
        roof = Roof(
            roof_x, roof_y, roof_width, roof_height, Vec2(x, y),
            batch=self.batch, group=self.back_group
        )
        self.current_screen.widgets.append(roof)
        return roof, pixel_size

    def create_panels(
        self, roof: Roof, panels: list[tuple[Vec2, Vec2]], pixel_size: float
    ):
        for panel_pos, panel_dims in panels:
            x = panel_pos.x * pixel_size
            y =panel_pos.y * pixel_size
            panel_width = int(panel_dims.x * pixel_size)
            panel_height = int(panel_dims.y * pixel_size)
            new_panel = Panel(
                x, y, panel_width, panel_height,
                roof, panel_dims, group=self.front_group
            )
            roof.children.append(new_panel)
