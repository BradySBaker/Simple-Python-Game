import pygame
import math
import random
pygame.init()

# Set up display
width, height = 1080, 500
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("My Game")

player = pygame.Rect((100, 250, 50, 100))
floor = pygame.Rect((0, height - 50, width, 50))
rectangle_obstacles = []
prevObstacleX = player.x
nextObstacleDistance = 100

player_move = {'vx': 0, 'vy': 0}
playerPos = {'x': player.x, 'y': player.y} #player position only allows integer movement
player_grounded = False
projectileTimer = 1
projectiles = []

dt = 0
clock = pygame.time.Clock()


run = True



def draw_rectangles():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), player)
    pygame.draw.rect(screen, (255, 0, 0), floor)
    for rect in rectangle_obstacles:
      rect['pos']['x'] -= player_move['vx'] * dt
      drawnRect = pygame.draw.rect(screen, (255, 0, 0), (round(rect['pos']['x']), round(rect['pos']['y']), 50, rect['height']))
      handle_collision(drawnRect)




def move_player():
    global player_grounded
    player_move['vx'] = 0

    if (playerPos['y'] >= floor.y - floor.height - player.height + 50):
        player_move['vy'] = 0
        playerPos['y'] = (floor.y - floor.height - player.height + 50)
        player_grounded = True
    else:
        player_move['vy'] += 3000 * dt
        player_grounded = False

    if (key[pygame.K_s]):
        player.height = 50
    else:
        player.height = 100

    player_move['vx'] = 1000

    if (key[pygame.K_w] and player_grounded):
        player_move['vy'] = -1000

    playerPos['y'] += player_move['vy'] * dt
    playerPos['x'] += player_move['vx'] * dt

    player.y = round(playerPos['y'])




def handle_projectiles():
    for projectile in projectiles:
      projectile['pos']['x'] += projectile['velocity']['x']
      projectile['pos']['y'] += projectile['velocity']['y']

      pygame.draw.circle(screen, (255, 0, 0), (round(projectile['pos']['x']), round(projectile['pos']['y'])), 10)




def handle_shoot():
    global projectileTimer
    mouse_x, mouse_y = pygame.mouse.get_pos()

    direction_x = mouse_x - player.x
    direction_y = mouse_y - player.y

    length = math.sqrt(direction_x**2 + direction_y**2)

    if length != 0:
        direction_x /= length
        direction_y /= length

    launchSpeed = 30

    if (pygame.mouse.get_pressed()[0] and projectileTimer > .5):
      projectile = {'pos': {'x': player.x + player.width, 'y': player.y + player.height/4}, 'velocity': {'x': direction_x * launchSpeed, 'y': direction_y * launchSpeed}}
      projectiles.append(projectile)
      projectileTimer = 0
    projectileTimer += 1 * dt


def handle_random_obstacles():
    global nextObstacleDistance
    global prevObstacleX
    prevObsDist = playerPos['x'] - prevObstacleX
    if (prevObsDist > nextObstacleDistance):
        nextObstacleDistance = random.randint(800, 2000)
        newX = player.x + width + 50
        prevObstacleX = playerPos['x']
        yOffset = 0 if random.randint(0, 1) == 1 else 50
        rectHeight = 50 if random.randint(0, 1) == 1 else 100
        newRect = {'pos': {'x': newX, 'y': height - (50 + yOffset + rectHeight)}, 'height': rectHeight}
        rectangle_obstacles.append(newRect)

def handle_collision(obst_rect):
    global run
    if (player.colliderect(obst_rect)):
        run = False

while run:
    dt = clock.tick(60) / 1000.0
    draw_rectangles()
    handle_projectiles()
    key = pygame.key.get_pressed()

    move_player()
    handle_shoot()
    handle_random_obstacles()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()