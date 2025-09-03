from pudu_ui import (
    Frame, FrameParams, Label, LabelParams, Slider, SliderParams,
    Widget, WidgetGroup
)
import pudu_ui
from pyglet.event import EVENT_HANDLE_STATE
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


class Setting(Widget):
    def __init__(
        self, label_str: str,
        value: float, min_value: float, max_value: float, batch: Batch
    ):
        super().__init__()
        label_params = LabelParams(
            x=20, text=label_str
        )
        self.label = Label(label_params, batch=batch, parent=self)

        value_label_params = LabelParams(x=300, text=f"{value}")
        self.value_label = Label(value_label_params, batch=batch, parent=self)

        slider_params = SliderParams(
            x=100, min_value=min_value, max_value=max_value, value=value,
            on_value_changed=self.on_value_changed
        )
        self.slider = Slider(slider_params, batch=batch, parent=self)

        self.children.append(self.label)
        self.children.append(self.slider)
        self.children.append(self.value_label)

    @property
    def value(self) -> float:
        return self.slider.value

    # def recompute(self):
    #     super().recompute()
    #     self.label.invalidate()
    #     self.slider.invalidate()
    #     self.value_label.invalidate()

    def on_value_changed(self, slider: Slider):
        self.value_label.text = f"{int(slider.value)}"
        self.value_label.invalidate()
        self.invalidate()

    def on_mouse_press(self, *args) -> EVENT_HANDLE_STATE:
        return self.slider.on_mouse_press(*args)

    def on_mouse_release(self, *args) -> EVENT_HANDLE_STATE:
        return self.slider.on_mouse_release(*args)

    def on_mouse_motion(self, *args) -> EVENT_HANDLE_STATE:
        return self.slider.on_mouse_motion(*args)

    def on_mouse_drag(self, *args) -> EVENT_HANDLE_STATE:
        return self.slider.on_mouse_drag(*args)
