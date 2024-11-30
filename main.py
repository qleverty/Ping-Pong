import pygame


pygame.init()

clock = pygame.time.Clock()
back = (200, 240, 240)
mw = pygame.display.set_mode((500, 500))


def end_screen(mode):
    global game_finished
    font = pygame.font.Font(None, 74)
    if mode == "won":
        mw.fill((240, 240, 240))
        text = font.render("You Won!", True, (0, 0, 0))
        mw.blit(text, (130, 230))

        ball_speed = 0
        platform_speed = 0
    elif mode == "lose":
        mw.fill((240, 240, 240))
        text = font.render("You Lose!", True, (0, 0, 0))
        mw.blit(text, (130, 230))

    else:
        suicide = 2 + "2"

    game_finished = True
        

class Area():
    def __init__(self, window, width, height, x, y, color):
        self.window = window
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.fill_color = color if color is not None else back
        self.rect = pygame.Rect(x, y, width, height)
    
    def change_color(self, new_color):
        self.fill_color = new_color
    
    def fill(self):
        pygame.draw.rect(self.window, self.fill_color, self.rect)
    
    def outline(self, color, width):
        pygame.draw.rect(self.window, color, self.rect, width)
    
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

class Picture(Area):
    def __init__(self, window, width, height, x, y, filename):
        super().__init__(window, width, height, x, y, None)
        self.image = pygame.image.load(filename)
    def draw(self):
        self.window.blit(self.image, (self.rect.x, self.rect.y))

offset = 55

enemies = []
for i in range(3):

    for j in range(9 - i):
        x = 5 + offset // 2 * i + offset * j
        y = 5 + offset * i
        printer = Picture(mw, 50, 50, x, y, "enemy.png")
        enemies.append(printer)

ball_speed = 3
platform_speed = 3

x_speed = ball_speed
y_speed = ball_speed * -1

ball = Picture(mw, 50, 50, 230, 255, "ball.png")
platform = Picture(mw, 50, 50, 225, 400, "platform.png")

right_pressed = False
left_pressed = False

ball_hitable = True
game_finished = False

running = True



while running:
    if not game_finished:
        mw.fill(back)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                right_pressed = True
            elif event.key == pygame.K_LEFT:
                left_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                right_pressed = False
            elif event.key == pygame.K_LEFT:
                left_pressed = False

#         # Auto-Pilot:
#    platform_speed = ball_speed
#    if not game_finished:
#        if platform.rect.x < (ball.rect.x - 25) and platform.rect.x < 400:
#            platform.rect.x+=platform_speed
#        elif platform.rect.x > (ball.rect.x - 25) and platform.rect.x > 0:
#            platform.rect.x-=platform_speed



    if not game_finished:
        if right_pressed and platform.rect.x < 400:
            platform.rect.x+=platform_speed
        elif left_pressed and platform.rect.x > 0:
            platform.rect.x-=platform_speed

        
        if ball.rect.y < 0:
            y_speed *= -1
        if ball.rect.x > 450 or ball.rect.x < 0:
            x_speed *= -1
        if ball.rect.y > 450:
            end_screen("lose")
        if ball.colliderect(platform.rect):
            y_speed = ball_speed * -1
            ball_hitable = True
    
        ball.rect.x+=x_speed
        ball.rect.y+=y_speed

    
        if len(enemies) == 0:
            end_screen("won")
        for enemy in enemies:
            if ball.colliderect(enemy.rect) and ball_hitable:
                enemies.remove(enemy)
                y_speed *= -1
                ball_hitable = False
            
        
            
    
    
    # Отрисовка:
    
    for enemy in enemies:
        enemy.draw()

    


    ball.draw()
    platform.draw()
        

    pygame.display.update()
    clock.tick(60)

pygame.quit()
