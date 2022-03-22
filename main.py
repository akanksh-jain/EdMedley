from pydoc import render_doc
import pygame as pg
import os
pg.font.init()

from Car_Minigame import Car_Minigame

WIN = pg.display.set_mode((1280,720))
WIDTH, HEIGHT = WIN.get_width(), WIN.get_height()
pg.display.set_caption("EDMEDLEY")

SCALE = 0.2;

def draw_window():
    return

def main():
    clock = pg.time.Clock();
    run = True;
    #Minigames shouldn't be created in the wild like this, minigame queue should fix this issue.
    minigame1 = Car_Minigame(WIN, SCALE);

    while run:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            
            if pg.key.get_focused and event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
        #Queue should also fix minigames running the while.
        minigame1.run_minigame();

    pg.quit()

if __name__ == "__main__":
    main()