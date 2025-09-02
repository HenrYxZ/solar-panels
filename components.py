from pudu_ui import Frame, FrameParams, Label, LabelParams, WidgetGroup
import pudu_ui
from pyglet.graphics import Batch, Group
from pyglet.math import Vec2


PANEL_RADIUS = 12


class Roof(Frame):
    def __init__(
        self, x: float, y: float, width: int, height: int, dims: Vec2,
        batch:Batch, group:Group
    ):
        params = FrameParams(
            x=x, y=y, width=width, height=height
        )
        params.style.set_solid_color(pudu_ui.colors.GRAY)
        super().__init__(params, batch=batch, group=group)

        # debug labels
        debug_group = Group(order=5, parent=group)
        label_style = pudu_ui.styles.fonts.FontStyle(
            color=pudu_ui.colors.WHITE
        )
        label_params = LabelParams(
            x=-40, y=self.height//2, text=f"x={dims.x}",
            anchor_x='center', anchor_y='center', style=label_style
        )
        self.x_label = Label(label_params, batch=batch, group=debug_group,
            parent=self)

        label_params.x = self.width // 2
        label_params.y = -20
        label_params.text = f"y={dims.y}"
        self.y_label = Label(
            label_params, batch=batch, group=debug_group, parent=self
        )


class Panel(Frame):
    def __init__(
        self, x: float, y: float, width: int, height: int, roof: Roof,
        dims: Vec2, group:Group
    ):
        batch = roof.batch
        params = FrameParams(
            x=x, y=y, width=width, height=height
        )
        params.style.set_solid_color(pudu_ui.colors.MEDIUM_BLUE)
        params.style.set_uniform_radius(PANEL_RADIUS)
        params.style.border_width = 2
        params.style.border_color = pudu_ui.colors.BLACK
        super().__init__(params, batch=batch, group=group, parent=roof)

        # debug labels
        self.debug_group = WidgetGroup(self, order=5, parent=group)
        label_style = pudu_ui.styles.fonts.FontStyle(
            font_size=14,
            color=pudu_ui.colors.RED
        )
        label_params = LabelParams(
            x=-20, y=self.height // 2, text=f"x={dims.x}",
            anchor_x='center', anchor_y='center', style=label_style
        )
        self.x_label = Label(
            label_params, batch=batch, group=self.debug_group, parent=self
        )

        label_params.x = self.width // 2
        label_params.y = -20
        label_params.text = f"y={dims.y}"
        self.y_label = Label(
            label_params, batch=batch, group=self.debug_group, parent=self
        )
        self.debug_group.visible = False


    def show_dims(self):
        self.debug_group.visible = True
