from pydoc import render_doc
import pygame as pg
import os

pg.font.init()

from Spelling_Minigame import Spelling_Minigame

#Test Game Parameters
os.environ["SDL_VIDEODRIVER"] = "dummy"
pg.init()
WIN = pg.display.set_mode((1280,720));
SCALE = 0.2;
NEXT_MINI = pg.USEREVENT + 1;
duration = 3000;

class Test_minigame:

    #Testing that loading existing images works.
    def test_1(self):
        testMinigame = Spelling_Minigame(WIN, SCALE, NEXT_MINI, duration);
        assert(testMinigame.loadImages(['notebook_background.png', 'pencil.png'])) == None;

    #Testing that loading non-existing images works.
    def test_2(self):
        testMinigame = Spelling_Minigame(WIN, SCALE, NEXT_MINI, duration);
        assert(testMinigame.loadImages(['doesntNotExist.png'])) == None;

    #Testing that loading any kind of image works.
    def test_3(self):
        testMinigame = Spelling_Minigame(WIN, SCALE, NEXT_MINI, duration);
        assert(testMinigame.loadImages(['pencil.png', 'doesntNotExist.png'])) == None;

    #Testing that loading no images works.
    def test_4(self):
        testMinigame = Spelling_Minigame(WIN, SCALE, NEXT_MINI, duration);
        assert(testMinigame.loadImages([])) == None;

    #Testing that existing image can scale.
    def test_5(self):
        testMinigame = Spelling_Minigame(WIN, SCALE, NEXT_MINI, duration);
        assert(testMinigame.initScaleImage('pencil', 1, 1)) == True;

    #Testing that non-existing image leaves gracefully.
    def test_6(self):
        testMinigame = Spelling_Minigame(WIN, SCALE, NEXT_MINI, duration);
        assert(testMinigame.initScaleImage('non-existant', 1, 1)) == False;

    #Testing that image can safely scale by 0.
    def test_7(self):
        testMinigame = Spelling_Minigame(WIN, SCALE, NEXT_MINI, duration);
        assert(testMinigame.initScaleImage('pencil', 0, 0)) == True;

    #Testing that image can gracefully leave after scaling by negative.
    def test_8(self):
        testMinigame = Spelling_Minigame(WIN, SCALE, NEXT_MINI, duration);
        assert(testMinigame.initScaleImage('pencil', -1, -1)) == False;

    #Testing non-existant image gets placeholder rectangle.
    def test_9(self):
        testMinigame = Spelling_Minigame(WIN, SCALE, NEXT_MINI, duration);
        assert(testMinigame.initImageObjectRect('non-existant', 0, 0)) == pg.Rect(0, 0, 420, 420);

    #Testing having out of bounds image doesn't break.
    def test_10(self):
        testMinigame = Spelling_Minigame(WIN, SCALE, NEXT_MINI, duration);
        assert(testMinigame.initImageObjectRect('pencil', 10000, -1000)) != pg.Rect(0, 0, 420, 420);

#All the Minigames above this mark test general Minigame methods and don't have to be repeated.