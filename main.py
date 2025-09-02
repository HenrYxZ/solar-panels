from pyglet.math import Vec2


from app import PanelsApp


#a = 1
a = 5
b = 3
memo = {}


def hash_rect(dims: Vec2) -> str:
    return f"{int(dims.x)}x{int(dims.y)}"


def max_panels(pos: Vec2, dims: Vec2) -> list[tuple[Vec2, Vec2]]:
    if dims.x < a or dims.y < b:
        return []
    #print(pos, dims)
    h = hash_rect(dims)
    if h in memo:
        answer = []
        for panel_pos, panel_dims in memo[h]:
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
        op1 += max_panels(new_pos, new_dims)

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
        op2 += max_panels(new_pos, new_dims)

    answer = op1 if len(op1) > len(op2) else op2
    memo[h] = answer

    return answer


if __name__ == '__main__':
    #x = 5
    x = 25
    #y = 3
    y = 15
    panels = max_panels(Vec2(), Vec2(x, y))
    #print(panels)
    # print(memo.keys())

    app = PanelsApp(x, y, panels)
    app.run()
