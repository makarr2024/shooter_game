#Создай собственный Шутер!

from pygame import *
from random import *
import time as timer 

font.init()
font = font.SysFont('Arial', 36)

# музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

# создание окна
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Galaxy shooter')
clock = time.Clock()
fps = 60
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

# классы
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        if keys_pressed[K_d] and self.rect.x < 635:
            self.rect.x += self.speed
        
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet('bullet.png', player.rect.centerx - 7, 425, 2, 15, 25  )
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
            
        if self.rect.y > 500:
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(10, 690)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

# объекты
player = Player('rocket.png', 350, 425, 5, 60, 65)

asteroids = sprite.Group()
for asteroid in range(3):
    asteroid = Enemy('asteroid.png', randint(20, 680), 0, randint(1,3), 50, 50)
    asteroid.add(asteroids)

monsters = sprite.Group()
for monster in range(5):
    monster = Enemy('ufo.png', randint(10, 690), 0, randint(1, 2), 75, 55)
    monsters.add(monster)

# переменные
bullets = sprite.Group()
lost = 0
score = 0
lives = 3
finish = False
game = True
rel_time = False
num_fire = 0

# игровой цикл
while game == True:
    keys_pressed = key.get_pressed()

    if finish != True:
        window.blit(background, (0, 0))
        sprites_list = sprite.groupcollide(bullets, monsters, True, True)
        
        collided_monsters = sprite.spritecollide(player, monsters, True)
        for mnstr in collided_monsters:
            monster = Enemy('ufo.png', randint(40, 660), 5, randint(1,3), 75, 55)
            monsters.add(monster)
            lives -= 1

        
        collided_asteroids = sprite.spritecollide(player, asteroids, True)
        for astr in collided_asteroids:
            asteroid = Enemy('asteroid.png', randint(20, 680), 0, randint(1,3), 50, 50)
            asteroid.add(asteroids)
            lives -= 1


        if lives == 0:
            text_lose = font.render('YOU LOSE!', 1, (255, 255, 255))
            window.blit(text_lose, (300, 250))
            finish = True

        for spr in sprites_list:
            score += 1
            monster = Enemy('ufo.png', randint(40, 660), 5, randint(1,3), 75, 55)
            monsters.add(monster)

        # отрисовка
        player.update()
        bullets.update()
        monsters.update()
        asteroids.update()
        player.reset()
        asteroids.draw(window)
        monsters.draw(window)
        bullets.draw(window)

        if score >= 10:
            text_win = font.render('YOU WIN!', 1, (255, 255, 255))
            window.blit(text_win, (300, 250))
            finish = True

        if lost >= 30:
            text_lose = font.render('YOU LOSE!', 1, (255, 255, 255))
            window.blit(text_lose, (300, 250))
            finish = True
            
        if rel_time == True:
            if (timer.time()) - time1 >= 1.5:
                num_fire = 0
                rel_time = False
            else:
                text_reload = font.render('Wait, reload', 1, (255, 0, 0))
                window.blit(text_reload, (320, 250))
            
            
            
        text_lost = font.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        text_score = font.render('Счёт:' + str(score), 1, (255, 255, 255))
        text_lives = font.render('Жизни:' + str(lives), 1, (255, 255, 255))
        window.blit(text_lost, (10, 50))
        window.blit(text_score, (10, 10))
        window.blit(text_lives, (590, 10))
         
        display.update()

    # получение событий
    for ev in event.get():
        if ev.type == QUIT:
            game = False

        if ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    player.fire()
                    num_fire += 1

                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    time1 = timer.time()
                    

    clock.tick(fps)