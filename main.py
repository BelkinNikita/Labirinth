import pygame
import random
from map import *
import tkinter as tk

pygame.init()
width = 800
height = 800
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 0))
pygame.display.set_caption('Labirinth by @BelkinNikita')
clock = pygame.time.Clock()
distance_of_move = None
x_Player = None
y_Player = None
last_move_time = None
last_direction = None
npc_velocity = None
TimeOfRespawn_neutral = 0
score = 0
string_score =('score: %s' % score)
amout_red = 7
amout_yellow = 5
amout_green = 0
time = 0
endgame_string = None

running = True

directions_list = ['Top', 'Right', 'Left', 'Bottom']
wall_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
neutral_group = pygame.sprite.Group()
defender_group = pygame.sprite.Group()

font_spawn = pygame.font.Font(None, 20)
surface_text_spawn_red = font_spawn.render('*', True, ('Red'))
surface_text_spawn_yellow = font_spawn.render('*', True, ('yellow'))
surface_text_spawn_green = font_spawn.render('*', True, ('green'))


font_score = pygame.font.Font(None, 50)
surface_text_score = font_score.render(string_score, True, ('green'))
surface_score = pygame.Surface((190, 90))
surface_score_invisible = pygame.Surface((190, 140))
surface_score.fill('Blue')

class Level:
    def __init__(self):
        global distance_of_move, x_Player, y_Player, last_move_time, last_direction, npc_velocity
        distance_of_move = 25
        x_Player, y_Player = 357, 407
        last_move_time = 0
        last_direction = 0
        npc_velocity = 0

    def map():
        x = 0
        y = 0
        row = 0
        for i in map:
            if row == 16:
                row = 0
                x -= 800
                y += 50
                if i == 1:
                    wall_group.add(Wall(x, y))
                    x += 50
                    row += 1
                else:
                    x += 50
                    row += 1
            else:
                if i == 1:
                    wall_group.add(Wall(x, y))
                    x += 50
                    row += 1
                else:
                    x += 50
                    row += 1


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((36, 35))
        self.image.fill('White')
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update():
        global x_Player, y_Player, last_move_time, collision_playerwall, last_direction, height, width
        if last_move_time > 10:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                y_Player -= distance_of_move
                last_direction = 0
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                y_Player += distance_of_move
                last_direction = 1
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                x_Player -= distance_of_move
                last_direction = 2
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                x_Player += distance_of_move
                last_direction = 3
            last_move_time = 0
            if x_Player > width: x_Player = x_Player - height - 25
            elif x_Player < -25: x_Player = x_Player + height + 25
            elif y_Player < -25: y_Player = y_Player + height + 25
            elif y_Player > height: y_Player = y_Player - height - 25


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill('Red')
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction_choice = 'Bottom'


    def direction(self):
        if self.direction_choice == 'Bottom': self.rect.y -= distance_of_move * 2
        elif self.direction_choice == 'Top': self.rect.y += distance_of_move * 2
        elif self.direction_choice == 'Left': self.rect.x += distance_of_move * 2
        elif self.direction_choice == 'Right': self.rect.x -= distance_of_move * 2
        self.direction_choice = random.choice(directions_list)

    def update(self):
        self.collision = pygame.sprite.spritecollideany(self, wall_group)
        if self.direction_choice == 'Bottom': self.rect.y += distance_of_move
        elif self.direction_choice == 'Top': self.rect.y -= distance_of_move
        elif self.direction_choice == 'Left': self.rect.x -= distance_of_move
        elif self.direction_choice == 'Right': self.rect.x += distance_of_move
        if  self.collision:
            Enemy.direction(self)
        if self.rect.x > width:
            self.rect.x = self.rect.x - height - 25
        elif self.rect.x < -25:
            self.rect.x = self.rect.x + height + 25
        elif self.rect.y < -25:
            self.rect.y = self.rect.y + height + 25
        elif self.rect.y > height:
            self.rect.y = self.rect.y - height - 25

    def spawn():
        global amout_red
        spawnplace = [Enemy(55, 455), Enemy(605, 305)]
        enemy_group.add(random.choice(spawnplace))
        amout_red += 1


class Defender(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill('Darkgreen')
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction_choice = 'Bottom'


    def direction(self):
        if self.direction_choice == 'Bottom': self.rect.y -= distance_of_move * 2
        elif self.direction_choice == 'Top': self.rect.y += distance_of_move * 2
        elif self.direction_choice == 'Left': self.rect.x += distance_of_move * 2
        elif self.direction_choice == 'Right': self.rect.x -= distance_of_move * 2
        self.direction_choice = random.choice(directions_list)

    def update(self):
        self.collision = pygame.sprite.spritecollideany(self, wall_group)
        if self.direction_choice == 'Bottom': self.rect.y += distance_of_move
        elif self.direction_choice == 'Top': self.rect.y -= distance_of_move
        elif self.direction_choice == 'Left': self.rect.x -= distance_of_move
        elif self.direction_choice == 'Right': self.rect.x += distance_of_move
        if  self.collision:
            Defender.direction(self)
        if self.rect.x > width:
            self.rect.x = self.rect.x - height - 25
        elif self.rect.x < -25:
            self.rect.x = self.rect.x + height + 25
        elif self.rect.y < -25:
            self.rect.y = self.rect.y + height + 25
        elif self.rect.y > height:
            self.rect.y = self.rect.y - height - 25

    def spawn():
        global score, amout_green
        if score >= 40:
            defender_group.add(Defender(655, 405))
            score = 0
            amout_green += 1


class Neutral(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((36, 35))
        self.image.fill('Yellow')
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction_choice = 'Bottom'


    def direction(self):
        if self.direction_choice == 'Bottom': self.rect.y -= distance_of_move * 2
        elif self.direction_choice == 'Top': self.rect.y += distance_of_move * 2
        elif self.direction_choice == 'Left': self.rect.x += distance_of_move * 2
        elif self.direction_choice == 'Right': self.rect.x -= distance_of_move * 2
        self.direction_choice = random.choice(directions_list)

    def update(self):
        self.collision = pygame.sprite.spritecollideany(self, wall_group)
        if self.direction_choice == 'Bottom': self.rect.y += distance_of_move
        elif self.direction_choice == 'Top': self.rect.y -= distance_of_move
        elif self.direction_choice == 'Left': self.rect.x -= distance_of_move
        elif self.direction_choice == 'Right': self.rect.x += distance_of_move
        if  self.collision:
            Neutral.direction(self)
        if self.rect.x > width:
            self.rect.x = self.rect.x - height - 25
        elif self.rect.x < -25:
            self.rect.x = self.rect.x + height + 25
        elif self.rect.y < -25:
            self.rect.y = self.rect.y + height + 25
        elif self.rect.y > height:
            self.rect.y = self.rect.y - height - 25

    def spawn():
        global TimeOfRespawn_neutral, amout_yellow
        spawnplace = [Neutral(207, 7), Neutral(7, 257), Neutral(757, 257), Neutral(7, 607), Neutral(757, 607)]
        if TimeOfRespawn_neutral > 150:
            neutral_group.add(random.choice(spawnplace))
            TimeOfRespawn_neutral = 0
            amout_yellow += 1
        else:
            TimeOfRespawn_neutral += 1


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill('Blue')
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def lines():
    x_line = 50
    y_line = 50

    for i in range(16):
        pygame.draw.line(screen, 'grey', (0, x_line), (width, x_line))
        x_line += 50

    for i in range(16):
        pygame.draw.line(screen, 'grey', (y_line, 0), (y_line, height))
        y_line += 50

def colliision():
    global collision_playerwall, collision_playerenemy, collision_neutralenemy, collision_playerneutral, collision_playerdefender,\
        collision_neutraldefender, collision_enemydefender, y_Player, x_Player, distance_of_move, running, score, amout_red, endgame_string
    collision_playerwall = pygame.sprite.groupcollide(player_group, wall_group, False, False)
    collision_playerenemy = pygame.sprite.groupcollide(player_group, enemy_group, False, False)
    collision_neutralenemy = pygame.sprite.groupcollide(neutral_group, enemy_group, True, False)
    collision_playerneutral = pygame.sprite.groupcollide(player_group, neutral_group, False, True)
    collision_playerdefender = pygame.sprite.groupcollide(player_group, defender_group, False, False)
    collision_neutraldefender = pygame.sprite.groupcollide(neutral_group, defender_group, True, False)
    collision_enemydefender = pygame.sprite.groupcollide(enemy_group, defender_group, True, False)
    if collision_playerwall:
        if last_direction == 0: y_Player += distance_of_move
        if last_direction == 1: y_Player -= distance_of_move
        if last_direction == 2: x_Player += distance_of_move
        if last_direction == 3: x_Player -= distance_of_move
    if collision_playerenemy or collision_playerdefender:
        running = False
    if collision_neutralenemy:
        Enemy.spawn()
    if collision_playerneutral or collision_neutraldefender or collision_enemydefender:
        score += 1


Level()
Level.map()
enemy_group.add(Enemy(705, 55))
enemy_group.add(Enemy(155, 705))
enemy_group.add(Enemy(255, 155))
enemy_group.add(Enemy(105, 355))
enemy_group.add(Enemy(655, 705))
enemy_group.add(Enemy(55, 105))
enemy_group.add(Enemy(355, 105))
neutral_group.add(Neutral(357, 707))
neutral_group.add(Neutral(157, 257))
neutral_group.add(Neutral(457, 57))
neutral_group.add(Neutral(407, 257))
neutral_group.add(Neutral(257, 507))


def endgame_window():
    window = tk.Tk()
    window.geometry('600x450')
    window.title('Labirinth by @BelkinNikita')
    window.eval('tk::PlaceWindow . center')
    lose_message = tk.Label(window, text=endgame_string, font=("Arial", 14))
    lose_message.pack(padx=100, pady=30)
    score_message = tk.Label(window,
                             text='score: {} yellow boxes \n      '
                                  '{} red boxes\n          '
                                  '{} green boxes\n \n \n '
                                  'play time: {} minuts and {} seconds'
                             .format(amout_yellow, amout_red, amout_green, int(time/3600), int((time/60) % 60)), font=("Arial", 14))
    score_message.pack(padx=100, pady=50)

    window.mainloop()

while running:

    screen.fill((0, 0, 0))
    lines()
    player_group.add(Player(x_Player, y_Player))
    wall_group.draw(screen)

    screen.blit(surface_score, (0, 0))
    screen.blit(surface_score_invisible, (30, 30))
    string_score = ('score: %s' % score)
    surface_score_invisible = font_score.render(string_score, True, ('green'))

    screen.blit(surface_text_spawn_red, (622, 320))
    screen.blit(surface_text_spawn_red, (72, 470))
    screen.blit(surface_text_spawn_yellow, (222, 20))
    screen.blit(surface_text_spawn_yellow, (222, 770))
    screen.blit(surface_text_spawn_yellow, (772, 270))
    screen.blit(surface_text_spawn_yellow, (22, 270))
    screen.blit(surface_text_spawn_yellow, (22, 620))
    screen.blit(surface_text_spawn_yellow, (772, 620))
    screen.blit(surface_text_spawn_green, (672, 420))


    player_group.draw(screen)
    enemy_group.draw(screen)
    defender_group.draw(screen)
    neutral_group.draw(screen)
    colliision()
    Neutral.spawn()
    Defender.spawn()


    Player.update()
    if npc_velocity > 60:
        enemy_group.update()
        neutral_group.update()
        defender_group.update()
        npc_velocity = 0
    else:
        npc_velocity += 1
    if len(enemy_group) == 0:
        running = False
        endgame_string = "Congratulations! You've won!"




    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            endgame_string = "You've failed"

    player_group.empty()


    time += 0.5

    clock.tick(120)
    last_move_time += 1
    pygame.display.update()


pygame.quit()
endgame_window()
