import pygame
import os
pygame.font.init()

WIN = pygame.display.set_mode((1280,720))
WIDTH, HEIGHT = WIN.get_width(),WIN.get_height()
pygame.display.set_caption("EDMEDLEY")

CAR_IMAGE_PNG = pygame.image.load(os.path.join('Assets','car.png'))
SCALE = .1
CAR_IMAGE=pygame.transform.scale(CAR_IMAGE_PNG, ((int)(WIDTH*SCALE),(int)(HEIGHT*SCALE)))

VEL=5

def draw_window(car):
    WIN.fill((155,155,155))
    WIN.blit(CAR_IMAGE,(car.x,car.y))
    pygame.display.update()

def handle_car_movement(keys_pressed,car):
    if keys_pressed[pygame.K_LEFT] and car.x>WIDTH//2-(int)(1.5*CAR_IMAGE.get_width()):
        car.x-=CAR_IMAGE.get_width()
    if keys_pressed[pygame.K_RIGHT] and car.x<WIDTH//2+(int)(.5*CAR_IMAGE.get_width()):
        car.x+=CAR_IMAGE.get_width()

def main():
    car=pygame.Rect(WIDTH//2-CAR_IMAGE.get_width()//2,(int)(HEIGHT*.75)-CAR_IMAGE.get_height()//2,CAR_IMAGE.get_width(),CAR_IMAGE.get_height())
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
        keys_pressed=pygame.key.get_pressed()
        handle_car_movement(keys_pressed,car)
        draw_window(car)
    pygame.quit()

if __name__ == "__main__":
    main()