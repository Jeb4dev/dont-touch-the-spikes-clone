import pygame
import random
from menu import MainMenu, OptionsMenu, CreditsMenu


def is_collision(object_x, object_y, player_x, player_y):
    if (((object_x + 60 - player_x + 16) < 108 and (object_x + 60 - player_x + 16)) > 14) and \
            (14 < (object_y + 60 - player_y + 16)) and ((object_y + 60 - player_y + 16) < 108):
        return True


class Game:
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.SPACE_KEY = False, False, False, False, False
        self.alive, self.dead = False, False
        self.DISPLAY_W, self.DISPLAY_H = 600, 800
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.killerPlaced, self.candyGot = False, True

        # Background
        self.background = pygame.image.load('assets/background_color.jpg')

        # Player
        self.playerImg = [pygame.image.load('assets/ufo.png'), pygame.image.load('assets/ufo.png'), pygame.image.load(
            'assets/ufo.png')]
        self.playerX, self.playerY = 10, 400
        self.playerX_change, self.playerY_change = 0, 0

        # Killer
        self.killerIMG = []
        self.killerX1, self.killerX2, self.killerY, self.killerYY = [], [], [], []
        self.killerVX, self.killerVY = [], []
        for i in range(1, 11):
            self.killerYY.append(64 + 67*i)
            self.killerY.append(64 + 67*i)
        for i in range(10):
            self.killerX2.append(0)
            self.killerX1.append(536)

        for i in range(20):
            self.killerIMG.append(pygame.image.load('assets/Minecraft-Lava.jpg'))
        for i in range(10):
            self.killerVY.append(750)
            self.killerVY.append(0)
            self.killerVX.append(i * 64)
            self.killerVX.append(i * 64)

        # Candy
        self.candyIMG = [pygame.image.load('assets/candy1.png'), pygame.image.load('assets/candy2.png'),
                         pygame.image.load('assets/candy3.png')]
        self.candyX, self.candyY, self.candyN = 0, 0, 0
        f = open("candy_value.txt", "r")
        self.candyV = int(f.readline())
        f.close()

        # Score
        self.scoreV = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)

        # Game Over
        self.gg_font = pygame.font.Font('freesansbold.ttf', 64)

        # Clock
        self.clock = pygame.time.Clock()

    def show_score(self, x, y, score, score_name):
        print_score = self.font.render(f"{score_name}: " + str(score), True, (255, 255, 255))
        self.window.blit(print_score, (x, y))

    def show_game_over_txt(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.window.blit(text_surface, text_rect)

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_SPACE:
                    self.SPACE_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.SPACE_KEY = False, False, False, False, False

    def draw_object(self, x, y, i, img):
        self.window.blit(img[i], (x, y))

    def game_loop(self):
        while self.playing:
            self.check_events()

            # Background
            self.window.blit(self.background, (0, 0))

            if self.START_KEY:
                self.playing = False
                self.alive = False
                self.playerY_change, self.playerX_change = 0, 0
                self.playerY, self.playerX = 400, 10
                self.killerPlaced = False
                # self.killerY, self.killerX1, self.killerX2 = 0, 0, 0
                self.candyGot = True

            # First space key down / start
            if self.SPACE_KEY and not self.alive:
                self.alive, self.dead = True, False
                self.scoreV, self.candyN = 0, 0
                self.playerY_change = 0
                self.playerX_change = 5

            # Jump
            if self.SPACE_KEY and not self.dead:
                self.playerY_change = -7

            # Borders
            if self.playerX <= 0 and self.alive and not self.dead:
                self.playerX_change = 5
                self.scoreV += 1
                self.killerPlaced = False
            elif self.playerX >= 564 and self.alive and not self.dead:
                self.playerX_change = -5
                self.scoreV += 1
                self.killerPlaced = False
            if self.playerY <= 64:
                self.dead = True
                self.playerY = 64
                self.playerY_change = 0
            elif self.playerY >= 736:
                self.dead = True
                self.playerY = 736

            # stop movement when dead
            if self.dead:
                f = open("candy_value.txt", "w")
                f.write(str(self.candyV))
                f.close()
                self.show_game_over_txt("Game Over", 50, self.DISPLAY_W / 2, self.DISPLAY_H / 2)
                self.show_game_over_txt("Press [Enter] to continue", 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2+50)
                while self.playerX_change*self.playerX_change != 0:
                    if self.playerX_change < 0:
                        self.playerX_change += 0.05
                    if self.playerX_change > 0:
                        self.playerX_change -= 0.05
                    if self.playerX_change*self.playerX_change < 0.1:
                        self.playerX_change = 0
                    if self.playerY > 800:
                        self.playerY_change = 0

            # Going down, gravity
            if self.alive:
                self.playerY_change += 0.2

            # Player movement
            self.playerY += self.playerY_change
            self.playerX += self.playerX_change

            if int(2 + 0.2 * self.scoreV) > 9:
                value = 10
            else:
                value = int(2 + 0.2 * self.scoreV)

            l1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            if self.scoreV % 2 == 0 and not self.killerPlaced:
                for i in range(value):
                    x = random.randint(0, len(l1) - 1)
                    a = int(l1.pop(x))
                    self.killerPlaced = True
                    self.killerX1[i] = self.killerX1[i]
                    self.killerY[i] = self.killerYY[a]
                    # pygame.Surface.fill(enemyImg[i], color="red")

            elif self.scoreV % 2 == 1 and not self.killerPlaced:
                for i in range(value):
                    x = random.randint(0, len(l1) - 1)
                    a = int(l1.pop(x))
                    self.killerPlaced = True
                    self.killerX1[i] = self.killerX1[i]
                    self.killerY[i] = self.killerYY[a]
                    # pygame.Surface.fill(enemyImg[i], color="red")
            for i in range(value):
                if self.scoreV % 2 == 0:
                    self.draw_object(self.killerX1[i], self.killerY[i], i, self.killerIMG)
                    collision = is_collision(self.killerX1[i], self.killerY[i], self.playerX, self.playerY)
                    if collision:
                        self.dead = True

                elif self.scoreV % 2 == 1:
                    self.draw_object(self.killerX2[i], self.killerY[i], i, self.killerIMG)
                    collision = is_collision(self.killerX2[i], self.killerY[i], self.playerX, self.playerY)
                    if collision:
                        self.dead = True
            # candy movement and drawing
            if self.candyGot:
                self.candyX, self.candyY = random.randint(65, 450), random.randint(100, 650)

                if self.scoreV > 31:
                    self.candyN = 2
                elif self.candyN > 15:
                    self.candyN = 1
                else:
                    self.candyN = 0
                self.candyGot = False
            else:
                self.draw_object(self.candyX, self.candyY, 0, self.candyIMG)

            # Candy collision
            collision = is_collision(self.candyX, self.candyY, self.playerX, self.playerY)
            if collision:
                self.candyGot = True
                self.candyV += self.candyN + 1

            # Upper and Lower lava
            for i in range(20):
                self.draw_object(self.killerVX[i], self.killerVY[i], i, self.killerIMG)

            # Draw player and decide direction
            if self.playerX_change < 0:  # going left
                self.draw_object(self.playerX, self.playerY, 0, self.playerImg)
            elif not self.alive:
                self.draw_object(self.playerX, self.playerY, 2, self.playerImg)
            else:  # going right
                self.draw_object(self.playerX, self.playerY, 1, self.playerImg)

            self.show_score(10, 10, self.scoreV, "Score")
            self.show_score(350, 10, self.candyV, "Candies")
            self.clock.tick(60)
            pygame.display.update()
            self.reset_keys()
