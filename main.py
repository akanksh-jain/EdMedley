import pygame as pg
import os
from pathlib import Path
import json
pg.font.init()

from Game_Instance import Game_Instance

WIN = pg.display.set_mode((1280,720))
WIDTH, HEIGHT = WIN.get_width(), WIN.get_height()
pg.display.set_caption("EDMEDLEY")

path_to_script = os.path.dirname(os.path.abspath(__file__))
save_file_path = os.path.join(path_to_script, "save_file.json")
save_data={}

NEXT_MINI = pg.USEREVENT + 1;
GO_TO_TRANSITION = pg.USEREVENT + 2
ADVANCE_TO_MINI = pg.USEREVENT + 3;

SCALE = 0.2;

def save(data):
    with open(save_file_path, "w") as save_file:
        json.dump(data, save_file)
        save_file.close()

def main():

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

    listOfMinigames = ['car', 'spell', 'animals']

    Game = Game_Instance(WIN, SCALE, listOfMinigames, NEXT_MINI, GO_TO_TRANSITION, ADVANCE_TO_MINI, False, True);

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
        if Game.getScore() > save_data["high score"]:
            save_data["high score"] = Game.getScore()


    save(save_data)

    pg.quit()

if __name__ == "__main__":
    main()