import pygame
import os
pygame.font.init()

WIN = pygame.display.set_mode((0,0))
WIDTH, HEIGHT = WIN.get_width(),WIN.get_height()
pygame.display.set_caption("EDMEDLEY")

def draw_window():
    WIN.fill((155,155,155))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN and pygame.key.get_focused:
                if event.key == pygame.K_ESCAPE:
                    run = False
        draw_window()
    pygame.quit()

if __name__ == "__main__":
    main()