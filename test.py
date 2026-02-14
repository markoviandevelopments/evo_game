# visualize_sim.py
import pygame
import sys
import random
import math
from lib_evo import Environment, TILE_COUNT_WIDTH, TILE_COUNT_HEIGHT

# ────────────────────────────────────────────────
# CONFIG
# ────────────────────────────────────────────────
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 700
TILE_SIZE = WINDOW_HEIGHT // max(TILE_COUNT_WIDTH, TILE_COUNT_HEIGHT)

LEFT_WIDTH = WINDOW_HEIGHT          # square grid on left
RIGHT_WIDTH = WINDOW_WIDTH - LEFT_WIDTH

AGENT_BASE_RADIUS = 9
FPS = 45

COLOR_BG        = (12, 14, 22)
COLOR_GRID      = (30, 35, 50)
COLOR_FOOD_LOW  = (30, 50, 30)
COLOR_FOOD_HIGH = (100, 220, 80)
COLOR_AGENT     = (240, 170, 60)
COLOR_TEXT      = (180, 190, 220)
COLOR_PLOT_BG   = (18, 20, 28)
COLOR_PLOT_GRID = (50, 55, 70)
COLOR_PLOT_AXIS = (100, 110, 130)

POPULATION = 75
INITIAL_SPEED = 0.006

PLOT_MARGIN = 60          # space for labels/axes
PLOT_X_MAX = 0.015        # adjust if agents get much faster
PLOT_Y_MAX = 5.0          # food upper limit for plot (adjust as needed)

# ────────────────────────────────────────────────
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hungry Grokking Agents – Grid + Food vs Speed")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 14)
font_small = pygame.font.SysFont("arial", 11)

# Setup simulation
env = Environment()
env.initialize_pop(POPULATION)

# Give agents random movement
for agent in env.agents:
    agent.x_v = random.uniform(-INITIAL_SPEED, INITIAL_SPEED)
    agent.y_v = random.uniform(-INITIAL_SPEED, INITIAL_SPEED)

print(f"Simulation started – {POPULATION} agents, {TILE_COUNT_WIDTH}×{TILE_COUNT_HEIGHT} food grid")
print("Press B = bark | SPACE = pause | ESC = quit\n")

paused = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_b:
                for a in env.agents:
                    a.bark()
                print("───")
            elif event.key == pygame.K_SPACE:
                paused = not paused
                print("PAUSED" if paused else "RUNNING")

    if not paused:
        env.iterate_physics()

    # ─── DRAW ────────────────────────────────────────
    screen.fill(COLOR_BG)

    # ── LEFT: Grid view ──────────────────────────────
    grid_rect = pygame.Rect(0, 0, LEFT_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(screen, COLOR_BG, grid_rect)

    # Food tiles
    for tx in range(TILE_COUNT_WIDTH):
        for ty in range(TILE_COUNT_HEIGHT):
            food_val = min(1.0, env.tiles[tx][ty])
            intensity = int(40 + food_val * 180)
            color = (
                min(255, intensity // 2),
                min(255, intensity + 40),
                min(255, intensity // 3)
            )
            rect = pygame.Rect(tx * TILE_SIZE, ty * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, COLOR_GRID, rect, 1)

    # Agents on grid
    for agent in env.agents:
        px = int(agent.x * LEFT_WIDTH)
        py = int(agent.y * WINDOW_HEIGHT)
        radius = max(6, min(18, int(AGENT_BASE_RADIUS + (agent.food - 0.5) * 6)))
        r = 240 if agent.food > 0.4 else min(255, 240 + int((0.4 - agent.food) * 300))
        g = 170 if agent.food > 0.4 else 60
        b = 60 if agent.food > 0.4 else 40
        color = (r, g, b)
        pygame.draw.circle(screen, color, (px, py), radius)

    # ── RIGHT: Scatter plot (Food vs Speed) ──────────
    plot_area = pygame.Rect(LEFT_WIDTH, 0, RIGHT_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(screen, COLOR_PLOT_BG, plot_area)

    # Plot axes
    pygame.draw.line(screen, COLOR_PLOT_AXIS,
                     (LEFT_WIDTH + PLOT_MARGIN, WINDOW_HEIGHT - PLOT_MARGIN),
                     (WINDOW_WIDTH - PLOT_MARGIN, WINDOW_HEIGHT - PLOT_MARGIN), 2)   # x-axis
    pygame.draw.line(screen, COLOR_PLOT_AXIS,
                     (LEFT_WIDTH + PLOT_MARGIN, WINDOW_HEIGHT - PLOT_MARGIN),
                     (LEFT_WIDTH + PLOT_MARGIN, PLOT_MARGIN), 2)                     # y-axis

    # Labels
    x_label = font_small.render("Speed (magnitude)", True, COLOR_TEXT)
    y_label = font_small.render("Food", True, COLOR_TEXT)
    screen.blit(x_label, (WINDOW_WIDTH - 120, WINDOW_HEIGHT - 35))
    y_label_rot = pygame.transform.rotate(y_label, 90)
    screen.blit(y_label_rot, (LEFT_WIDTH + 8, WINDOW_HEIGHT // 2 - 20))

    # Light grid lines in plot
    for i in range(6):
        x = LEFT_WIDTH + PLOT_MARGIN + i * (RIGHT_WIDTH - 2*PLOT_MARGIN)/5
        pygame.draw.line(screen, COLOR_PLOT_GRID, (x, PLOT_MARGIN), (x, WINDOW_HEIGHT - PLOT_MARGIN), 1)
    for i in range(6):
        y = WINDOW_HEIGHT - PLOT_MARGIN - i * (WINDOW_HEIGHT - 2*PLOT_MARGIN)/5
        pygame.draw.line(screen, COLOR_PLOT_GRID, (LEFT_WIDTH + PLOT_MARGIN, y), (WINDOW_WIDTH - PLOT_MARGIN, y), 1)

    # Plot points
    for agent in env.agents:
        speed = math.sqrt(agent.x_v**2 + agent.y_v**2)
        food = agent.food

        plot_x = LEFT_WIDTH + PLOT_MARGIN + (speed / PLOT_X_MAX) * (RIGHT_WIDTH - 2*PLOT_MARGIN)
        plot_y = (WINDOW_HEIGHT - PLOT_MARGIN) - (food / PLOT_Y_MAX) * (WINDOW_HEIGHT - 2*PLOT_MARGIN)

        # Clamp to plot area
        plot_x = max(LEFT_WIDTH + PLOT_MARGIN, min(WINDOW_WIDTH - PLOT_MARGIN, plot_x))
        plot_y = max(PLOT_MARGIN, min(WINDOW_HEIGHT - PLOT_MARGIN, plot_y))

        r = 240 if food > 0.4 else min(255, 240 + int((0.4 - food) * 300))
        g = 170 if food > 0.4 else 60
        b = 60 if food > 0.4 else 40
        color = (r, g, b)

        pygame.draw.circle(screen, color, (int(plot_x), int(plot_y)), 5)

    # HUD (bottom left-ish)
    avg_food = sum(sum(row) for row in env.tiles) / (TILE_COUNT_WIDTH * TILE_COUNT_HEIGHT)
    status = font.render(
        f"Time: {env.time:>5}   Agents: {len(env.agents)}   "
        f"Avg food/tile: {avg_food:.2f}   "
        f"[SPACE=pause] [B=bark]",
        True, COLOR_TEXT
    )
    screen.blit(status, (10, WINDOW_HEIGHT - 28))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()