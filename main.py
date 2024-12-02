from pygame import *
from time import sleep


init()

clock = time.Clock()
back = (0,0,0)
mw = display.set_mode((700, 500))

mw_size = mw.get_size()


class GameSprite(sprite.Sprite):
    def __init__(self, img, blur_img, x, y, w, h, speed=5):
        super().__init__()
        self.image = image.load(img)
        self.blur_image = image.load(blur_img)
        self.w = w
        self.h = h
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)        



class Player(GameSprite):
    def __init__(self, img, blur_img, x, y, w, h, speed=5):
        self.hiden = False
        self.score = 0
        super().__init__(img, blur_img, x, y, w, h, speed)

    def draw(self):
        mw.blit(self.image, self.rect.topleft)
        mw.blit(self.blur_image, (self.rect.center[0] - 24, self.rect.center[1] - 64))


class Ball(GameSprite):
    def __init__(self, img, blur_img, x, y ,w, h):
        super().__init__(img, blur_img, x, y, w, h)
        self.speed_x = 3
        self.speed_y = 2
        self.last_hit_player = None

    def speed_up(self):
        self.speed_x += 0.2 if self.speed_x >= 0 else -0.2
        self.speed_y += 0.2 if self.speed_y >= 0 else -0.2
        
    def update(self):
        self.rect.x += int(self.speed_x)
        self.rect.y += int(self.speed_y)

        if self.rect.x + self.w <= 0:
            lose(players[0])
        if self.rect.x >= mw_size[0]:
            lose(players[1])

        if self.rect.y <= 0 or self.rect.y + self.h >= mw_size[1]:
            self.speed_y *= -1

        for i, player in enumerate(players):
            if sprite.collide_rect(self, player):
                if self.last_hit_player != i:
                    self.speed_x *= -1                
                    diff = (player.rect.centery - self.rect.centery) / (player.h / 2)
                    self.speed_y = (diff * 2) * -1
                    self.speed_up()
                    self.last_hit_player = i
                break
        else:
            self.last_hit_player = None

    def draw(self):
        mw.blit(self.image, self.rect.topleft)
        mw.blit(self.blur_image, (self.rect.center[0] - 45, self.rect.center[1] - 45))





def move():
    keys = key.get_pressed()
    if keys[K_w] and players[0].rect.y > 0:
        players[0].rect.y -= players[0].speed
    if keys[K_s] and players[0].rect.y + players[0].h < mw_size[1]:
        players[0].rect.y += players[0].speed

    if keys[K_UP] and players[1].rect.y > 0:
        players[1].rect.y -= players[1].speed
    if keys[K_DOWN] and players[1].rect.y + players[1].h < mw_size[1]:
        players[1].rect.y += players[1].speed


def lose(player):
    for i in range(7):
        mw.fill(back)
        BALL.draw()
        for p in players:
            if p == player:
                p.hiden = not p.hiden
                if not p.hiden:
                    p.draw()
            else:
                p.draw()
                    
        display.update()
        sleep(0.3)
    for p in players:
        p.rect.y = 250 - (p.h // 2)
        if p is not player:
            p.score += 1
    print(f"{players[0].score}:{players[1].score}")

    BALL.rect.x, BALL.rect.y = (350, 250)
    BALL.speed_x = max(int(BALL.speed_x // 2), 2)
    display.update()
    
        
    


enemies = []

players = (Player("player.png", "player_blur.png", 40, 250, 13, 95), Player("player.png", "player_blur.png", 660, 250, 13, 95))

BALL = Ball("ball.png", "ball_blur.png", 350, 250, 54, 54)


running = True
finished = False


while running:
    mw.fill(back)

    for e in event.get():
        if e.type == QUIT:
            running = False

    if not finished:
        move()

        BALL.update()
        BALL.draw()

        
        players[0].draw()
        players[1].draw()
        

    display.update()
    clock.tick(60)


quit()
