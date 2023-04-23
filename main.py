import queue
import time

import pygame
import random

pygame.init()

width = 800
height = 800
rows = 10
cols = 10
mines = 15

size = width / rows

num_font = pygame.font.SysFont('Arial', 25, bold=True)
lost_font = pygame.font.SysFont('Arial', 45, bold=True)
time_font = pygame.font.SysFont('Arial', 35, bold=True)

num_colors = {1: 'green', 2: 'red', 3: 'orange', 4: 'purple', 5: 'blue', 6: 'black', 7: 'pink', 8: 'yellow'}
rect_color = (200, 200, 200)
clicked_rect_color = (140, 140, 140)
flag_color = 'red'
bomb_color = 'red'

rec_color = 'white'
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Сапер_nfactorial')

background_color = 'white'


def get_neigh(row, col, rows, cols):
    neighbors = []

    if row > 0:
        neighbors.append((row - 1, col))
    if row < rows - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < cols - 1:
        neighbors.append((row, col + 1))

    if row > 0 and col > 0:
        neighbors.append((row - 1, col - 1))
    if row < rows - 1 and col < cols - 1:
        neighbors.append((row + 1, row + 1))
    if row < rows - 1 and col > 0:
        neighbors.append((row + 1, col - 1))
    if row > 0 and col < cols - 1:
        neighbors.append((row - 1, col + 1))

    return neighbors


def create_field(rows, cols, mines):
    field = [[0 for _ in range(cols)] for _ in range(rows)]
    mines_pos = set()

    while len(mines_pos) < mines:
        row = random.randrange(0, rows)
        col = random.randrange(0, cols)
        pos = row, col

        if pos in mines_pos:
            continue

        mines_pos.add(pos)
        field[row][col] = -1

    for mine in mines_pos:
        neighbors = get_neigh(*mine, rows, cols)
        for r, c in neighbors:
            if field[r][c] != -1:
                field[r][c] += 1

    return field


def draw(win, field, cover_field, current_time):
    win.fill(background_color)

    time_text = time_font.render(f'Time Elapsed: {round(current_time)}', 1, 'black')
    win.blit(time_text, (10, height - time_text.get_height()))

    for i, row in enumerate(field):
        y = size * i
        for j, value in enumerate(row):
            x = size * j

            is_covered = cover_field[i][j] == 0
            is_flag = cover_field[i][j] == -2
            is_bomb = value == -1

            if is_flag:
                pygame.draw.rect(win, flag_color, (x, y, size, size))
                pygame.draw.rect(win, 'black', (x, y, size, size), 2)
                continue

            if is_covered:
                pygame.draw.rect(win, rec_color, (x, y, size, size))
                pygame.draw.rect(win, 'black', (x, y, size, size), 2)
                continue
            else:
                pygame.draw.rect(win, clicked_rect_color, (x, y, size, size))
                pygame.draw.rect(win, 'black', (x, y, size, size), 2)
                if is_bomb:
                    pygame.draw.circle(win, bomb_color, (x + size / 2, y + size / 2), radius=size / 2 - 4)

            if value > 0:
                text = num_font.render(str(value), 1, num_colors[value])
                win.blit(text, (x + (size / 2 - text.get_width() / 2), y + (size / 2 - text.get_height() / 2)))

    pygame.display.update()


def uncover_from_pos(row, col, cover_field, field):
    q = queue.Queue()
    q.put((row, col))
    visited = set()

    while not q.empty():
        current = q.get()

        neighbors = get_neigh(*current, rows, cols)
        for r, c in neighbors:
            if (r, c) in visited:
                continue

            value = field[r][c]
            if value == 0 and cover_field[r][c] != -2:
                q.put((r, c))

            if cover_field[r][c] != -2:
                cover_field[r][c] = 1
            visited.add((r, c))


def get_grid_pos(mouse_pos):
    mx, my = mouse_pos
    row = int(my // size)
    col = int(mx // size)

    return row, col


def draw_lost(win, text):
    text = lost_font.render(text, 1, 'black')
    win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    pygame.display.update()


def main():
    run = True
    field = create_field(rows, cols, mines)
    cover_field = [[0 for _ in range(cols)] for _ in range(rows)]
    flags = mines
    clicks = 0
    start_time = time.time()

    while run:
        current_time = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_grid_pos(pygame.mouse.get_pos())
                if row >= rows or col >= cols:
                    continue

                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0] and cover_field[row][col] != -2:
                    cover_field[row][col] = 1

                    if field[row][col] == -1:
                        draw(win, field, cover_field, current_time)
                        draw_lost(win, 'Вы проиграли! Попробуйте ещё раз')
                        pygame.time.delay(5000)
                        field = create_field(rows, cols, mines)
                        cover_field = [[0 for _ in range(cols)] for _ in range(rows)]
                        flags = mines
                        clicks = 0

                    if clicks == 0 or field[row][col] == 0:
                        uncover_from_pos(row, col, cover_field, field)
                    if clicks == 0:
                        start_time = time.time()
                    clicks += 1

                elif mouse_pressed[2]:
                    if cover_field[row][col] == -2:
                        cover_field[row][col] = 0
                        flags += 1
                    else:
                        flags -= 1
                        cover_field[row][col] = -2

        draw(win, field, cover_field, current_time)

    pygame.quit()


if __name__ == '__main__':
    main()
