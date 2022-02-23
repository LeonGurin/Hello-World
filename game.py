import pygame
import random
import os
import sys
import time

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN,    
    RLEACCEL,
)

pygame.init()

# fixed python 32-bit bug ✔
# add start screen ✔
# fix berry bug ❌
# add score bar and timer 🤷‍♂️
# add sound
# add game over
# add high score
# add pause

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
FPS = 60

# init screen and clock
pygame.display.set_caption('Clicky Bicky Game')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# init background
class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.dirname(__file__) + "\\sky3.jpg").convert()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.y2 = self.rect.height
    def update(self):
        self.y -= 2
        self.y2 -= 2
        if self.y <= -self.rect.height:
            self.y = self.rect.height
        if self.y2 <= -self.rect.height:
            self.y2 = self.rect.height
    def render(self):
        screen.blit(self.image, (self.x, self.y))
        screen.blit(self.image, (self.x, self.y2))

# create a start button
class StartButton(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super(StartButton, self).__init__()
        self.image = pygame.image.load(os.path.dirname(__file__) + "\\start.png").convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.image = pygame.transform.scale(self.image, (200, 100))
        self.rect = self.image.get_rect()
        self.posX = SCREEN_WIDTH / 2 - self.rect.width / 2
        self.posY = SCREEN_HEIGHT / 2 - self.rect.height / 2
    def is_clicked(self,x,y):
        if x > self.posX and x < self.posX + self.rect.width:
            if y > self.posY and y < self.posY + self.rect.height:
                # self.surf.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                return True
        return False
    def render(self):
        # render the button at the center of the screen
        screen.blit(self.image, (self.posX, self.posY))

class Title:
    def __init__(self):
        self.font = pygame.font.Font('freesansbold.ttf', 35)
        self.text = self.font.render('Clicky Bicky Game', True, (0,255,0), (0,0,255))
        self.rect = self.text.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200)
    def render(self):
        screen.blit(self.text, self.rect)

class UI(pygame.sprite.Sprite):
    def __init__(self):
        super(UI, self).__init__()
        self.surf = pygame.image.load(os.path.dirname(__file__) + "\\uiBar2.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (SCREEN_WIDTH+36, 600))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        #self.rect.center = (SCREEN_WIDTH // 2, 222)

    def render(self):
        screen.blit(self.surf, (-15, 0))

class ClockText:
    def __init__(self):
        self.font = pygame.font.Font(None, 50)
        self.current_time = time.time()
        self.s = 0
        self.m = 0
        self.text = self.font.render("0:00", True, (255, 255, 255))
        # self.text = self.font.render(str(self.m) + ':' + str(self.s), True, (255, 255, 255))
        self.rect = self.text.get_rect()
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT // 2 - 200)
    def update(self):
        if time.time() - self.current_time >= 1:
            self.current_time = time.time()
            self.s += 1
            if self.s == 60:
                self.s = 0
                self.m += 1
        self.text = self.font.render(str(self.m) + ':' + str(self.s), True, (255, 255, 255))
    
    def render(self):
        if self.s < 10:
            self.text = self.font.render(str(self.m) + ':0' + str(self.s), True, (255, 255, 255))
        else:
            self.text = self.font.render(str(self.m) + ':' + str(self.s), True, (255, 255, 255))
        screen.blit(self.text, self.rect)

# fruit object
class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        super(Fruit, self).__init__()
        self.surf = pygame.image.load(os.path.dirname(__file__) + "\\Strawberry.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.posX = SCREEN_WIDTH / 2 - self.rect.width / 2
        self.posY = SCREEN_HEIGHT / 2 - self.rect.height / 2
        self.tempX = self.posX
        self.tempY = self.posY
    def is_clicked(self,x,y):
        if x > self.posX and x < self.posX + self.rect.width:
            if y > self.posY and y < self.posY + self.rect.height:
                # self.surf.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                while self.tempX >= self.posX and self.tempX <= self.posX + self.rect.width:
                    self.tempX = random.randint(0, SCREEN_WIDTH - self.rect.width)
                    self.tempY = random.randint(100, SCREEN_HEIGHT - self.rect.height)
                self.posX = self.tempX
                self.posY = self.tempY
    def render(self):
        screen.blit(self.surf, (self.posX, self.posY))

#-------------------#
#  code starts here
#-------------------#

# init objects
bg = Background()
st = StartButton()

(x,y) = pygame.mouse.get_pos()
# start menu
while st.is_clicked(x,y) == False:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    if event.type == MOUSEBUTTONDOWN:
        (x,y) = pygame.mouse.get_pos()
        st.is_clicked(x,y)
    bg.render()
    bg.update()
    st.render()
    pygame.display.update()
    clock.tick(FPS)

# delay
time.sleep(.1)
# game loop
fr = Fruit()
tt = Title()
cl = ClockText()
ui = UI()

running = True
while running:    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    #if the mouse is clicked
    if event.type == MOUSEBUTTONDOWN:
        (x,y) = pygame.mouse.get_pos()
        fr.is_clicked(x,y)
    
    bg.update()
    bg.render()
    fr.render()
    # tt.render()
    ui.render()
    cl.update()
    cl.render()
    pygame.display.update()
    clock.tick(FPS)
    
pygame.quit()
sys.exit()
