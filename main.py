import pygame
import os
pygame.font.init()

WIN = pygame.display.set_mode((0,0))
WIDTH, HEIGHT = WIN.get_width(),WIN.get_height()
pygame.display.set_caption("EDMEDLEY")

CAR_IMAGE_PNG = pygame.image.load(os.path.join('Assets','car.png'))
SCALE = .1
CAR_IMAGE=pygame.transform.scale(CAR_IMAGE_PNG, ((int)(WIDTH*SCALE),(int)(HEIGHT*SCALE)))

def draw_window():
    WIN.fill((155,155,155))
    WIN.blit(CAR_IMAGE,(WIDTH//2-CAR_IMAGE.get_width()//2,(int)(HEIGHT*.75)-CAR_IMAGE.get_height()//2))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.key.get_focused and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        draw_window()
    pygame.quit()

if __name__ == "__main__":
    main()