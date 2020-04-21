import pygame as pg
import random
import time

pg.init()

WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 30
BG_IMAGE = "files/bg.jpg"
HERO_IMAGE = "files/hero.png"
MARCH_IMAGE = "files/march.png"
WALL_IMAGE = "files/moss.jpg"
MOE_IMAGE = "files/moe.png"
BEER_IMAGE = "files/beer.png"

# all classes
class BeerCup(pg.sprite.Sprite):
    def __init__(self, filename=BEER_IMAGE, x=200, y=200, width=10, height=10):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load(filename),
                        (width, height)).convert_alpha()
        # self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.speed_y = 0
        self.speed_x = 12

    def gravity(self):
        self.speed_y += 0.35

    def fly(self, x):
        if x < 0:
            self.speed_y = - self.speed_y
            self.speed_x = -abs(self.speed_x)

    def update(self):
        # platforms_touched = pg.sprite.spritecollide(self, walls, False)
        # for p in platforms_touched:
        #     self.kill()

        self.gravity()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

class Moe(pg.sprite.Sprite):
    def __init__(self, filename=MOE_IMAGE, x=710, y=300, width=80, height=110, speed=5):
        pg.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = pg.transform.scale(pg.image.load(filename),
                        (width, height)).convert()
        if speed < 0:
            self.image = pg.transform.flip(self.image, True, False)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 


    def update(self):
        if self.rect.left <= 120:
            self.speed = random.randint(1, 5)
        elif self.rect.right >= 680:
            self.speed = random.randint(-5, -1)
        self.rect.x += self.speed

class March(pg.sprite.Sprite):
    def __init__(self, filename=MARCH_IMAGE, x=710, y=457, width=100, height=140):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load(filename),
                        (width, height)).convert()
        # self.image = pg.transform.flip(self.image, True, False)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 

class Hero(pg.sprite.Sprite):
    def __init__(self, filename, x_speed=0, y_speed=0, x=0, y=0, width=100, height=120):
        pg.sprite.Sprite.__init__(self)
        self.filename = filename
        self.width = width
        self.height = height
        self.rect =  self.load_image(1)
        self.rect.x = x 
        self.rect.y = y 

        self.x_speed = x_speed 
        self.y_speed = y_speed 

        self.stand_on = False

    def load_image(self, x_speed):
        self.image = pg.transform.scale(pg.image.load(self.filename),
                        (self.width, self.height)).convert()
        if x_speed >= 0:
            self.image = pg.transform.flip(self.image, True, False)
        self.image.set_colorkey((0,0,0))
        rect = self.image.get_rect()
        return rect 

    def gravity(self):
        self.y_speed += 0.35

    def jump(self, y):
        if self.stand_on:
            self.y_speed = y

    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = pg.sprite.spritecollide(self, walls, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)

        self.gravity()
        self.rect.y += self.y_speed
        platforms_touched = pg.sprite.spritecollide(self, walls, False)
        if self.y_speed > 0: # move down
            for p in platforms_touched:
                self.y_speed = 0
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
                self.stand_on = p
        elif self.y_speed <= 0: # move up
            self.stand_on = False
            for p in platforms_touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top, p.rect.bottom)

class Wall(pg.sprite.Sprite):
    def __init__(self, x=10, y=0, width=100, height=40, filename=WALL_IMAGE):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename)
        self.image = pg.transform.scale(self.image, (width, height)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 

# window settings
window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Save")

# load images
bg_img = pg.image.load(BG_IMAGE).convert()
bg = pg.transform.scale(bg_img, (WIN_WIDTH, WIN_HEIGHT))

wall_image = pg.image.load(BG_IMAGE).convert()
wall = pg.transform.scale(bg_img, (10, 100))

timer = pg.time.Clock()

# create sprites
all_sprites = pg.sprite.Group()
walls = pg.sprite.Group()
march_spride = pg.sprite.Group()
moe_sprite = pg.sprite.Group()
beers = pg.sprite.Group()

# create objects
homer = Hero(HERO_IMAGE)

# add objects to sprites
all_sprites.add(homer)

for i in range(7):
    w = Wall(i*100, 150)
    walls.add(w)
    all_sprites.add(w)
for i in range(7):
    w = Wall(100+i*100, 370)
    walls.add(w)
    all_sprites.add(w)
for i in range(8):
    w = Wall(i*100, 590)
    walls.add(w)
    all_sprites.add(w)

march = March()
march_spride.add(march)
# all_sprites.add(march)

for j in range(2):
    moe = Moe(x=random.randint(120, 680), y=44)
    moe_sprite.add(moe)
    all_sprites.add(moe)
for j in range(2):
    moe = Moe(x=random.randint(120, 680), y=268, speed=-1)
    moe_sprite.add(moe)
    all_sprites.add(moe)
for j in range(2):
    moe = Moe(x=random.randint(120, 680), y=485)
    moe_sprite.add(moe)
    all_sprites.add(moe)

flag = "R"
run = True 
while run:
    for event in pg.event.get(): 
        if event.type == pg.QUIT: 
            run = False 
        elif event.type == pg.KEYDOWN: 
            if event.key == pg.K_LEFT:
                flag = "L"
                homer.x_speed = -5 
                homer.load_image(-1)
            elif event.key == pg.K_RIGHT:
                flag = "R"
                homer.x_speed = 5 
                homer.load_image(1)
            elif event.key == pg.K_UP:
                homer.jump(-7)
            elif event.key == pg.K_SPACE:
                beer = BeerCup(width=20, height=20, x=homer.rect.x + 5, 
                                y=homer.rect.y + 3)
                beers.add(beer)
                all_sprites.add(beer)
                if flag == "R":
                    beer.fly(+1)
                elif flag == "L":
                    beer.fly(-1)
            elif event.key == pg.K_ESCAPE:
                run = False

        elif event.type == pg.KEYUP: 
            if event.key == pg.K_LEFT:
                homer.x_speed = 0
                flag = "L"
            elif event.key == pg.K_RIGHT:
                homer.x_speed = 0
                flag = "R"
                        
    all_sprites.update()

    pg.sprite.groupcollide(beers, walls, True, False)
    pg.sprite.groupcollide(beers, moe_sprite, True, True)

    if pg.sprite.spritecollide(homer, march_spride, True):
        run = False
        f2 = pg.font.SysFont('serif', 78)
        img2 = f2.render("You Win!!!", 0, (255, 0, 0))
        rect2 = img2.get_rect()
        pg.draw.rect(img2, (255,0,255), rect2, 1)
        window.blit(img2, (250, 200))
        pg.display.update()
        time.sleep(5)

    if pg.sprite.spritecollide(homer, moe_sprite, False):
        homer.kill()
        run = False

    if homer.rect.top < 0 or homer.rect.bottom > WIN_HEIGHT:
        homer.rect.y -= homer.y_speed
    if homer.rect.right > WIN_WIDTH or homer.rect.left < 0:
        homer.rect.x -= homer.x_speed

    window.blit(bg, (0,0))
    
    all_sprites.draw(window)
    march_spride.draw(window)
    
    pg.display.update()
    timer.tick(FPS)