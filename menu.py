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
        # Adds Display Main Menu event to event queue which is then handled in the main to start displaying the menu.
        pg.event.post(pg.event.Event(self.DISP_MAIN_MENU))

    # Handles Main Menu of game, makes and displays the background, title, and play and quit buttons.
    def displayMainMenu(self):
        play_btn = Button(image=pg.image.load("Assets/Play_Rect.png"), pos=(self.mid_w, self.mid_h+40), 
                            text_input="PLAY", font=get_font(70), base_color="#d7fcd4", hovering_color="White")
        quit_btn = Button(image=pg.image.load("Assets/Quit_Rect.png"), pos=(self.mid_w, self.mid_h+200), 
                            text_input="QUIT", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        
        self.WIN.blit(pg.image.load("Assets/background.png"), (0,0))
        title_text = get_font(100).render("EDMEDLEY", True, "#b68f40")
        title_rect = title_text.get_rect(center=(self.mid_w, self.mid_h-200))
        self.WIN.blit(title_text, title_rect)

        # Updates interface based on user's cursor, handles hovering and click animations along with button functionality.
        run_main_menu_display = True
        while run_main_menu_display:
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

    # Handles Game Select screen of game, makes and displays the background and title 
    # Handles minigame thumbnail buttons and play again and home buttons.
    def displayGameSelect(self):
        car_btn = Button(image=pg.image.load("Assets/Car_thumbnail.png"), pos=(self.mid_w-400, self.mid_h), 
                            text_input="", font=get_font(60), base_color="#d7fcd4", hovering_color="White", image2=pg.image.load("Assets/Car_thumbnail_outline.png"))
        animal_btn = Button(image=pg.image.load("Assets/Animal_thumbnail.png"), pos=(self.mid_w, self.mid_h), 
                            text_input="", font=get_font(60), base_color="#d7fcd4", hovering_color="White", image2=pg.image.load("Assets/Animal_thumbnail_outline.png"))
        spelling_btn = Button(image=pg.image.load("Assets/Spelling_thumbnail.png"), pos=(self.mid_w+400, self.mid_h), 
                            text_input="", font=get_font(60), base_color="#d7fcd4", hovering_color="White", image2=pg.image.load("Assets/Spelling_thumbnail_outline.png"))
        back_btn = Button(image=pg.image.load("Assets/Back_Rect.png"), pos=(self.mid_w-500, self.mid_h+250), 
                            text_input="BACK", font=get_font(40), base_color="#d7fcd4", hovering_color="White")                
        start_btn = Button(image=pg.image.load("Assets/Start_Rect.png"), pos=(self.mid_w+500, self.mid_h+250), 
                            text_input="START", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        self.WIN.blit(pg.image.load("Assets/background.png"), (0,0))
        title_text = get_font(80).render("Game Select", True, "#b68f40")
        title_rect = title_text.get_rect(center=(self.mid_w, self.mid_h-200))
        self.WIN.blit(title_text, title_rect)
        
        # Updates interface based on user's cursor, handles hovering and click animations along with button functionality.
        run_game_select_display = True
        while run_game_select_display:
            mouse_pos = pg.mouse.get_pos()
            for button in [car_btn, animal_btn, spelling_btn, back_btn, start_btn]:
                button.changeColor(mouse_pos)
                button.changeOutline(mouse_pos)
                button.update(self.WIN)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    if car_btn.checkForInput(mouse_pos):
                        car_btn.update(self.WIN)
                        if "car" in self.listOfMinigames:
                            self.listOfMinigames.remove("car")
                        else:
                            self.listOfMinigames.append("car")
                    if animal_btn.checkForInput(mouse_pos):
                        animal_btn.update(self.WIN)
                        if "animals" in self.listOfMinigames:
                            self.listOfMinigames.remove("animals")
                        else:
                            self.listOfMinigames.append("animals")
                    if spelling_btn.checkForInput(mouse_pos):
                        spelling_btn.update(self.WIN)
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

    # Handles End Screen of game, makes and displays the background, title, current and 
    # high scores, along with making and handling play again and home buttons.
    def displayEndScreen(self, currentScore, highScore):
        play_again_btn = Button(image=pg.image.load("Assets/Play_Again_Rect.png"), pos=(self.mid_w+400, self.mid_h+270), 
                            text_input="PLAY AGAIN", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        home_btn = Button(image=pg.image.load("Assets/Back_Rect.png"), pos=(self.mid_w-500, self.mid_h+270), 
                            text_input="HOME", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        self.WIN.blit(pg.image.load("Assets/background.png"), (0,0))

        # Displays current and high score
        title_text = get_font(100).render("GAME OVER", True, "#b68f40")
        title_rect = title_text.get_rect(center=(self.mid_w, self.mid_h-200))
        self.WIN.blit(title_text, title_rect)

        curr_score_text1 = get_font(60).render("CURRENT", True, "White")
        curr_score_rect1 = curr_score_text1.get_rect(center=(self.mid_w-310, self.mid_h-60))
        self.WIN.blit(curr_score_text1, curr_score_rect1)
        
        curr_score_text2 = get_font(60).render("SCORE:", True, "White")
        curr_score_rect2 = curr_score_text2.get_rect(center=(self.mid_w-310, self.mid_h-60 + curr_score_text1.get_height()))
        self.WIN.blit(curr_score_text2, curr_score_rect2)

        curr_score_text3 = get_font(60).render(str(currentScore), True, "White")
        curr_score_rect3 = curr_score_text3.get_rect(center=(self.mid_w-310, self.mid_h-60 + curr_score_text1.get_height() + curr_score_text2.get_height()))
        self.WIN.blit(curr_score_text3, curr_score_rect3)
        
        high_score_text1 = get_font(60).render("HIGH", True, "White")
        high_score_rect1 = high_score_text1.get_rect(center=(self.mid_w+310, self.mid_h-60))
        self.WIN.blit(high_score_text1, high_score_rect1)

        high_score_text2 = get_font(60).render("SCORE:", True, "White")
        high_score_rect2 = high_score_text2.get_rect(center=(self.mid_w+310, self.mid_h-60 + high_score_text1.get_height()))
        self.WIN.blit(high_score_text2, high_score_rect2)

        high_score_text3 = get_font(60).render(str(highScore), True, "White")
        high_score_rect3 = high_score_text3.get_rect(center=(self.mid_w+310, self.mid_h-60 + high_score_text1.get_height() + high_score_text2.get_height()))
        self.WIN.blit(high_score_text3, high_score_rect3)

        # Updates interface based on user's cursor, handles hovering and click animations along with button functionality.
        run_end_screen_display = True
        while run_end_screen_display:
            mouse_pos = pg.mouse.get_pos()
            for button in [play_again_btn, home_btn]:
                button.changeColor(mouse_pos)
                button.update(self.WIN)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    if play_again_btn.checkForInput(mouse_pos):
                        pg.event.post(pg.event.Event(self.START_GAME))
                        run_end_screen_display=False
                    if home_btn.checkForInput(mouse_pos):
                        self.listOfMinigames.clear()
                        pg.event.post(pg.event.Event(self.DISP_MAIN_MENU))
                        run_end_screen_display=False
            pg.display.update()