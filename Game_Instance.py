from random import randint
import pygame as pg
pg.font.init()

from Minigame_Queue import Minigame_Queue
from Car_Minigame import Car_Minigame
from Spelling_Minigame import Spelling_Minigame
from Animals_Minigame import Animals_Minigame

class Game_Instance:
    
    def __init__(self, WIN, SCALE, LIST_OF_MINIGAMES, NEXT_MINI, GO_TO_TRANSITION, ADVANCE_TO_MINI, DISP_END_SCREEN, PLAY_TESTING_MODE, STABILITY_TESTING_MODE):
        self.WIN = WIN;
        self.SCALE = SCALE;
        self.listOfMinigames = LIST_OF_MINIGAMES;

        self.PLAY_TESTING_MODE = PLAY_TESTING_MODE;
        self.STABILITY_TESTING_MODE = STABILITY_TESTING_MODE;
        MINIGAME_TESTING_MODE_SPEED = 1;
        TRANSITION_TESTING_MODE_SPEED = 1;

        self.NEXT_MINI = NEXT_MINI;
        self.GO_TO_TRANSITION = GO_TO_TRANSITION;
        self.ADVANCE_TO_MINI = ADVANCE_TO_MINI;
        self.DISP_END_SCREEN = DISP_END_SCREEN;

        #States for the Game Instance
        self.isMinigameInitialized = False;
        self.isGoingToWinLoseScreen = False;
        self.isTransitioning = False;
        self.firstTransition = True; #Used to ensure that the score is updated only once, perhaps could be done cleaner with an event flag

        self.minigameNumber = 1;

        self.minigameCurrentDuration = MINIGAME_TESTING_MODE_SPEED
        self.transitionCurrentDuration = TRANSITION_TESTING_MODE_SPEED

        if(not STABILITY_TESTING_MODE):
            self.minigameStartDuration = 5000
            self.minigameEndDuration = 2000
            self.minigameCurrentDuration = self.durationCalculator(self.minigameStartDuration, self.minigameEndDuration);

            self.transitionStartDuration = 750
            self.transitionEndDuration = 350
            self.transitionCurrentDuration = self.durationCalculator(self.transitionStartDuration, self.transitionEndDuration);

        self.minigameQueue = Minigame_Queue(3);

        if(not pg.font.get_init):
                pg.font.init;
        self.font = pg.font.Font('Assets/FreeSansBold.ttf', 150);

        while(not self.minigameQueue.isFull()):
            self.minigameQueue.addToMinigameQueue(self.addRandomMinigame());
            
        self.currentRunningMinigame = None;
        pg.event.post(pg.event.Event(self.ADVANCE_TO_MINI));

        self.lastMinigameAnswer = False
        self.score = 0
        self.losses = 0

        return

    def tickGameInstance(self):
        #Checks if application is in minigame playing mode 
        if(self.isMinigameInitialized):
            if(self.currentRunningMinigame != None):
                self.currentRunningMinigame.run_minigame();
            else:
                #Probably change to a stop minigames, return to menu event
                pg.event.post(pg.event.Event(pg.QUIT));
                return
            self.firstTransition=True #constantly sets to true but only needs to do so once when the next minigame loads/could be made more efficient
            self.lastMinigameAnswer = self.currentRunningMinigame.correctAnswer() #same issue as above but with the answer key

        #Checks if application is in transition mode
        if(self.isTransitioning):
            #Determines what part of the two part transition is playing, the win/loss or minigame num
            if (self.isGoingToWinLoseScreen):
                if(self.firstTransition):
                    #If correct, else if not
                    if(self.lastMinigameAnswer):
                        self.score+=1
                    else:
                        self.losses += 1;
                        # print(self.losses)
                    self.firstTransition = False;
                scoreText, scoreRect = self.createScoreText()
                winLoseText, winLoseRect = self.createWinLose()
                self.draw_win_lose_window(scoreText, scoreRect, winLoseText, winLoseRect);
            else:
                transitionText, transitionRect = self.createTransition();
                self.draw_transition_window(transitionText, transitionRect);

        return

    def stateHandlerGameInstance(self, eventId):
        #Event fires when the minigame ends, shows scores and win/lose
        if eventId == self.NEXT_MINI:

            self.isMinigameInitialized = False;
            self.isGoingToWinLoseScreen = True;
            self.isTransitioning = True;

            #Calculate the times here for organization
            if(not self.STABILITY_TESTING_MODE):
                self.transitionCurrentDuration = self.durationCalculator(self.transitionStartDuration, self.transitionEndDuration);
                self.minigameCurrentDuration = self.durationCalculator(self.minigameStartDuration, self.minigameEndDuration);

            pg.time.set_timer(self.GO_TO_TRANSITION, self.transitionCurrentDuration, 1);

        #Event fires when time ends for win/lose screen, shows minigame number
        if eventId == self.GO_TO_TRANSITION:

            #Check to see if we lose before going onto next minigame
            if(self.losses >= 3 and not (self.PLAY_TESTING_MODE or self.STABILITY_TESTING_MODE)):
                #Switich to transition to end menu
                pg.event.post(pg.event.Event(self.DISP_END_SCREEN));
                return
            
            self.minigameNumber = self.minigameNumber + 1;
            self.isGoingToWinLoseScreen = False;
            pg.time.set_timer(self.ADVANCE_TO_MINI, self.transitionCurrentDuration, 1);

        #Event fires when transition is done, loads next minigame
        if eventId == self.ADVANCE_TO_MINI:
            
            self.currentRunningMinigame = self.minigameQueue.getFromMinigameQueue();
            while(not self.minigameQueue.isFull()):
                self.minigameQueue.addToMinigameQueue(self.addRandomMinigame());

            #Fail-safe if queue is somehow empty at loading
            if(self.currentRunningMinigame == None):
                print("Minigame failed to load");
                pg.event.post(pg.event.Event(pg.QUIT));
                return

            self.isTransitioning = False;

            #Initializes the minigame once and begins running
            if(not self.isMinigameInitialized):
                self.currentRunningMinigame.startRunningMinigame();
                self.isMinigameInitialized = True;

        return

    def getScore(self):
        return self.score;

    def createScoreText(self):
        scoreText = self.font.render("Score: " + str(self.score), True, (255, 255, 255));
        scoreRect = scoreText.get_rect();
        scoreRect.center = (640, 560);    
        return scoreText, scoreRect;

    def createTransition(self):
        transitionText = self.font.render("Minigame #" + str(self.minigameNumber), True, (255, 255, 255));
        transitionRect = transitionText.get_rect();
        transitionRect.center = (640, 360);    
        return transitionText, transitionRect;

    def createWinLose(self):
        winLoseText = None;
        winLoseRect = None;
        if(self.lastMinigameAnswer):
            winLoseText = self.font.render("WIN!", True, (255, 255, 255));
        else:
            winLoseText = self.font.render("LOSS!", True, (255, 255, 255));

        winLoseRect = winLoseText.get_rect();
        winLoseRect.center = (640, 360);    
        return winLoseText, winLoseRect;

    def draw_win_lose_window(self, scoreText, scoreRect, winLoseText, winLoseRect):
        if(self.lastMinigameAnswer):
            self.WIN.fill((0, 200, 0));
        else:
            self.WIN.fill((200, 0, 0));
        if(winLoseText is not None and winLoseRect is not None): 
            self.WIN.blit(winLoseText, winLoseRect)
        if(scoreText is not None and scoreRect is not None): 
            self.WIN.blit(scoreText, scoreRect)
        pg.display.update();
        return

    def draw_transition_window(self, transitionText, transitionRect):
        self.WIN.fill((0, 0, 0));
        if(transitionText is not None and transitionRect is not None):
            self.WIN.blit(transitionText, transitionRect)
        pg.display.update();
        return

    def durationCalculator(self, startDuration, endDuration):
        if(self.minigameNumber >= 30):
            return endDuration;
        result = int(endDuration + (startDuration - endDuration) * pow(2, -0.25 * self.minigameNumber));
        if(result <= 0):
            return 1;
        return result;

    def addRandomMinigame(self):
        length = len(self.listOfMinigames);
        choice = self.listOfMinigames[randint(0, length - 1)];

        if(choice == 'car'):
            return Car_Minigame(self.WIN, self.SCALE, self.NEXT_MINI, self.minigameCurrentDuration);
        elif(choice == 'spell'):
            return Spelling_Minigame(self.WIN, self.SCALE, self.NEXT_MINI, self.minigameCurrentDuration);
        elif(choice == 'animals'):
            return Animals_Minigame(self.WIN, self.SCALE, self.NEXT_MINI, self.minigameCurrentDuration);

        return Car_Minigame(self.WIN, self.SCALE, self.NEXT_MINI, self.minigameCurrentDuration);
