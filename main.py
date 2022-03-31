from pydoc import render_doc
import pygame as pg
import os
pg.font.init()

import queue
from Minigame_Queue import Minigame_Queue
from Car_Minigame import Car_Minigame

WIN = pg.display.set_mode((1280,720))
WIDTH, HEIGHT = WIN.get_width(), WIN.get_height()
pg.display.set_caption("EDMEDLEY")

SCALE = 0.2;
NEXT_MINI = pg.USEREVENT + 1;
ADVANCE_TO_MINI = pg.USEREVENT + 2;

def createScoreText(font,score):
    scoreText = font.render("Score: " + str(score), True, (255, 255, 255));
    scoreRect = scoreText.get_rect();
    scoreRect.center = (640, 560);    
    return scoreText, scoreRect;

def createTransition(font, minigameNumber):
    transitionText = font.render("Minigame #" + str(minigameNumber), True, (255, 255, 255));
    transitionRect = transitionText.get_rect();
    transitionRect.center = (640, 360);    
    return transitionText, transitionRect;

def draw_window(font, minigameNumber, transitionText, transitionRect, scoreText, scoreRect):
    WIN.fill((0, 0, 0));
    if(transitionText is not None and transitionRect is not None):
        WIN.blit(transitionText, transitionRect)
    if(scoreText is not None and scoreRect is not None): 
        WIN.blit(scoreText, scoreRect)
    pg.display.update();
    return

def main():
    clock = pg.time.Clock();
    run = True;
    isMinigameInitialized = False;
    isTransitioning = False;
    firstTransition = True; #Used to ensure that the score is updated only once, perhaps could be done cleaner with an event flag

    minigameQueue = Minigame_Queue(3);
    while(not minigameQueue.isFull()):
        minigameQueue.addToMinigameQueue(Car_Minigame(WIN, SCALE, NEXT_MINI));
        
    currentRunningMinigame = None;
    minigameNumber = 0;
    pg.event.post(pg.event.Event(NEXT_MINI));

    if(not pg.font.get_init):
            pg.font.init;
    font = pg.font.Font('freesansbold.ttf', 150);

    transitionText = None;
    transitionRect = None;
    scoreText = None
    scoreRect = None
    lastMinigameAnswer=False
    score=0

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
                currentRunningMinigame = minigameQueue.getFromMinigameQueue();
                while(not minigameQueue.isFull()):
                    minigameQueue.addToMinigameQueue(Car_Minigame(WIN, SCALE, NEXT_MINI));

                if(currentRunningMinigame == None):
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
            if(currentRunningMinigame != None):
                currentRunningMinigame.run_minigame();
            else:
                #Probably change to a stop minigames, return to menu event
                run = False;
            firstTransition=True #constantly sets to true but only needs to do so once when the next minigame loads/could be made more efficient
            lastMinigameAnswer = currentRunningMinigame.correctAnswer() #same issue as above but with the answer key
        else:
            if lastMinigameAnswer and firstTransition: #Does not display the score until a point is earned/ unsure if this should be the intended functionality
                score+=1
                scoreText, scoreRect = createScoreText(font,score);
                firstTransition=False
            draw_window(font, minigameNumber, transitionText, transitionRect, scoreText, scoreRect);

    pg.quit()

if __name__ == "__main__":
    main()