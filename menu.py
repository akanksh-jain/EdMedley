import pygame as pg
import sys

from button import Button

def get_font(size): # Returns Press-Start-2P in the desired size
    return pg.font.Font("Assets/font.ttf", size)

class Menu():
    def __init__(self, WIN, DISP_MAIN_MENU, DISP_GAME_SELECT, START_GAME):
        self.WIN = WIN
        self.listOfMinigames = []
        self.DISP_MAIN_MENU = DISP_MAIN_MENU
        self.DISP_GAME_SELECT = DISP_GAME_SELECT
        self.START_GAME = START_GAME
        self.mid_w, self.mid_h = WIN.get_width() / 2, WIN.get_height() / 2
        pg.event.post(pg.event.Event(self.DISP_MAIN_MENU))

    def eventHandler(self, eventID):
        if eventID == self.DISP_MAIN_MENU:
            self.displayMainMenu()
        if eventID == self.DISP_GAME_SELECT:
            self.displayGameSelect()
            
    def displayMainMenu(self):
        run_main_menu_display = True
        while run_main_menu_display:
            self.WIN.blit(pg.image.load("Assets/background.png"), (0,0))
            title_text = get_font(100).render("EDMEDLEY", True, "#b68f40")
            title_rect = title_text.get_rect(center=(self.mid_w, self.mid_h-200))
            self.WIN.blit(title_text, title_rect)

            play_btn = Button(image=pg.image.load("Assets/Play_Rect.png"), pos=(self.mid_w, self.mid_h+40), 
                            text_input="PLAY", font=get_font(70), base_color="#d7fcd4", hovering_color="White")
            quit_btn = Button(image=pg.image.load("Assets/Quit_Rect.png"), pos=(self.mid_w, self.mid_h+200), 
                            text_input="QUIT", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
            
            mouse_pos = pg.mouse.get_pos()
            for button in [play_btn, quit_btn]:
                button.changeColor(mouse_pos)
                button.update(self.WIN)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    if play_btn.checkForInput(mouse_pos):
                        pg.event.post(pg.event.Event(self.DISP_GAME_SELECT))
                        run_main_menu_display=False
                    if quit_btn.checkForInput(mouse_pos):
                        pg.quit()
                        sys.exit()

            pg.display.update()

    def displayGameSelect(self):
        run_game_select_display = True
        while run_game_select_display:
            self.WIN.blit(pg.image.load("Assets/background.png"), (0,0))
            title_text = get_font(80).render("Game Select", True, "#b68f40")
            title_rect = title_text.get_rect(center=(self.mid_w, self.mid_h-200))
            self.WIN.blit(title_text, title_rect)

            car_btn = Button(image=pg.image.load("Assets/Car_thumbnail.png"), pos=(self.mid_w-400, self.mid_h), 
                            text_input="", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
            animal_btn = Button(image=pg.image.load("Assets/Animal_thumbnail.png"), pos=(self.mid_w, self.mid_h), 
                            text_input="", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
            spelling_btn = Button(image=pg.image.load("Assets/Spelling_thumbnail.png"), pos=(self.mid_w+400, self.mid_h), 
                            text_input="", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
            back_btn = Button(image=pg.image.load("Assets/Back_Rect.png"), pos=(self.mid_w-500, self.mid_h+250), 
                            text_input="BACK", font=get_font(40), base_color="#d7fcd4", hovering_color="White")                
            start_btn = Button(image=pg.image.load("Assets/Start_Rect.png"), pos=(self.mid_w+500, self.mid_h+250), 
                            text_input="START", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

            mouse_pos = pg.mouse.get_pos()
            for button in [car_btn, animal_btn, spelling_btn, back_btn, start_btn]:
                button.changeColor(mouse_pos)
                button.update(self.WIN)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    if car_btn.checkForInput(mouse_pos):
                        if "car" in self.listOfMinigames:
                            self.listOfMinigames.remove("car")
                        else:
                            self.listOfMinigames.append("car")
                    if animal_btn.checkForInput(mouse_pos):
                        if "animals" in self.listOfMinigames:
                            self.listOfMinigames.remove("animals")
                        else:
                            self.listOfMinigames.append("animals")
                    if spelling_btn.checkForInput(mouse_pos):
                        if "spell" in self.listOfMinigames:
                            self.listOfMinigames.remove("spell")
                        else:
                            self.listOfMinigames.append("spell")
                    if back_btn.checkForInput(mouse_pos):
                        self.listOfMinigames.clear()
                        run_game_select_display = False
                        pg.event.post(pg.event.Event(self.DISP_MAIN_MENU))
                    if start_btn.checkForInput(mouse_pos):
                        if len(self.listOfMinigames) == 0:
                            self.listOfMinigames = ["car", "spell", "animals"]
                        run_game_select_display = False
                        pg.event.post(pg.event.Event(self.START_GAME))
            pg.display.update()