import pygame, sys
from pygame import mixer
pygame.init()

score = 0
window = pygame.display.set_mode((700, 550))
clock = pygame.time.Clock()
pygame.display.set_caption('ADVENTURES OF SANTA')


slide_right = pygame.image.load('sprites//santa_right//RS1.png')
slide_left = pygame.image.load('sprites//santa_left//LS1.png')
char = pygame.image.load('sprites//santa_right//RI1.png')
background = pygame.image.load('sprites//icebg.png')
END = pygame.image.load('sprites//info.png')
HEROEND = pygame.image.load('sprites//heroend.png')
bg = pygame.mixer.Sound('sounds//background.wav')
Evil_Laugh = pygame.mixer.Sound('sounds//Evil_Laugh.wav')
fire = pygame.mixer.Sound('sounds//fireball.wav')
icon = pygame.image.load('sprites//icon.png')
pygame.display.set_icon(icon)
bg.play(-1)


class player:

    walk_right = [pygame.image.load('sprites//santa_right//RW1.png'),pygame.image.load('sprites//santa_right//RW2.png'),
                  pygame.image.load('sprites//santa_right//RW3.png'),pygame.image.load('sprites//santa_right//RW4.png'),
                  pygame.image.load('sprites//santa_right//RW5.png'),pygame.image.load('sprites//santa_right//RW6.png'),
                  pygame.image.load('sprites//santa_right//RW7.png'),pygame.image.load('sprites//santa_right//RW8.png'),
                  pygame.image.load('sprites//santa_right//RW9.png'),pygame.image.load('sprites//santa_right//RW10.png')]

    walk_left = [pygame.image.load('sprites//santa_left//LW1.png'),pygame.image.load('sprites//santa_left//LW2.png'),
                 pygame.image.load('sprites//santa_left//LW3.png'),pygame.image.load('sprites//santa_left//LW4.png'),
                 pygame.image.load('sprites//santa_left//LW5.png'),pygame.image.load('sprites//santa_left//LW6.png'),
                 pygame.image.load('sprites//santa_left//LW7.png'),pygame.image.load('sprites//santa_left//LW8.png'),
                 pygame.image.load('sprites//santa_left//LW9.png'),pygame.image.load('sprites//santa_left//LW10.png')]

    def __init__(self, playerX, playerY, player_width, player_height):
        self.playerX = playerX
        self.playerY = playerY
        self.player_width = player_width
        self.player_height = player_height
        self.vel = 5
        self.jump = False
        self.m = 1
        self.v = 8
        self.left = False
        self.right = False
        self.slidel = False
        self.slider = False
        self.standing = True
        self.hitbox = (self.playerX + 20, self.playerY + 10, 25, 50)
        self.health = 10

    def redraw(self, window):

        if self.slidel or self.slider == True:
            self.vel = 7

        elif self.slidel or self.slider == False:
            self.vel = 5

        if not (self.standing):
            if self.left:
                if self.slidel:
                    window.blit(slide_left, (self.playerX, self.playerY))
                    self.slidel = False
                else:
                    window.blit(self.walk_left[len(self.walk_left)//3], (self.playerX, self.playerY))
                self.walk_count += 1
            elif self.right:
                if self.slider:
                    window.blit(slide_right, (self.playerX, self.playerY))
                    self.slider = False
                else:
                    window.blit(self.walk_right[len(self.walk_right) // 3], (self.playerX, self.playerY))
                self.walk_count += 1

        else:
            if self.right:
                window.blit(self.walk_right[0], (self.playerX, self.playerY))
            elif self.left:
                window.blit(self.walk_left[0], (self.playerX, self.playerY))
            else:
                window.blit(char, (self.playerX, self.playerY))

        self.hitbox = (self.playerX + 25, self.playerY + 5, 25, 50)
        pygame.draw.rect(window, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 30, 50, 10))
        pygame.draw.rect(window, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 30, 50 - (5 * (10 - self.health)), 10))

    def hit(self):
        if self.health > 0:
            self.health -= 1


class projectile:
    def __init__(self, playerX, playerY, radius, colour, facing):
        self.playerX = playerX
        self.playerY = playerY
        self.radius = radius
        self.colour = colour
        self.facing = facing
        self.v = 10 * facing

    def draw(self, window):
        pygame.draw.circle(window, self.colour, (self.playerX, self.playerY), self.radius)


class enemy:

    walkRight = [pygame.image.load('sprites//villian_right//RW1.png'),pygame.image.load('sprites//villian_right//RW2.png'),
                 pygame.image.load('sprites//villian_right//RW3.png'),pygame.image.load('sprites//villian_right//RW4.png'),
                 pygame.image.load('sprites//villian_right//RW5.png'),pygame.image.load('sprites//villian_right//RW6.png'),
                 pygame.image.load('sprites//villian_right//RW7.png'),pygame.image.load('sprites//villian_right//RW8.png'),
                 pygame.image.load('sprites//villian_right//RW9.png'),pygame.image.load('sprites//villian_right//RW10.png')]

    walkLeft = [pygame.image.load('sprites//villian_left//LW1.png'),pygame.image.load('sprites//villian_left//LW2.png'),
                pygame.image.load('sprites//villian_left//LW3.png'),pygame.image.load('sprites//villian_left//LW4.png'),
                pygame.image.load('sprites//villian_left//LW5.png'),pygame.image.load('sprites//villian_left//LW6.png'),
                pygame.image.load('sprites//villian_left//LW7.png'),pygame.image.load('sprites//villian_left//LW8.png'),
                pygame.image.load('sprites//villian_left//LW9.png'),pygame.image.load('sprites//villian_left//LW10.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkCount = 0
        self.vel = 6
        self.hitbox = (self.x + 20, self.y, 35, 60)
        self.health = 10
        self.visible = True

    def draw(self, window):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 30:
                self.walkCount = 0
            if self.vel > 0:
                window.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                window.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(window, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(window, (0, 128, 0),
                             (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 20, self.y, 35, 60)

    def move(self):

        if self.vel > 0:
            if self.x + self.vel < 645:
                self.x += self.vel
            else:
                self.vel = self.vel * (-1)
                self.walkCount = 0

        elif self.vel < 0:
            if self.x - self.vel > 0:
                self.x += self.vel
            else:
                self.vel = self.vel * (-1)
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False


class enemy_projec:
    def __init__(self, x, y, rad, color, face):
        self.x = x
        self.y = y
        self.rad = rad
        self.color = color
        self.face = face
        self.v = 20 * face

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.rad)


def redrawwin():

    window.blit(background, (0, 0))
    text = font.render('Score: ' + str(score), 1, (150, 0, 150))
    window.blit(text, (280, 20))
    hero.redraw(window)
    villian.draw(window)
    for iceball in iceballs:
        iceball.draw(window)
    for fireball in fireballs:
        fireball.draw(window)
    pygame.display.update()


def main_loop():

    # GLOBAL VARIABLE
    global hero
    global font
    global score
    global villian
    global iceballs
    global fireballs

    run = True
    hero = player(50, 400, 93, 64)
    font = pygame.font.SysFont('comicsans', 50, True)
    fireballs = []
    iceballs = []
    villian = enemy(500, 400, 64, 64, 450)
    shootLoop = 0

    while run:

        clock.tick(30)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()  # quit the screen
                run = False
                sys.exit()

        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > 3:
            shootLoop = 0

        if keys[pygame.K_SPACE] and shootLoop == 0:
            if hero.left:
                facing = -1
            else:
                facing = 1
            if len(iceballs) < 1:
                iceballs.append(projectile(round(hero.playerX + hero.player_width // 2),
                                           round(hero.playerY + hero.player_height // 2), 8, (250, 250, 250), facing))
            shootLoop = 1

        if shootLoop == 0:
            if villian.vel > 0:
                face = 1
            else:
                face = -1
            if len(fireballs) < 1:
                fireballs.append(
                    enemy_projec(round(villian.x + villian.width // 2), round(villian.y + villian.height // 2), 8,
                                 (255, 165, 0), face))
            shootLoop = 1

        if keys[pygame.K_LEFT]:

            if hero.playerX <= -36:
                hero.playerX = -36
                if keys[pygame.K_DOWN]:
                    hero.slidel = True
                    hero.slider = False
                hero.left = True
                hero.right = False
                hero.standing = False

            else:
                hero.playerX -= hero.vel
                hero.left = True
                hero.right = False
                hero.standing = False
                if keys[pygame.K_DOWN]:
                    hero.slidel = True
                    hero.slider = False

        elif keys[pygame.K_RIGHT]:

            if hero.playerX >= 644:
                hero.playerX = 644
                if keys[pygame.K_DOWN]:
                    hero.slider = True
                    hero.slidel = False
                hero.right = True
                hero.left = False
                hero.standing = False

            else:
                hero.playerX += hero.vel
                hero.right = True
                hero.left = False
                hero.standing = False
                if keys[pygame.K_DOWN]:
                    hero.slider = True
                    hero.slidel = False

        else:
            hero.standing = True
            hero.walk_count = 0

        if hero.jump == False:
            if keys[pygame.K_UP]:
                hero.jump = True

        if hero.jump:
            F = 0.5 * hero.m * (hero.v ** 2)
            hero.playerY -= int(F)
            hero.v -= 1
            if hero.v < 0:
                hero.m = -1
            if hero.v == -9:
                hero.jump = False
                hero.v = 8
                hero.m = 1

        if hero.health == 0:
            score = 0
            if keys[pygame.K_RETURN]:
                main_loop()
            else:
                window.blit(HEROEND, (0, 0))
                pygame.display.update()
                pygame.time.delay(200)

        if villian.visible == True:

            if hero.hitbox[1] < villian.hitbox[1] + villian.hitbox[3] and hero.hitbox[1] + hero.hitbox[3] > \
                    villian.hitbox[1]:
                if hero.hitbox[0] + hero.hitbox[2] > villian.hitbox[0] and hero.hitbox[0] < villian.hitbox[0] + \
                        villian.hitbox[2]:
                    hero.hit()
                    Evil_Laugh.play()
                    score -= 1

            for iceball in iceballs:
                if iceball.playerY - iceball.radius < villian.hitbox[1] + villian.hitbox[
                    3] and iceball.playerY + iceball.radius > villian.hitbox[1]:
                    if iceball.playerX + iceball.radius > villian.hitbox[0] and iceball.playerX - iceball.radius < \
                            villian.hitbox[0] + villian.hitbox[2]:
                        villian.hit()
                        score += 1
                        iceballs.pop(iceballs.index(iceball))

                if iceball.playerX < 700 and iceball.playerX > 0:
                    iceball.playerX += iceball.v
                else:
                    iceballs.pop(iceballs.index(iceball))

            for fireball in fireballs:
                if fireball.y - fireball.rad < hero.hitbox[1] + hero.hitbox[3] and fireball.y + fireball.rad > \
                        hero.hitbox[1]:
                    if fireball.x + fireball.rad > hero.hitbox[0] and fireball.x - fireball.rad < hero.hitbox[0] + \
                            hero.hitbox[2]:
                        hero.hit()
                        fire.play()
                        score -= 1
                        fireballs.pop(fireballs.index(fireball))

                if fireball.x < 700 and fireball.x > 0:
                    fireball.x += fireball.v
                else:
                    fireballs.pop(fireballs.index(fireball))

        elif villian.visible == False:
            score = 0
            if keys[pygame.K_RETURN]:
                main_loop()
            else:
                window.blit(END, (0, 0))
                pygame.display.update()
                pygame.time.delay(200)

        redrawwin()

main_loop()
