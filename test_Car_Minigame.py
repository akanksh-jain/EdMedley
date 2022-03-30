from pydoc import render_doc
import pygame as pg
import os
pg.font.init()

from Car_Minigame import Car_Minigame

class Test_minigame:

    #Testing that loading existing images works.
    def test_one(self):
        WIN = pg.display.set_mode((1280,720))
        SCALE = 0.2;
        NEXT_MINI = pg.USEREVENT + 1;
        testMinigame = Car_Minigame(WIN, SCALE, NEXT_MINI);

        assert(testMinigame.loadImages(['car.png', 'Cactus_Short.png', 'Cactus_Tall.png', 'road.png'])) == None;

    #Testing that loading non-existing images works.
    def test_two(self):
        WIN = pg.display.set_mode((1280,720))
        SCALE = 0.2;
        NEXT_MINI = pg.USEREVENT + 1;
        testMinigame = Car_Minigame(WIN, SCALE, NEXT_MINI);

        assert(testMinigame.loadImages(['doesntNotExist.png'])) == None;

    #Testing that loading any kind of image works.
    def test_three(self):
        WIN = pg.display.set_mode((1280,720))
        SCALE = 0.2;
        NEXT_MINI = pg.USEREVENT + 1;
        testMinigame = Car_Minigame(WIN, SCALE, NEXT_MINI);

        assert(testMinigame.loadImages(['car.png', 'doesntNotExist.png'])) == None;

    #Testing that loading no images works.
    def test_four(self):
        WIN = pg.display.set_mode((1280,720))
        SCALE = 0.2;
        NEXT_MINI = pg.USEREVENT + 1;
        testMinigame = Car_Minigame(WIN, SCALE, NEXT_MINI);

        assert(testMinigame.loadImages([])) == None;