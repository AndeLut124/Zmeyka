import pgzrun
import random

WIDTH = 500
HEIGHT = 500
TITLE = "Змейка"

CELL = 25
MOVE_DELAY = 0.2

snake = [(10, 10), (9, 10), (8, 10)]
dx = 1
dy = 0
move_timer = 0.0

food = None
score = 0
game_over = False
game_win = False

key_queue = []

my_map = [
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [6, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 7],
]

cell = Actor("pustoy_block")
cell1 = Actor("wall_block_1")
cell2 = Actor("wall_block_2")
cell3 = Actor("wall_block_3")
cell5 = Actor("wall_block_5")
cell6 = Actor("wall_block_6")
cell7 = Actor("wall_block_7")
cell8 = Actor("wall_block_8")
cell9 = Actor("wall_block_9")

snake_head = Actor("snake_green_head")
snake_body = Actor("snake_green_blob")
apple = Actor("apple")

tiles = {
    0: cell,
    1: cell1,
    2: cell2,
    3: cell3,
    5: cell5,
    6: cell6,
    7: cell7,
    8: cell8,
    9: cell9,
}


def map_draw():
    for y, row in enumerate(my_map):
        for x, value in enumerate(row):
            tile = tiles.get(value)
            if tile:
                tile.left = x * CELL
                tile.top = y * CELL
                tile.draw()


def draw():
    map_draw()

    if food is not None:
        apple.center = (food[0] * CELL + CELL // 2, food[1] * CELL + CELL // 2)
        apple.draw()

    for i, (x, y) in enumerate(snake):
        actor = snake_head if i == 0 else snake_body
        actor.left = x * CELL
        actor.top = y * CELL
        actor.draw()

    screen.draw.text(f"Score: {score}", (10, 5), color="white")

    if game_over:
        screen.draw.text("GAME OVER", center=(250, 250), fontsize=40, color="red")
    elif game_win:
        screen.draw.text("YOU WIN!!!", center=(250, 250), fontsize=40, color="red")


def spawn_food():
    global food, game_win

    empty = []
    for y, row in enumerate(my_map):
        for x, value in enumerate(row):
            if value == 0 and (x, y) not in snake:
                empty.append((x, y))

    if not empty:
        food = None
        game_win = True
    else:
        food = random.choice(empty)


def update(dt):
    global dx, dy, move_timer, snake, food, score, game_over, game_win

    if game_over or game_win:
        return

    if keyboard.left and dx != 1:
        key_queue.append((-1, 0))
    elif keyboard.right and dx != -1:
        key_queue.append((1, 0))
    elif keyboard.up and dy != 1:
        key_queue.append((0, -1))
    elif keyboard.down and dy != -1:
        key_queue.append((0, 1))

    move_timer += dt

    if move_timer < MOVE_DELAY:
        return

    move_timer = 0

    if key_queue:
        new_dx, new_dy = key_queue.pop(0)
        if (new_dx, new_dy) != (-dx, -dy):
            dx, dy = new_dx, new_dy
            if dx == 1:
                snake_head.angle = 0
            elif dx == -1:
                snake_head.angle = 180
            elif dy == -1:
                snake_head.angle = 90
            elif dy == 1:
                snake_head.angle = 270

    hx, hy = snake[0]
    new_head = (hx + dx, hy + dy)
    x, y = new_head

    if not (0 <= x < len(my_map[0]) and 0 <= y < len(my_map)):
        game_over = True
        return

    if my_map[y][x] != 0:
        game_over = True
        return

    if new_head in snake[:-1]:
        game_over = True
        return

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        spawn_food()
    else:
        snake.pop()


spawn_food()
pgzrun.go()