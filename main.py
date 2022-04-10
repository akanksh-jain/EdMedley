from pydoc import render_doc
from random import randint
import pygame as pg
import os
from pathlib import Path
import json
pg.font.init()

import queue
from Minigame_Queue import Minigame_Queue
from Car_Minigame import Car_Minigame
from Spelling_Minigame import Spelling_Minigame

WIN = pg.display.set_mode((1280,720))
WIDTH, HEIGHT = WIN.get_width(), WIN.get_height()
pg.display.set_caption("EDMEDLEY")

path_to_script = os.path.dirname(os.path.abspath(__file__))
save_file_path = os.path.join(path_to_script, "save_file.json")
save_data={}

SCALE = 0.2;
NEXT_MINI = pg.USEREVENT + 1;
GO_TO_TRANSITION = pg.USEREVENT + 2
ADVANCE_TO_MINI = pg.USEREVENT + 3;

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

def createWinLose(font, lastMinigameAnswer):
    winLoseText = None;
    winLoseRect = None;
    if(lastMinigameAnswer):
        winLoseText = font.render("WIN!", True, (255, 255, 255));
    else:
        winLoseText = font.render("LOSS!", True, (255, 255, 255));

    winLoseRect = winLoseText.get_rect();
    winLoseRect.center = (640, 360);    
    return winLoseText, winLoseRect;


def draw_win_lose_window(scoreText, scoreRect, winLoseText, winLoseRect, lastMinigameAnswer):
    if(lastMinigameAnswer):
        WIN.fill((0, 200, 0));
    else:
        WIN.fill((200, 0, 0));
    if(winLoseText is not None and winLoseRect is not None): 
        WIN.blit(winLoseText, winLoseRect)
    if(scoreText is not None and scoreRect is not None): 
        WIN.blit(scoreText, scoreRect)
    pg.display.update();
    return

def draw_transition_window(transitionText, transitionRect):
    WIN.fill((0, 0, 0));
    if(transitionText is not None and transitionRect is not None):
        WIN.blit(transitionText, transitionRect)
    pg.display.update();
    return

def save(data):
    with open(save_file_path, "w") as save_file:
        json.dump(data, save_file)
        save_file.close()

def durationCalculator(minigameNumber, startDuration, endDuration):
    if(minigameNumber >= 30):
        return endDuration;
    return int(endDuration + (startDuration - endDuration) * pow(2, -0.25 * minigameNumber));

def addRandomMinigame(listOfMinigames, minigameCurrentDuration):
    length = len(listOfMinigames);
    choice = listOfMinigames[randint(0, length - 1)];

    if(choice == 'car'):
        return Car_Minigame(WIN, SCALE, NEXT_MINI, minigameCurrentDuration);
    elif(choice == 'spell'):
        return Spelling_Minigame(WIN, SCALE, NEXT_MINI, minigameCurrentDuration);

    return Car_Minigame(WIN, SCALE, NEXT_MINI, minigameCurrentDuration);

def main():

    #For testing to see if game crashes at some point, slow down to check graphical stability
    STABILITY_TESTING_MODE = False;
    MINIGAME_TESTING_MODE_SPEED = 1;
    TRANSITION_TESTING_MODE_SPEED = 1;

    PLAY_TESTING_MODE = False;

    file = Path(save_file_path)
    file.touch(exist_ok=True)
    if os.stat(save_file_path).st_size == 0:
        save_data = {
            "high score" : 0
        }
        save(save_data)
    else:
        with open(file, "r") as save_file:
            save_data = json.load(save_file)
            save_file.close()
    if len(save_data) == 0:
        save_data = {
            "high score" : 0
        }
    clock = pg.time.Clock();
    
    run = True;
    isMinigameInitialized = False;
    isGoingToWinLoseScreen = False;
    isTransitioning = False;
    firstTransition = True; #Used to ensure that the score is updated only once, perhaps could be done cleaner with an event flag

    listOfMinigames = ['car', 'spell']

    minigameNumber = 0;

    minigameCurrentDuration = MINIGAME_TESTING_MODE_SPEED
    transitionCurrentDuration = TRANSITION_TESTING_MODE_SPEED

    if(not STABILITY_TESTING_MODE):
        minigameStartDuration = 5000
        minigameEndDuration = 2000
        minigameCurrentDuration = durationCalculator(minigameNumber, minigameStartDuration, minigameEndDuration);

        transitionStartDuration = 750
        transitionEndDuration = 350
        transitionCurrentDuration = durationCalculator(minigameNumber, transitionStartDuration, transitionEndDuration);

    minigameQueue = Minigame_Queue(3);
    while(not minigameQueue.isFull()):
        minigameQueue.addToMinigameQueue(addRandomMinigame(listOfMinigames, minigameCurrentDuration));
        
    currentRunningMinigame = None;
    pg.event.post(pg.event.Event(ADVANCE_TO_MINI));

    if(not pg.font.get_init):
            pg.font.init;
    font = pg.font.Font('freesansbold.ttf', 150);

    transitionText = None;
    transitionRect = None;
    scoreText = None
    scoreRect = None
    lastMinigameAnswer=False
    score = 0
    losses = 0

    while run:
        clock.tick(30)
        for event in pg.event.get():
            #Event fires when the minigame ends, shows scores and win/lose
            if event.type == NEXT_MINI:
                isMinigameInitialized = False;
                isGoingToWinLoseScreen = True;
                isTransitioning = True;

                #Calculate the times here for organization
                if(not STABILITY_TESTING_MODE):
                    transitionCurrentDuration = durationCalculator(minigameNumber, transitionStartDuration, transitionEndDuration);
                    minigameCurrentDuration = durationCalculator(minigameNumber, minigameStartDuration, minigameEndDuration);

                pg.time.set_timer(GO_TO_TRANSITION, transitionCurrentDuration, 1);

            #Event fires when time ends for win/lose screen, shows minigame number
            if event.type == GO_TO_TRANSITION:
                minigameNumber = minigameNumber + 1;
                isGoingToWinLoseScreen = False;
                transitionText, transitionRect = createTransition(font, minigameNumber);
                pg.time.set_timer(ADVANCE_TO_MINI, transitionCurrentDuration, 1);

            #Event fires when transition is done, loads next minigame
            if event.type == ADVANCE_TO_MINI:
                currentRunningMinigame = minigameQueue.getFromMinigameQueue();
                while(not minigameQueue.isFull()):
                    minigameQueue.addToMinigameQueue(addRandomMinigame(listOfMinigames, minigameCurrentDuration));

                #Fail-safe if queue is somehow empty at loading
                if(currentRunningMinigame == None):
                    print("Minigame failed to load");
                    run = False;

                isTransitioning = False;

                #Initializes the minigame once and begins running
                if(not isMinigameInitialized):
                    currentRunningMinigame.startRunningMinigame();
                    isMinigameInitialized = True;

            if event.type == pg.QUIT:
                run = False
            
            if pg.key.get_focused and event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False

        #Checks if application is in minigame playing mode 
        if(isMinigameInitialized):
            if(currentRunningMinigame != None):
                currentRunningMinigame.run_minigame();
            else:
                #Probably change to a stop minigames, return to menu event
                run = False;
            firstTransition=True #constantly sets to true but only needs to do so once when the next minigame loads/could be made more efficient
            lastMinigameAnswer = currentRunningMinigame.correctAnswer() #same issue as above but with the answer key

        #Checks if application is in transition mode
        if(isTransitioning):
            #Determines what part of the two part transition is playing, the win/loss or minigame num
            if (isGoingToWinLoseScreen):
                if(firstTransition):
                    #If correct, else if not
                    if(lastMinigameAnswer):
                        score+=1
                        if score > save_data["high score"]:
                            save_data["high score"] = score
                    else:
                        losses += 1;
                        print(losses)
                    firstTransition = False;
                scoreText, scoreRect = createScoreText(font,score)
                winLoseText, winLoseRect = createWinLose(font, lastMinigameAnswer)
                draw_win_lose_window(scoreText, scoreRect, winLoseText, winLoseRect, lastMinigameAnswer);
            else:
                draw_transition_window(transitionText, transitionRect);

    save(save_data)

    pg.quit()

if __name__ == "__main__":
    main()