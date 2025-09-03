from pudu_ui import App
from pyglet.math import Vec2

from settings_screen import SettingsScreen
from simulation_screen import SimulationScreen


class PanelsApp(App):
    def __init__(self):
        super().__init__(caption="Solar Panels")
        self.memo = {}

        # Start with the settings
        settings_screen = SettingsScreen()
        settings_screen.button.on_press = self.simulate
        self.push_handlers(settings_screen)

        self.set_screen(settings_screen)

    @staticmethod
    def hash_rect(dims: Vec2) -> str:
        return f"{int(dims.x)}x{int(dims.y)}"

    def max_panels(
        self, pos: Vec2, dims: Vec2, panel_dims: Vec2
    ) -> list[tuple[Vec2, Vec2]]:
        a, b = panel_dims.x, panel_dims.y
        if not dims.x or not dims.y:
            return []
        # print(pos, dims)
        h = self.hash_rect(dims)
        if h in self.memo:
            answer = []
            for panel_pos, panel_dims in self.memo[h]:
                answer.append((pos + panel_pos, panel_dims))
            return answer

        x = dims.x
        y = dims.y

        panel_x = a
        panel_y = b

        # Try with panel_x in row
        op1 = []
        op2 = []
        if x >= panel_x and y >= panel_y:
            op1.append((pos, Vec2(panel_x, panel_y)))
            remaining_x = x - panel_x
            left_pos = pos + Vec2(panel_x, 0)
            while remaining_x >= panel_x:
                op1.append((left_pos, Vec2(panel_x, panel_y)))
                remaining_x -= panel_x
                left_pos += Vec2(panel_x, 0)
            new_pos = pos + Vec2(0, panel_y)
            new_dims = Vec2(x, y - panel_y)
            op1 += self.max_panels(new_pos, new_dims, panel_dims)

        # Try with panel_x in columns
        if x >= panel_x and y >= panel_y:
            op2 = [(pos, Vec2(panel_x, panel_y))]
            remaining_y = y - panel_y
            left_pos = pos + Vec2(0, panel_y)
            while remaining_y >= panel_y:
                op2.append((left_pos, Vec2(panel_x, panel_y)))
                remaining_y -= panel_y
                left_pos += Vec2(0, panel_y)
            new_pos = pos + Vec2(panel_x, 0)
            new_dims = Vec2(x - panel_x, y)
            op2 += self.max_panels(new_pos, new_dims, panel_dims)

        op3 = []
        op4 = []
        if a != b:
            panel_x = b
            panel_y = a
            if x >= panel_x and y >= panel_y:
                op3.append((pos, Vec2(panel_x, panel_y)))
                remaining_x = x - panel_x
                left_pos = pos + Vec2(panel_x, 0)
                while remaining_x >= panel_x:
                    op3.append((left_pos, Vec2(panel_x, panel_y)))
                    remaining_x -= panel_x
                    left_pos += Vec2(panel_x, 0)
                new_pos = pos + Vec2(0, panel_y)
                new_dims = Vec2(x, y - panel_y)
                op3 += self.max_panels(new_pos, new_dims, panel_dims)

            if x >= panel_x and y >= panel_y:
                op4 = [(pos, Vec2(panel_x, panel_y))]
                remaining_y = y - panel_y
                left_pos = pos + Vec2(0, panel_y)
                while remaining_y >= panel_y:
                    op4.append((left_pos, Vec2(panel_x, panel_y)))
                    remaining_y -= panel_y
                    left_pos += Vec2(0, panel_y)
                new_pos = pos + Vec2(panel_x, 0)
                new_dims = Vec2(x - panel_x, y)
                op4 += self.max_panels(new_pos, new_dims, panel_dims)

        options = [op1, op2, op3, op4]
        best_option = op1
        for option in options:
            if len(option) > len(best_option):
                best_option = option
        self.memo[h] = best_option

        return best_option

    def simulate(self, btn):
        self.pop_handlers()
        values = self.current_screen.get_values()
        panels = self.max_panels(
            Vec2(), Vec2(values['x'], values['y']),
            Vec2(values['a'], values['b'])
        )
        sim_screen = SimulationScreen(
            self.width, self.height, values['x'], values['y'], panels
        )
        self.set_screen(sim_screen)
