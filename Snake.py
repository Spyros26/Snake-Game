#Snake Game

import sys
import random
import pygame


class cube(object):
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = side // rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))

        if eyes:
            centre = dis//2
            radius = 3
            circleMmiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis+dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMmiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

            

class snack(object):
    def __init__(self, place, color=(150,40,0)):
        self.pos = place
        self.color = color
      

    def draw(self, surface):
        dis = side // rows
        radius = dis // 2
        r = 2
        i = self.pos[0]
        j = self.pos[1]
        circleMiddle = (i*dis+radius, j*dis+radius)
        circleMiddle1 = (i*dis+radius-6, j*dis+radius-1)
        circleMiddle2 = (i*dis+radius+4, j*dis+radius-1)
        circleMiddle3 = (i*dis+radius+4, j*dis+radius+6)
        circleMiddle4 = (i*dis+radius-3, j*dis+radius+5)
        circleMiddle5 = (i*dis+radius, j*dis+radius-5) 
        pygame.draw.circle(surface, self.color, circleMiddle, radius)
        pygame.draw.circle(surface, (0,0,0), circleMiddle1, r)
        pygame.draw.circle(surface, (0,0,0), circleMiddle2, r) 
        pygame.draw.circle(surface, (0,0,0), circleMiddle3, r)
        pygame.draw.circle(surface, (0,0,0), circleMiddle4, r)
        pygame.draw.circle(surface, (0,0,0), circleMiddle5, r) 



class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 1
        self.dirny = 0

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
                    continue
                elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
                    continue
                elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
                    continue
                elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
                    continue 
                elif keys[pygame.K_LEFT] and self.dirnx != 1:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT] and self.dirnx != -1:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP] and self.dirny != 1:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN] and self.dirny != -1:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= rows-1: c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= rows-1:  c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], rows-1)
                else: c.move(c.dirnx,c.dirny)


    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 1
        self.dirny = 0 


    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)
                

def redrawWindow(surface):
    surface.fill((0,0,0)) 
    s.draw(surface)
    snake_snack.draw(surface)
    snake_supersnack.draw(surface)
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)


def main():
    global side, rows, s, snake_snack, snake_supersnack, count
    pygame.init()
    side = 600
    rows = 30
    win = pygame.display.set_mode((side, side))
    s = snake((255,0,0), (15,15))
    snake_snack = snack(randomSnack(rows, s))
    #no supersanck to begin with
    snake_supersnack = snack((-1,-1))
    flag = True
    clock = pygame.time.Clock()
    count = 0
    tick_count = 0

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        tick_count += 1
        s.move()
        if s.body[0].pos == snake_snack.pos:
            count += 1
            s.addCube()
            snake_snack = snack(randomSnack(rows, s))
            if count%3 == 0:
                snake_supersnack = snack(randomSnack(rows, s), (0,255,0))
                tick_count = 0
                
        if s.body[0].pos == snake_supersnack.pos:
            s.addCube()
            s.addCube()
            snake_snack = snack(randomSnack(rows, s))
            # "delete" supersnack
            snake_supersnack = snack((-1,-1))

        # "delete" supersnack if 2.5 seconds have passed
        if tick_count > 25:
            snake_supersnack = snack((-1,-1))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print('Score: ', len(s.body))
                s.reset((15,15))
                snake_supersnack = snack((-1,-1))
                count = 0
                break

        redrawWindow(win)


main()
    
