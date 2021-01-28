import pygame
import random
import time
from pygame.locals import *
import math
from levels import *
pygame.init()

bg = pygame.image.load('ground.png')
bg2 = pygame.image.load('ground.png') 
tile = pygame.image.load('tiles.png') 
coin = pygame.image.load('coin.png')
fin = pygame.image.load('fin.jpeg')
lava = pygame.image.load('lava.png')
clouds = pygame.image.load('cloud.png')
mounts = pygame.image.load('Mountains.png')
window = pygame.display.set_mode((800, 600)) 
onfin = False
x = 0 #x for the ground
x2 = -1100 #x for the other ground
playerx=268 #fake playerx for putting images that dont need to repeat
jumpcount = 40 
jump = 0
animate = 1 
pygame.display.set_caption('Platformer Shooter')
groundmove = 0
monsters = []
clock = pygame.time.Clock()
white = (255, 255, 255)
black = (0, 0, 0)
blue = (50, 155, 255)
collisionl = False
collisionr = False
collisiontop = False
font = pygame.font.SysFont(None, 24)
fontbig = pygame.font.SysFont(None, 100)
jumpupspeed = 10
gravityspeed = 4
cloudx = 0
pygame.mixer.get_init()
pygame.mixer.get_num_channels()
shootsound = pygame.mixer.Sound('shoot.wav')
shootsound.play()
class Player:
    def __init__(self, x, y):
        self.health = 5 #player health
        self.x = x
        self.y = y
        self.level = 1
        self.score = 0
        self.vel = 2
        self.facing = ('right')
        self.PlayerIdle = (pygame.image.load('PlayerIdle.png'))
        self.PlayerRun1 = (pygame.image.load('PlayerRun1.png'))
        self.PlayerRun2 = (pygame.image.load('PlayerRun2.png'))
        self.PlayerRun3 = (pygame.image.load('PlayerRun3.png'))
        self.PlayerRun4 = (pygame.image.load('PlayerRun4.png'))
        self.PlayerIdleL = (pygame.image.load('PlayerIdleL.png'))
        self.PlayerRun1L = (pygame.image.load('PlayerRun1L.png'))
        self.PlayerRun2L = (pygame.image.load('PlayerRun2L.png'))
        self.PlayerRun3L = (pygame.image.load('PlayerRun3L.png'))
        self.PlayerRun4L = (pygame.image.load('PlayerRun4L.png'))
        self.PlayerShootIdle = (pygame.image.load('PlayerShootIdle.png'))
        self.PlayerShootIdleL = (pygame.image.load('PlayerShootIdleL.png'))
        self.state = self.PlayerIdle
        self.playerrect = Rect(self.x+14, self.y+4, 34 , 55)
    def render(self):
        window.blit((player.state), (self.x, self.y))
        self.playerrect = Rect(self.x+14, self.y+4, 34 , 55)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shot = False
        self.speedir = 5
        self.range = 900 #bullet range
    def shoot(self, x, y, direction):
        self.x = x + 30
        self.y = y + 30
        self.shot = True
        if direction == 'right':
            self.speedir = 5
        else:
            self.speedir = -5
    def update(self):
        self.x += self.speedir
        if self.x > 800 or self.x < 0:
            self.shot = False

    def render(self):
        if self.shot == True:
            pygame.draw.rect(window, black, (self.x, self.y, 10, 5))

class Monsters:
    def __init__(self, x, y, block=None):
        self.x = x
        self.y = y
        self.speedir = 5
        self.block = block
        #self.health = 2
        #self.mobnum = 5
        self.originaly = self.y
        self.s1 = (pygame.image.load('slime1.png'))
        self.s2 = (pygame.image.load('slime2.png'))
        self.s3 = (pygame.image.load('slime3.png'))
        self.s4 = (pygame.image.load('slime4.png'))
        self.s5 = (pygame.image.load('slime5.png'))
        self.s6 = (pygame.image.load('slime6.png'))
        self.s7 = (pygame.image.load('slime7.png'))
        self.s8 = (pygame.image.load('slime8.png'))
        self.s9 = (pygame.image.load('slime9.png'))
        self.s10 = (pygame.image.load('slime10.png'))
        self.img = self.s1
        self.slimerect = Rect(self.x, self.y, self.img.get_size()[0] , self.img.get_size()[1])
    def move(self, targetx, groundmove):
        if self.block != None:
            xlimitr = ((map1[self.block])[1])
            xlimitl = ((((map1[self.block])[2])*60)+xlimitr)
        else:
            xlimitl = math.inf
            xlimitr = -(math.inf)
        
        if animate == 2:
            self.img = self.s1
            self.y = self.y
        if animate == 4:
            self.img = self.s2
            self.y -=16
        if animate == 6:
            self.img = self.s3
            self.y -=8
        if animate == 8:
            self.img = self.s4
            self.y -=6
        if animate == 10:
            self.img = self.s5
            self.y -=2
        if animate == 12:
            self.img = self.s6
            self.y +=2
        if animate == 14:
            self.img = self.s7
            self.y +=6
        if animate == 16:
            self.img = self.s8
            self.y +=8
        if animate == 18:
            self.img = self.s9
            self.y = self.originaly
        if animate == 20:
            self.img = self.s10
            self.y = self.originaly
        if self.x > targetx: #slimes move left
            if groundmove == -player.vel: 
                groundmove = player.vel
            elif groundmove == player.vel:
                groundmove = -player.vel
            self.x -= (2 + 2*groundmove) #monster speed is effected by the players speed if the player is walking towards or away from the monster
        elif self.x < targetx: #slimes move right
            self.x += (2 + 2*groundmove)
        if self.x < xlimitr+75:
            
            self.x = xlimitr+75
        if self.x > xlimitl-75:
            
            self.x = xlimitl-75

    def __str__(self):
        return(self.slimerect)
    def render(self):
        window.blit(self.img, (self.x, self.y))
        self.slimerect = Rect(self.x, self.y, self.img.get_size()[0] , self.img.get_size()[1])
       
class Mounts:
    def __init__(self, displacement):
        self.x = 0
        self.y = 0
        self.displacement = displacement
    def locate(self, x):
        self.x = x
        # if self.x == 800:
        #     self.x=0
        #     for m in MountsList:
        #         m.displacement+=400
        # elif self.x == -800:
        #     self.x=0
        #     for m in MountsList:
        #         m.displacement-=400
    def render(self):
        window.blit(mounts, (self.x - self.displacement, self.y))

class Clouds:
    def __init__(self, displacement):
        self.x = 0
        self.y = 0
        self.displacement = displacement
    def locate(self, x):
        self.x = x
    def render(self):
        window.blit(clouds, (self.x - self.displacement, self.y))

def generatemonsters(multyplyer):
    if len(monsters) < multyplyer*player.score+1: #only 10 slimes on the map at a time
        for p in map1:
            if p[3] != 'f':
                block = map1.index(p)
                yspot = p[0]-30
                endofground = (((p[2]*60)+p[1]))
                xranges = random.choice([p[1], endofground])

                if player.playerrect.colliderect(xranges-120, yspot, 240, 30):# player collides with slime
                    pass
                else:
                    monsters.append(Monsters(xranges, yspot, block))

        xranges = random.choice([-800, 800])
        monsters.append(Monsters(xranges, 510))

def tiles(map1, groundmove, tile):
    for z in map1:
        wy = z[0]
        wx = z[1]
        blocks = z[2]
        z[1]+=groundmove
        for d in range(z[2]+1):
            if d > 1:
                wx+= 60
            if z[3] == 'g':
                window.blit(tile, (wx, wy))
            elif z[3] == 'f':
                window.blit(fin, (wx, wy))
            elif z[3] == 'l':
                window.blit(lava, (wx, wy))

def coins(coinsmap, groundmove, coin):
    for c in coinsmap:
        c[1]+=groundmove
        window.blit(coin, (c[1], c[0])) 


def Collision(m, coinsmap):
    if m != 0:
        if player.playerrect.colliderect(m.__str__()):# player collides with slime
             player.health -= 1
             if player.health == 0:
                return False
        if m.__str__().colliderect(bullet.x, bullet.y, 10, 5):# bullet collides with slime
            return('kill')
    for c in coinsmap:
        if player.playerrect.colliderect(c[1], c[0], 20, 32):
            coinsmap.remove(c)
            player.score+=1
def die():
    youdied = fontbig.render('You died', True, (0,0,0))    
    for x in range(0, 100): 
        window.fill((x*.0001, 250-x, x))
        window.blit(youdied, (100, 300))
        pygame.display.flip()
        time.sleep(0.01)
    gameloop = False
    pygame.quit()
player = Player(268, 475)
bullet = Bullet(0, 0)

MountsList = []
MountsList.append(Mounts(0))
MountsList.append(Mounts(-800))
MountsList.append(Mounts(800)) 

CloudsList = []
CloudsList.append(Clouds(0))
CloudsList.append(Clouds(-800))
CloudsList.append(Clouds(800))
lencoins = 5
gameLoop = True
while gameLoop:
    fps = font.render('FPS: '+str(int(clock.get_fps())), True, (black))
    score = font.render('Score: '+str(player.score)+'/'+str(lencoins), True, (0,0,0))
    level = font.render('Level: '+str(player.level), True, (0,0,0))
    window.fill(blue)

    for m in MountsList:
        m.locate(cloudx / 2)
    for c in CloudsList:
        c.locate(cloudx / 4)
    
    for c in CloudsList:
        c.render()
    for m in MountsList:
        m.render()
    window.blit(bg, (x, 536))
    window.blit(bg2, (x2, 536)) 
    
    
    animate +=1
    player.x = 268
    if animate == 21:
        animate = 1 
    #window.fill(white)
    window.blit(bg, (x, 536))
    window.blit(bg2, (x2, 536)) 
    window.blit(score, (20, 20))
    window.blit(level, (20, 40))
    window.blit(fps, (20, 60))
#=============================================
    keys = pygame.key.get_pressed()
    #left
    if keys[pygame.K_a]:

        if collisionl == False:
            groundmove = player.vel 
            player.facing = 'left'
            if animate == 1:
                player.state = player.PlayerRun1L
            if animate == 5:
                player.state = player.PlayerRun2L
            if animate == 10:
                player.state = player.PlayerRun3L
            if animate == 15:
                player.state = player.PlayerRun4L
            x += groundmove 
            playerx+=groundmove
            cloudx += groundmove

            if x > 0:
               x = -71.428571429

        elif collisionl == True:
            groundmove = 0

    else:
        if groundmove == player.vel:
            groundmove = 0

    #right
    if keys[pygame.K_d]:
        if collisionr == False:
            groundmove = -player.vel 
            player.facing = 'right'
            if animate == 1:
                player.state = player.PlayerRun1
            if animate == 5:
                player.state = player.PlayerRun2
            if animate == 10:
                player.state = player.PlayerRun3
            if animate == 15:
                player.state = player.PlayerRun4
     
            x += groundmove
            playerx+=groundmove
            cloudx+=groundmove
            if x <= -212:
                x = 0 

        elif collisionr == True:
            groundmove = 0

    else:
        if groundmove == -player.vel:
            groundmove = 0

    li = list((str(keys)).split(", ")) # list of all keys 0 not pressed 1 pressed 

    if keys[pygame.K_w] or jump == 1:
        player.state = player.PlayerIdle
        jump = 1
        if jumpcount > 0:
            player.y -= jumpupspeed
            jumpcount -=1
        else:
            if (int(li[26]) == 0 and (collisiontop==True or player.y==475)) or (collisiontop==True or player.y==475): #if collisiontop==True or player.y==475 is removed you cant repeatedly jump
                jumpcount = 30
                jump = 0 


    if keys[pygame.K_SPACE]:
        if bullet.shot == False:
            shootsound.play()

            bullet.shoot(player.x, player.y, player.facing)

            if player.facing == 'right':
                player.state = player.PlayerShootIdle

            else:
                player.state = player.PlayerShootIdleL
    #print(li[4], li[7]) #a d
    if (set(keys) == {0, 0}) : #no keys are pressed
        groundmove = 0 

        if player.facing == 'right':
            player.state = player.PlayerIdle
        else:
            player.state = player.PlayerIdleL

#=================================================

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False

    if animate%10 == 0: #generate monsters 1 once every 10 loops
         
        generatemonsters(lencoins)
    
    for m in monsters: #move monsters and check for collisions


        if animate%2 == 0:
            m.move(player.x, groundmove)
        m.render()
        check = Collision(m, coinsmap)
        if check == 'kill': #bullet hits monster
            bullet.x = -10
            bullet.y = -10
            monsters.remove(m)
        if check == False:    #you died
            die()
                

      #check for collision if there are no monsters
    check = Collision(0, coinsmap)

    
    for j in map1:  

        endofground = (((j[2]*60)))
        tilesrect = Rect(0, j[0]-35, endofground, 34)
        tilesrect.move_ip(j[1], 34)
        if j == map1[0]: 
            collisiontop = False
            collisionl = False
            collisionr = False
            onfin = False
        if player.playerrect.colliderect(tilesrect.x, tilesrect.y+10, endofground, 34):#collision on bottom side
            jumpcount = 0
        if player.playerrect.colliderect(tilesrect.x, tilesrect.y-5, endofground, 34):#collision on top side
            collisiontop = True
            if j[3] == 'f':
                onfin=True
            if j[3] == 'l':
                die()
        if player.playerrect.colliderect(tilesrect.x+5, tilesrect.y, endofground, 34): #collision on right side
            collisionl = True
        if player.playerrect.colliderect(tilesrect.x-5, tilesrect.y, endofground, 34): #collision on left side
            collisionr = True

    if player.y != 475 and collisiontop == False: #gravity

        player.y += gravityspeed
    if player.y > 475:
        player.y=475

    
    if bullet.x >= bullet.range: #bullet range
        bullet.x = -10
        bullet.y = -10
    if player.score == lencoins and onfin == True:#next level
        player.level += 1
        #scorenxtlvl=len(coinslist)
        player.score=0
        coinsmap = coinslist[player.level-1]
        map1 = levelslist[player.level-1]
        level = fontbig.render('Level: '+str(player.level), True, (64,255,25))
        monsters.clear()
        lencoins=len(coinsmap)
        for x in range(100): 
            window.fill((0, 0, x))
            window.blit(level, (100+2*x, 300))
            pygame.display.flip()
            time.sleep(.01)
        player.y=475

    tiles(map1, groundmove, tile) #show the grounds
    coins(coinsmap, groundmove, coin)
    bullet.update()
    bullet.render()
    player.render()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


