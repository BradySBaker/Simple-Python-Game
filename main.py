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
nextObstacleDistance = 100
nextEnemyDistance = 100

player_grounded = False
projectileTimer = 1

clock = pygame.time.Clock()

highScore = 0


def initialize_game():
    global player_move, player_pos, projectiles, score, prevObstacleX, rectangle_obstacles, dt, enemies, prevEnemyX, projectile_entities, player_speed, start
    dt = 0
    player_move = {'vx': 0, 'vy': 0}
    player_pos = {'x': player.x, 'y': player.y}
    projectiles = []
    projectile_entities = []
    score = 1
    prevEnemyX = player.x
    prevObstacleX = player.x
    rectangle_obstacles = []
    enemies = []
    player_speed = 500
    start = False

def draw_obstacles_floor_player():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), player)
    pygame.draw.rect(screen, (165, 42, 42), floor)
    for rect in rectangle_obstacles:
      rect['pos']['x'] -= player_move['vx'] * dt
      drawnRect = pygame.draw.rect(screen, (255, 0, 255), (round(rect['pos']['x']), round(rect['pos']['y']), 50, rect['height']))
      handle_collision(drawnRect)


def handle_enemies():
    global nextEnemyDistance
    global prevEnemyX

    prevEnemyDist = player_pos['x'] - prevEnemyX
    maxDist = round(1000000/player_speed)
    if (prevEnemyDist > nextEnemyDistance):
      nextEnemyDistance = random.randint(400, maxDist if maxDist > 400 else 401)
      prevEnemyX = player_pos['x']
      enemies.append({'pos': {'x': player.x + width, 'y': height / 2}, 'going_up': False if random.randint(0, 1) == 1 else True})

    for enemy in enemies:
      if (enemy['pos']['x'] < player.x - 100):
          enemies.remove(enemy)
          continue
      if (enemy['pos']['y'] < 100):
          enemy['going_up'] = False
      elif (enemy['pos']['y'] > height/1.5):
          enemy['goingUp'] = True

      if (enemy['going_up']):
          enemy['pos']['y'] -= player_speed/10 * dt
      else:
        enemy['pos']['y'] += player_speed/10 * dt


      enemy['pos']['x'] -= player_move['vx'] * dt
      drawnCircle = pygame.draw.circle(screen, (255, 0, 0), (round(enemy['pos']['x']), round(enemy['pos']['y'])), 30)
      handle_collision(drawnCircle)
      handle_projectile_collision(drawnCircle, enemy)



def move_player():
    global player_speed
    if (player_speed < 1000):
        player_speed += dt * 2
    global player_grounded


    player_move['vx'] = 0

    key = pygame.key.get_pressed()

    if (player_pos['y'] >= floor.y - floor.height - player.height + 50):
        player_move['vy'] = 0
        player_pos['y'] = (floor.y - floor.height - player.height + 50)
        player_grounded = True
    else:
        player_move['vy'] += 3000 * dt
        player_grounded = False

    if (key[pygame.K_s]):
        player.height = 50
    else:
        player.height = 100
    player_move['vx'] = round(player_speed)

    if (key[pygame.K_w] and player_grounded):
        player_move['vy'] = -1000

    player_pos['y'] += player_move['vy'] * dt
    player_pos['x'] += player_move['vx'] * dt

    player.y = round(player_pos['y'])




def handle_projectiles():
    global projectile_entities
    projectile_entities = []
    for projectile in projectiles:
      projectile['pos']['x'] += projectile['velocity']['x']
      projectile['pos']['y'] += projectile['velocity']['y']

      projectile_entities.append(pygame.draw.circle(screen, (255, 0, 0), (round(projectile['pos']['x']), round(projectile['pos']['y'])), 10))

def handle_projectile_collision(enemy_entity, enemy):
    global score
    for index, projectile in enumerate(projectile_entities):
        if (projectile.colliderect(enemy_entity)):
            score += 5
            projectiles.remove(projectiles[index])
            enemies.remove(enemy)



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
    prevObsDist = player_pos['x'] - prevObstacleX
    if (prevObsDist > nextObstacleDistance):
        nextObstacleDistance = random.randint(450, 2000)
        newX = player.x + width + 50
        prevObstacleX = player_pos['x']
        yOffset = 0 if random.randint(0, 1) == 1 else 50
        rectHeight = 50 if random.randint(0, 1) == 1 else 100
        newRect = {'pos': {'x': newX, 'y': height - (50 + yOffset + rectHeight)}, 'height': rectHeight}
        rectangle_obstacles.append(newRect)

def handle_collision(obst_rect):
    global highScore
    if (player.colliderect(obst_rect)):
        if (score > highScore):
            highScore = score
        initialize_game()


def handle_start():
    global start
    font = pygame.font.Font(None, 36)
    text_rendered = font.render('High Score : ' + str(round(highScore)) + '        Press Space to play...', True, (255, 255, 255))
    screen.blit(text_rendered, (width/4, height/4))
    key = pygame.key.get_pressed()
    if (key[pygame.K_SPACE]):
        start = True

def main():
    global dt
    global score

    run = True


    initialize_game()
    while run:
        dt = clock.tick(60) / 1000.0
        if (start == False):
            handle_start()
        else:
            draw_obstacles_floor_player()
            handle_projectiles() #must come before handle_enemies

            move_player()
            handle_shoot()
            handle_random_obstacles()
            handle_enemies()
            score += dt
            font = pygame.font.Font(None, 36)
            text_rendered = font.render('Score: ' + str(round(score)) + '       High Score : ' + str(round(highScore)), True, (255, 255, 255))
            screen.blit(text_rendered, (width - 350, 20))
            font = pygame.font.Font(None, 20)
            text_rendered = font.render('Speed: ' + str(round(player_speed)), True, (255, 255, 255))
            screen.blit(text_rendered, (0, 20))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
