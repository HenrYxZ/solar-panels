from pudu_ui import Label, LabelParams, Screen
from pudu_ui.utils import fit_screen
import pudu_ui
from pyglet.gl.gl_compat import glClearColor
from pyglet.math import Vec2
from pyglet.graphics import Group


from components import Panel, Roof


class SimulationScreen(Screen):
    def __init__(
        self, width: int, height: int, x: float, y: float,
        panels: list[tuple[Vec2, Vec2]]
    ):
        super().__init__("Simulation")
        self.width = width
        self.height = height
        self.canvas_max_width = int(width * 0.8)
        self.canvas_max_height = int(height * 0.75)

        self.back_group = Group(order=0)
        self.front_group = Group(order=1)

        roof, pixel_size = self.create_roof(x, y)
        self.create_panels(roof, panels, pixel_size)
        if len(roof.children) > 0:
            roof.children[0].show_dims()

        params = LabelParams(
            x=width / 2,
            y=height * 0.95,
            anchor_x='center', anchor_y='center',
            style=pudu_ui.styles.fonts.FontStyle(
                color=pudu_ui.colors.WHITE
            ),
            text=f"{len(panels)} panels fit in the roof"
        )
        self.label = Label(params, batch=self.batch)
        # Use black background
        glClearColor(0.0, 0.0, 0.0, 0.0)

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
        self.widgets.append(roof)
        return roof, pixel_size

    def create_panels(
        self, roof: Roof, panels: list[tuple[Vec2, Vec2]], pixel_size: float
    ):
        for panel_pos, panel_dims in panels:
            x = panel_pos.x * pixel_size
            y = panel_pos.y * pixel_size
            panel_width = int(panel_dims.x * pixel_size)
            panel_height = int(panel_dims.y * pixel_size)
            new_panel = Panel(
                x, y, panel_width, panel_height,
                roof, panel_dims, group=self.front_group
            )
            roof.children.append(new_panel)
