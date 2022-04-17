from pydoc import render_doc
import pygame as pg
import os

pg.font.init()

from Game_Instance import Game_Instance

#Test Game Parameters
os.environ["SDL_VIDEODRIVER"] = "dummy"
pg.init()
WIN = pg.display.set_mode((1280,720));

NEXT_MINI = pg.USEREVENT + 1;
GO_TO_TRANSITION = pg.USEREVENT + 2
ADVANCE_TO_MINI = pg.USEREVENT + 3;
DISP_END_SCREEN = pg.USEREVENT + 14;

SCALE = 0.2;

class Test_minigame:

    #Play game speed up for a while and check if it crashes
    def test_stability(self):
        listOfMinigames = ['car', 'spell', 'animals']
        Game = Game_Instance(WIN, SCALE, listOfMinigames, NEXT_MINI, GO_TO_TRANSITION, ADVANCE_TO_MINI, DISP_END_SCREEN, False, True);

        clock = pg.time.Clock();
        pg.time.set_timer(pg.QUIT, 7000, 1);
        run = True;
        while run:
            clock.tick(30)
            for event in pg.event.get():
                #Event fires when the minigame ends, shows scores and win/lose
                if event.type == NEXT_MINI:
                    Game.stateHandlerGameInstance(NEXT_MINI);

                #Event fires when time ends for win/lose screen, shows minigame number
                if event.type == GO_TO_TRANSITION:
                    Game.stateHandlerGameInstance(GO_TO_TRANSITION);

                #Event fires when transition is done, loads next minigame
                if event.type == ADVANCE_TO_MINI:
                    Game.stateHandlerGameInstance(ADVANCE_TO_MINI);

                if event.type == pg.QUIT:
                    run = False
                
                if pg.key.get_focused and event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        run = False

            Game.tickGameInstance()

