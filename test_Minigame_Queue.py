from pydoc import render_doc
import pygame as pg
import os
pg.font.init()

from Minigame_Queue import Minigame_Queue
from Car_Minigame import Car_Minigame

WIN = pg.display.set_mode((1280,720));
SCALE = 0.2;
NEXT_MINI = pg.USEREVENT + 1;

class Test_minigame_queue:

    #Adding Minigame to unfull queue succeeds.
    def test_1(self):
        minigameQueue = Minigame_Queue(3);
        testMinigame = Car_Minigame(WIN, SCALE, NEXT_MINI);
        assert(minigameQueue.addToMinigameQueue(Car_Minigame(WIN, SCALE, NEXT_MINI))) == True;

    #Adding Minigame to full queue fails gracefully.
    def test_2(self):
        minigameQueue = Minigame_Queue(1);
        testMinigame = Car_Minigame(WIN, SCALE, NEXT_MINI);
        minigameQueue.addToMinigameQueue(Car_Minigame(WIN, SCALE, NEXT_MINI));
        assert(minigameQueue.isFull()) == True;
        assert(minigameQueue.addToMinigameQueue(Car_Minigame(WIN, SCALE, NEXT_MINI))) == False;

    #Getting minigame from queue succeeds.
    def test_3(self):
        minigameQueue = Minigame_Queue(3);
        testMinigame = Car_Minigame(WIN, SCALE, NEXT_MINI);
        minigameQueue.addToMinigameQueue(Car_Minigame(WIN, SCALE, NEXT_MINI));
        assert(minigameQueue.getFromMinigameQueue()) != None;

    #Getting minigame from empty queue fails gracefully.
    def test_4(self):
        minigameQueue = Minigame_Queue(1);
        testMinigame = Car_Minigame(WIN, SCALE, NEXT_MINI);
        assert(minigameQueue.isEmpty()) == True;
        assert(minigameQueue.getFromMinigameQueue()) == None;
