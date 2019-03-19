import pygame
import functions.init as init

class decor(pygame.sprite.Sprite):
    def __init__(self, name, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.name         = name
        self.image        = image
        self.rect         = self.image.get_rect()
        self.rect.x,self.rect.y  = position
        

class birdObj(pygame.sprite.Sprite):
    def __init__(self, name, image, position,radius,cloud,crush,state="normal"):
        pygame.sprite.Sprite.__init__(self)
        self.name         = name
        self.state        = state
        self.image        = image
        self.rect         = self.image.get_rect()
        self.rect.center  = position
        self.radius       = radius

        self.imageNormal  = image
        self.imageCloud   = cloud
        self.imageCrush   = crush
        self.pointnb      = -1
        self.points       = []

    def update(self):
        if self.state    == "normal":
            self.image    = self.imageNormal
        elif self.state  == "cloud":
            self.image    = self.imageCloud
        elif self.state  == "crush":
            self.image    = self.imageCrush
        if self.pointnb >= 0:
            self.move()

    def move(self):
        if self.pointnb == len(self.points): 
            # Animation : nuage de disparition
            pygame.time.wait(200)
            self.state = "cloud"
            self.pointnb+=1
            return

        if self.pointnb == len(self.points)+1: # si dernier point passé, effacer les listes,numeros...
            pygame.time.wait(650)
            self.state = "normal"
            self.pointnb            = -1
            self.points             = 0
            init.inMove = False
            return

        i=self.points[self.pointnb]

        if i[0] - 153 >= 0 or i[1] - 150 <= 0:
            init.line1.end_pos = (160, 177)
            init.line1.width = 20
            init.line2.width = 0
        else :
            init.line1.end_pos = (i[0] - 10, i[1] - 2)
            init.line1.width = 7
            init.line2.end_pos = (i[0] - 10, i[1])
            init.line2.width = 7

        if i == self.points[-2]: # On passe a l'état crush à l'avant dernier point            
            self.state = "crush"

        self.rect.center    = i
        self.pointnb        += 1


class pigObj(pygame.sprite.Sprite):
    def __init__(self, name, image, position,radius,cloud):
        pygame.sprite.Sprite.__init__(self)
        self.name         = name
        self.image        = image
        self.rect         = self.image.get_rect()
        self.rect.center  = position
        self.radius       = radius
        self.imageCloud   = cloud
        self.die          = False
        self.countdown    = 0
    
    def update(self):
        for i in init.middle:
            if i != self and type(i) == birdObj and pygame.sprite.collide_circle(self, i):
                self.disparait()
        if self.die == True and self.countdown < 7:
            self.countdown += 1
        elif self.die == True and self.countdown >= 7:
            self.kill()

    def disparait(self):
        self.image    = self.imageCloud
        self.die   = True



class lineObj(pygame.sprite.Sprite):
    def __init__(self, color, start_pos, end_pos, width=1):
        pygame.sprite.Sprite.__init__(self)
        self.color        = color
        self.start_pos    = start_pos
        self.end_pos      = end_pos
        self.end_posLast      = end_pos
        self.width        = width
        self.widthLast    = width
        self.image        = pygame.Surface([init.WIDTH,init.HEIGHT], pygame.SRCALPHA, 32)
        self.image        = self.image.convert_alpha()
        pygame.draw.line(self.image, self.color, self.start_pos, self.end_pos, self.width)
        self.rect         = self.image.get_rect()

    def update(self):
        if self.end_pos != self.end_posLast or self.width != self.widthLast: #update only if modification made
            self.image            = pygame.Surface([init.WIDTH,init.HEIGHT], pygame.SRCALPHA, 32)
            self.image            = self.image.convert_alpha()
            pygame.draw.line(self.image, self.color, self.start_pos, self.end_pos, self.width)
            self.rect             = self.image.get_rect()
            self.end_posLast      = self.end_pos
            self.widthLast        = self.width
