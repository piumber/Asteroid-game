#Створи власний Шутер!

from pygame import *
from random import randint

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')

score = 0
lost = 0
goal = 10
max_lost = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
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
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed

        if self.rect.y > win_height:
            lost += 1
            self.rect.y = 0 
            self.rect.x = randint(80, win_width-80)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.kill()


rocket = Player('rocket.png', 5, win_height-100, 80, 100, 10)
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))                    

ufos = sprite.Group()
for i in range(5):
    ufo = Enemy('ufo.png', randint(80, win_width-80), randint(-20, 0), 80, 50, randint(2, 5))
    ufos.add(ufo)
bullets = sprite.Group()


finish = False
game = True
FPS = 60
clock = time.Clock()

mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 35)
font2 = font.SysFont('Arial', 72)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                rocket.fire()
    if not finish:
        window.blit(background, (0, 0))
        rocket.update()
        rocket.reset()

        ufos.update()
        ufos.draw(window)
        bullets.update()
        bullets.draw(window)
 
        collides = sprite.groupcollide(ufos, bullets, True, True)
        for c in collides:
            score += 1
            ufo = Enemy('ufo.png', randint(80, win_width-80), randint(-20, 0), 80, 50, randint(2, 5))
            ufos.add(ufo)

        if sprite.spritecollide(rocket, ufos, True) or lost >= max_lost:
            finish = True
            lose = font2.render('YOU LOSE!', True, (180, 0, 0))
            window.blit(lose, (200, 200))
        elif score >= goal:
            finish = True 
            win = font2.render('YOU WIN!', True, (255, 255, 255))
            window.blit(win, (200, 200))   

        text = font1.render("Рахунок: "+str(score), 1, (207, 215, 255))
        text_lost = font1.render("Пропущенно: "+str(lost), 1, (207, 215, 255))

        window.blit(text, (10, 20))
        window.blit(text_lost, (10, 50))
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for ufo in ufos:
            ufo.kill()

        time.delay(3000)
        for i in range(1, 5):
            ufo = Enemy('ufo.png', randint(80, win_width-80), randint(-20, 0), 80, 50, randint(2, 5))
            ufos.add(ufo)

    display.update()
    clock.tick(FPS)

