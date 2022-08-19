import pygame
import random
import os
WIDTH = 1000
HEIGHT = 1000
FPS = 60

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

score = 0

class Star(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((8, 8))
        self.image = star_img
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0,WIDTH), random.randint(0,HEIGHT))

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image = rock_img
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0,WIDTH), 0)
    def update(self):
        global score
        self.rect.y += 2
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(0,WIDTH), random.randint(-HEIGHT/2,0))
        if pygame.sprite.collide_rect(self, player):
            score -= 20
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image = enemy_img
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0,WIDTH), 0)
    def update(self):
        global score
        self.rect.y += 5
        self.rect.x += random.randint(-5,5)
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(0,WIDTH), random.randint(-HEIGHT/2,0))
        if pygame.sprite.collide_rect(self, player):
            score -= 5


class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((3, 6))
        self.image = rocket_img
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (player.rect.x, player.rect.y)
    def update(self):
        global score
        self.rect.y -= 10
        if self.rect.y == 0:
            self.kill()

p_move_left=False
p_move_right=False
p_move_up=False
p_move_down=False

weapon_act=False
f_delay=0
f_count=0

e_delay=0
e_count=0
r_count=0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 20))
        self.image = player_img
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2,7*HEIGHT/8)
    def update(self):
        global p_move_left
        global p_move_right
        global p_move_up
        global p_move_down
        
        global weapon_act
        global f_delay
        global f_count
        
        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            if(event.key==pygame.K_d):
                p_move_right=True
            if(event.key==pygame.K_a):
                p_move_left=True
            if(event.key==pygame.K_w):
                p_move_up=True
            if(event.key==pygame.K_s):
                p_move_down=True
            if(event.key==pygame.K_SPACE):
                weapon_act=True
        for event in pygame.event.get(eventtype=pygame.KEYUP):
            if(event.key==pygame.K_d):
                p_move_right=False
            if(event.key==pygame.K_a):
                p_move_left=False
            if(event.key==pygame.K_w):
                p_move_up=False
            if(event.key==pygame.K_s):
                p_move_down=False
            if(event.key==pygame.K_SPACE):
                    weapon_act=False

                    
        if(p_move_left):
            self.rect.x -= 6
        if(p_move_right):
            self.rect.x += 6
        if(p_move_up):
            self.rect.y -= 6
        if(p_move_down):
            self.rect.y += 6
        if self.rect.x < 0:
            self.rect.x = 0
            
        if self.rect.x > WIDTH-10:
            self.rect.x = WIDTH-10
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > HEIGHT-15:
            self.rect.y = HEIGHT-15

        if(weapon_act):
            f_delay += 1
            if f_delay == 5:
                f_delay = 0
                f_count += 1
                exec(f'rocket_{f_count}=Rocket()')
                exec(f'rockets.add(rocket_{f_count})')


pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
my_font2 = pygame.font.SysFont('Impact', 36)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Soldiers")

player_img = pygame.image.load(os.path.join(img_folder, 'player.png')).convert()
enemy_img = pygame.image.load(os.path.join(img_folder, 'enemy.png')).convert()
star_img = pygame.image.load(os.path.join(img_folder, 'star.png')).convert()
rocket_img = pygame.image.load(os.path.join(img_folder, 'rocket.png')).convert()
rock_img = pygame.image.load(os.path.join(img_folder, 'rock.png')).convert()

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
rockets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

star_sprites = pygame.sprite.Group()
for i in range(100):
    exec(f'star_{i} = Star()')
    exec(f'star_sprites.add(star_{i})')


running1 = True
running = True

while running:
    for event in pygame.event.get(eventtype=pygame.QUIT):
        if event:
           running = False
    clock.tick(FPS)
    if running1 == True:
        all_sprites.update()
        rockets.update()
        enemies.update()
        e_delay+=1
        if e_delay == 20 or e_delay == 40:
            exec(f'enemy_{e_count} = Enemy()')
            exec(f'enemies.add(enemy_{e_count})')
            e_count+=1
            if e_delay == 40:
                e_delay = 0
                exec(f'rock_{e_count} = Rock()')
                exec(f'enemies.add(rock_{e_count})')
    for enemie in enemies:
        for rocket in rockets:
            if pygame.sprite.collide_rect(rocket, enemie):
                enemie.kill()
                rocket.kill()
                score += 1

    screen.fill((0,0,30))
    star_sprites.draw(screen)
    all_sprites.draw(screen)
    rockets.draw(screen)
    enemies.draw(screen)
    if score < 0:
        player.kill()
        running1 = False
        gameovertext = my_font2.render("Game Over", 1, (255,255,255))
        gameovertext_rect = gameovertext.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(gameovertext, gameovertext_rect)
        playagaintext = my_font.render("Move your mouse to play again", 1, (255,255,255))
        playagaintext_rect = playagaintext.get_rect(center=(WIDTH/2, HEIGHT/2+30))
        screen.blit(playagaintext, playagaintext_rect)
        for event in pygame.event.get():
            if(event.type==pygame.MOUSEMOTION):
                for enemie in enemies:
                    enemie.kill()
                score = 0
                f_delay = 0
                f_count = 0
                e_delay = 0
                e_count = 0
                r_count = 0
                player = Player()
                all_sprites.add(player)
                running1 = True
        
    scoretext = my_font.render("Score: {0}".format(score), 1, (255,255,255))
    screen.blit(scoretext, (5, 10))
    pygame.display.flip()

pygame.quit()
