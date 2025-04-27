from pygame import *
from random import randint
from time import time as timer

score = 0
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 70: 
            self.rect.x += self.speed
            
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(100, 600)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play(-1) 
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 36)

game = True
finish = False
clock = time.Clock()
FPS = 60

rocket = Player('rocket.png', 300, 400, 10, 80, 100)
monsters = sprite.Group()  

for i in range(5):
    monster = Enemy('ufo.png', randint(100, 600), -48, randint(2, 7), 88, 50)
    monsters.add(monster)

bullets = sprite.Group()


asteroids = sprite.Group()

for i in range(3):
    asteroid = Enemy('asteroid.png', randint(100, 600), -48, randint(2, 7), 88, 50)
    asteroids.add(asteroid)

life = 3

rel_time = False
num_fire = 0


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    rocket.fire()
                    fire_sound.play()
                if  rel_time == False and num_fire >= 5:
                    rel_time = True
                    last_time = timer()

    if not finish:
        window.blit(background, (0, 0))
        
        text_score = font1.render('Счет: ' + str(score), True, (255,255,255))
        text_lost = font1.render('Потеряно: ' + str(lost), True, (255,255,255))

        window.blit(text_score, (18,20))
        window.blit(text_lost, (18,50))

        rocket.update()
        rocket.reset()

        monsters.update()
        monsters.draw(window)  

        bullets.update()
        bullets.draw(window)

        asteroids.draw(window)
        asteroids.update()

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for s in sprites_list:
            score += 1
            monster = Enemy('ufo.png', randint(100, 600), -48, randint(2, 7), 88, 50)
            monsters.add(monster)

        if sprite.spritecollide(rocket, asteroids, True):
            life -= 1 
        text_life = font1.render('Жизни '  + str(life), 1, (255,255,255))
        window.blit(text_life, (600, 10))

        if rel_time == True:
            new_time = timer()
            if new_time - last_time < 3:
                reload = font1.render('Перезагрузка', 1, (255,255,255))
                window.blit(reload, (250, 450))
            else:
                num_fire = 0
                rel_time = False


        if score >= 10:
            finish = True
            font2 = font.SysFont('Arial', 70) 
            win_text = font2.render('YOU WON!', True,(0 ,255 ,0))
            window.blit(win_text,(200 ,200))

        if lost == 3 or life == 0:
            finish = True
            font2 = font.SysFont('Arial' ,70) 
            lose_text= font2.render('YOU LOSE!', True,(255 ,0 ,0))
            window.blit(lose_text,(200 ,200))

    display.update()
    clock.tick(FPS)