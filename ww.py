import pygame


N = 100
WIDTH = HEIGHT = 500
RES = WIDTH, HEIGHT
START_TILE = 50
FPS = 120
FPT = 24
INF_SIGNALS = False


def n_signals(x, y, field):
    res = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx != 0 or dy != 0:
                if field[(x + dx) % N][(y + dy) % N] == 'S':
                    res += 1
    return res


def update_field(field):
    new_field = [field[q].copy() for q in range(len(field))]
    for q in range(N):
        for w in range(N):
            if field[q][w] == '':
                new_field[q][w] = ''
            elif field[q][w] == 'S':
                if INF_SIGNALS:
                    new_field[q][w] = 'S'
                else:
                    new_field[q][w] = 'T'
            elif field[q][w] == 'T':
                new_field[q][w] = 'W'
            elif field[q][w] == 'W':
                if n_signals(q, w, field) in [1, 2]:
                    new_field[q][w] = 'S'
                else:
                    new_field[q][w] = 'W'
    return new_field


def draw_field(screen, field, tile):
    screen.fill((255, 255, 255))
    for q in range(N):
        pygame.draw.line(screen, (0, 0, 0), (tile * q, 0), (tile * q, N * tile))
    for q in range(N):
        pygame.draw.line(screen, (0, 0, 0), (0, tile * q), (N * tile, tile * q))
    for q in range(N):
        for w in range(N):
            if field[q][w] == '':
                pass
            elif field[q][w] == 'S':
                pygame.draw.rect(screen, (0, 0, 255),
                                 pygame.Rect((q * tile + 1, w * tile + 1, tile - 1, tile - 1)))
            elif field[q][w] == 'T':
                pygame.draw.rect(screen, (255, 0, 0),
                                 pygame.Rect((q * tile + 1, w * tile + 1, tile - 1, tile - 1)))
            elif field[q][w] == 'W':
                pygame.draw.rect(screen, (0, 255, 0),
                                 pygame.Rect((q * tile + 1, w * tile + 1, tile - 1, tile - 1)))
    pygame.draw.circle(screen, (0, 0, 0), (N * tile // 2, N * tile // 2), 20)


pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
tile = START_TILE
tick = 0

dx, dy = -N * tile // 2 + WIDTH // 2, -N * tile // 2 + HEIGHT // 2
pause = True

field = [['' for _ in range(N)] for _ in range(N)]

if __name__ == "__main__":
    while True:
        place = pygame.Surface((N * tile, N * tile))
        sc.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause
                elif event.key == pygame.K_BACKSPACE:
                    field = [['' for _ in range(N)] for _ in range(N)]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    tile += 5
                    dx -= N * 5 // 2
                    dy -= N * 5 // 2
                elif event.button == 5:
                    if tile != 5:
                        tile -= 5
                        dx += N * 5 // 2
                        dy += N * 5 // 2
                elif event.button == 1:
                    if field[(event.pos[0] - dx) // tile][(event.pos[1] - dy) // tile] == 'W':
                        field[(event.pos[0] - dx) // tile][(event.pos[1] - dy) // tile] = ''
                    else:
                        field[(event.pos[0] - dx) // tile][(event.pos[1] - dy) // tile] = 'W'
                elif event.button == 3:
                    if field[(event.pos[0] - dx) // tile][(event.pos[1] - dy) // tile] == 'W':
                        field[(event.pos[0] - dx) // tile][(event.pos[1] - dy) // tile] = 'S'
                    elif field[(event.pos[0] - dx) // tile][(event.pos[1] - dy) // tile] == 'S':
                        field[(event.pos[0] - dx) // tile][(event.pos[1] - dy) // tile] = 'W'
                elif event.button == 2:
                    print(n_signals((event.pos[0] - dx) // tile, (event.pos[1] - dy) // tile, field))

        if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_UP]:
            dy += max(tile // 10, 1)
        if pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_DOWN]:
            dy -= max(tile // 10, 1)
        if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
            dx += max(tile // 10, 1)
        if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
            dx -= max(tile // 10, 1)

        if not pause:
            if tick % FPT == 0:
                field = update_field(field)
            tick += 1

        draw_field(place, field, tile)

        sc.blit(place, (dx, dy))

        pygame.display.flip()
        clock.tick(FPS)
