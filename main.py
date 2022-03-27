from asyncio.windows_events import NULL
from pydoc import render_doc
import pygame as pg
import os
pg.font.init()

import queue
from Car_Minigame import Car_Minigame

WIN = pg.display.set_mode((1280,720))
WIDTH, HEIGHT = WIN.get_width(), WIN.get_height()
pg.display.set_caption("EDMEDLEY")

SCALE = 0.2;
NEXT_MINI = pg.USEREVENT + 1;
ADVANCE_TO_MINI = pg.USEREVENT + 2;

def createTransition(font, minigameNumber):
    transitionText = font.render("Minigame #" + str(minigameNumber), True, (255, 255, 255));
    transitionRect = transitionText.get_rect();
    transitionRect.center = (640, 360);    
    return transitionText, transitionRect;

def draw_window(font, minigameNumber, transitionText, transitionRect):
    WIN.fill((0, 0, 0));
    if(transitionText is not NULL and transitionRect is not NULL):
        WIN.blit(transitionText, transitionRect)
    pg.display.update();
    return

def main():
    clock = pg.time.Clock();
    run = True;
    isMinigameInitialized = False;
    isTransitioning = False;

    queueMaxSize = 3;
    minigameQueue = queue.LifoQueue(queueMaxSize);
    while not minigameQueue.full():
        minigameQueue.put(Car_Minigame(WIN, SCALE, NEXT_MINI));
        
    currentRunningMinigame = NULL;
    minigameNumber = 0;
    pg.event.post(pg.event.Event(NEXT_MINI));

    if(not pg.font.get_init):
            pg.font.init;
    font = pg.font.Font('freesansbold.ttf', 150);

    transitionText = NULL;
    transitionRect = NULL;

    while run:
        clock.tick(30)

        for event in pg.event.get():
            if event.type == NEXT_MINI:
                minigameNumber = minigameNumber + 1;
                isMinigameInitialized = False;
                isTransitioning = True;
                transitionText, transitionRect = createTransition(font, minigameNumber);
                pg.time.set_timer(ADVANCE_TO_MINI, 750, 1);

            if event.type == ADVANCE_TO_MINI:
                if(not minigameQueue.empty()):
                    currentRunningMinigame = minigameQueue.get();
                if(not minigameQueue.full()):
                    minigameQueue.put(Car_Minigame(WIN, SCALE, NEXT_MINI));
                if(currentRunningMinigame == NULL):
                    print("Minigame failed to load");
                    run = False;

                isTransitioning = False;

                if(not isMinigameInitialized):
                    currentRunningMinigame.startRunningMinigame();
                    isMinigameInitialized = True;

            if event.type == pg.QUIT:
                run = False
            
            if pg.key.get_focused and event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False

        if(not isTransitioning):
            currentRunningMinigame.run_minigame();
        else:
            draw_window(font, minigameNumber, transitionText, transitionRect);


    pg.quit()

if __name__ == "__main__":
    main()
