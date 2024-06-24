import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((500, 500),pygame.SCALED, vsync=1)
clock = pygame.time.Clock()
x,y = 50,50
xm,ym = 0,0
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            xm=(event.key == K_RIGHT)-(event.key == K_LEFT)
            ym=(event.key == K_DOWN)-(event.key == K_UP)
        if event.type == KEYUP:
            xm = xm - xm*(event.key == K_RIGHT)-xm*(event.key == K_LEFT)
            ym = ym - ym*(event.key == K_DOWN)+ym*(event.key == K_UP)
    x=x+xm*4
    y=y+ym*4
    pygame.draw.rect(screen, [255, 255, 255], [x, y, 160, 160])
    pygame.display.update()
    pygame.display.set_caption("FPS: %.2f" % clock.get_fps())
    clock.tick(60)
pygame.quit()