from pydoc import render_doc
import pygame as pg
import os

pg.font.init()

from Animals_Minigame import Animals_Minigame

#Test Game Parameters
os.environ["SDL_VIDEODRIVER"] = "dummy"
pg.init()
WIN = pg.display.set_mode((1280,720));
SCALE = 0.2;
NEXT_MINI = pg.USEREVENT + 1;
duration = 3000;

class Test_Minigame:

    #Tests loading in of all animal minigame images
    def test_1(self):
        testMinigame = Animals_Minigame(WIN, SCALE, NEXT_MINI, duration);
        assert(testMinigame.loadImages(['Detective_room.png', 'Mag_glass.png', 'Fish.png', 'Frog.png', 'Giraffe.png', 'Ladybug.png', 'Bird.png', 'Seagull.png', 'Lizard.png', 'Ant.png', 'Dolphin.png', 'Monkey.png', 'Snake.png', 'Axolotl.png', 'Swordfish.png'])) == None;

    #Tests
    def test_2(self):
        testMinigame = Animals_Minigame(WIN, SCALE, NEXT_MINI, duration);
        assert(testMinigame.transformImages) == None;
    
    def test_3(self):
        testMinigame = Animals_Minigame(WIN, SCALE, NEXT_MINI, duration);
        assert(testMinigame.createObjects) == None;

    #def test_4(self):
