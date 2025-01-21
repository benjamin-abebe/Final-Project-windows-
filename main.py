import math # we used this library because its important to calculate the amount of damage that the spaceship takes during collision and to count the score. 
import random # to make the enemies pop-up on a random x-axis and y-axis
import serial # to establish connection from the computer to the micro:bit
import time # we used this library to make the bullet shoot every 1-2 seconds automatically
import pygame # the framework that we used to make this game 
from pygame import mixer # used specifically for the background and the background music that will be avaliable throughout the game play and on the main menu. 

# initialize pygame
pygame.init()

# set up the screen
screen = pygame.display.set_mode((900, 600))

# background
background = pygame.image.load('background_20.png')

# sound
mixer.music.load("background.ogg")
mixer.music.play(-1)

# title of the game and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# fonts
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)

# button class
class Button:
    def __init__(self, text, x, y, enabled=True):
        self.text = text
        self.x = x
        self.y = y
        self.enabled = enabled
        self.width = 200
        self.height = 50

    def draw(self, screen):
        color = 'dark gray' if self.check_hover() else 'light gray'
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, 'black', (self.x, self.y, self.width, self.height), 2, border_radius=10)
        text_surface = font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.x + (self.width - text_surface.get_width()) // 2, self.y + (self.height - text_surface.get_height()) // 2))

    def check_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        return pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(mouse_pos)

    def check_click(self):
        return self.check_hover() and pygame.mouse.get_pressed()[0]

# health Bar(spaceship)
class HealthBar:
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.width * ratio, self.height))

# score
def show_score(x, y, score):
    score_text = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (250, 250))

def game_loop():
    playerImg = pygame.image.load('player.20.png')
    playerX, playerY = 370, 480
    playerX_change = 0

    enemyImg = [pygame.image.load('Final-Boss.png') for _ in range(6)]
    enemyX = [random.randint(0, 736) for _ in range(6)]
    enemyY = [random.randint(50, 150) for _ in range(6)]
    enemyY_change = [4 for _ in range(6)]

    bulletImg = pygame.image.load('fire.png')
    bullets = []
    bullet_speed = 10
    bullet_interval = 2
    last_bullet_time = time.time()

    score_value = 0
    health_bar = HealthBar(10, 50, 200, 20, 100)

    explosionSound = mixer.Sound("explosion.wav")

    # establishing connection with the micro:bit (via USB cable)
    try:
        microbit = serial.Serial('/dev/ttyACM0', 115200, timeout=1) 
        time.sleep(2) 
        microbit_connected = True
    except serial.SerialException as e:
        print(f"Micro:bit connection failed: {e}")
        microbit_connected = False

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

        # positioning the bullet at the center of the spaceship
    def fire_bullet(x, y):
        bullet_x = x + (playerImg.get_width() - bulletImg.get_width()) // 2
        bullets.append({"x": bullet_x, "y": y})

    def update_bullets():
        for bullet in bullets[:]:
            bullet["y"] -= bullet_speed
            if bullet["y"] < 0:
                bullets.remove(bullet)

    # bullets
    def draw_bullets():
        for bullet in bullets:
            screen.blit(bulletImg, (bullet["x"], bullet["y"]))

    # enemy collision with the bullet
    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((enemyX - bulletX)**2 + (enemyY - bulletY)**2)
        return distance < 27

    # enemy collision with the player
    def player_collision(enemyX, enemyY, playerX, playerY):
        distance = math.sqrt((enemyX - playerX)**2 + (enemyY - playerY)**2)
        return distance < 27

    # loop while True (Infinite loop)
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if microbit_connected:
            # recieve commands from the micro:bit to control the movement of the spaceship
            command = microbit.readline().decode('utf-8').strip() if microbit.in_waiting > 0 else None
            if command == "left":
                playerX_change = -5
            elif command == "right":
                playerX_change = 5
            elif command == "stop":
                playerX_change = 0

        playerX += playerX_change
        playerX = max(0, min(736, playerX))

        current_time = time.time()
        if current_time - last_bullet_time >= bullet_interval:
            fire_bullet(playerX, playerY)
            last_bullet_time = current_time

        update_bullets()

        for i in range(len(enemyImg)):
            enemyY[i] += enemyY_change[i]

            if player_collision(enemyX[i], enemyY[i], playerX, playerY):
                health_bar.hp -= 10
                enemyY[i] = random.randint(-100, -40)
                enemyX[i] = random.randint(0, 736)
                if health_bar.hp <= 0:
                    running = False

            for bullet in bullets:
                if isCollision(enemyX[i], enemyY[i], bullet["x"], bullet["y"]):
                    explosionSound.play()
                    bullets.remove(bullet)
                    score_value += 1
                    enemyY[i] = random.randint(-100, -40)
                    enemyX[i] = random.randint(0, 736)

            if enemyY[i] > 600:
                enemyY[i] = random.randint(-100, -40)
                enemyX[i] = random.randint(0, 736)

            enemy(enemyX[i], enemyY[i], i)

        draw_bullets()
        health_bar.draw(screen)
        player(playerX, playerY)
        show_score(10, 10, score_value)
        pygame.display.update()

    game_over_text()
    pygame.display.update()
    time.sleep(3)

def main_menu():
    start_button = Button("Start Game", 400, 200)
    quit_button = Button("Quit", 400, 300)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        start_button.draw(screen)
        quit_button.draw(screen)

        if start_button.check_click():
            game_loop()
        if quit_button.check_click():
            pygame.quit()
            exit()

        pygame.display.update()

main_menu()
