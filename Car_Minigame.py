from pydoc import render_doc
import pygame as pg
import os
pg.font.init()
import random
from Minigame import Minigame

#Need to add win/lose condition and exit event so minigame queue knows to load next game.
class Car_Minigame(Minigame):
    
    def __init__(self, WIN, SCALE, NEXT_MINI):
        super().__init__(WIN, SCALE, NEXT_MINI);

        self.WIDTH = WIN.get_width();
        self.HEIGHT = WIN.get_height();

        #Simply list the names of the files you want to load, will auto load them for you, named after their file name sans file type
        self.imageSet = {};
        self.loadImages(['car.png', 'Cactus_Short.png', 'Cactus_Tall.png', 'road.png']);
        self.transformImages();

        self.CURRENT_POS = 0;
        self.rumbleUp = True;
        self.rumbleDistance = 2;
        self.move_timer = 100

        if(not pg.font.get_init):
            pg.font.init;
        self.font = pg.font.Font('freesansbold.ttf', 150);

        self.createObjects();

    def startRunningMinigame(self):
        #Will need to change to event that moves the queue foward
        print("New Minigame")
        pg.time.set_timer(self.NEXT_MINI, 5000, 1);

    def correctAnswer(self):
        if self.answerKey-2==self.CURRENT_POS:
            return True
        else:
            return False

    def createSignObject(self, sign1text, sign2text, sign3text):
        self.sign_1 = pg.Rect(80, 100, 300, 250);
        self.sign_1_border = pg.Rect(80, 100, 300, 250);
        self.sign_1_text = self.font.render(str(sign1text), True, (255, 255, 255));
        self.sign_1_text_rect = self.sign_1_text.get_rect();
        self.sign_1_text_rect.center = (200, 175);

        self.sign_2 = pg.Rect(480, 100, 300, 250);
        self.sign_2_border = pg.Rect(480, 100, 300, 250);
        self.sign_2_text = self.font.render(str(sign2text), True, (255, 255, 255));
        self.sign_2_text_rect = self.sign_1_text.get_rect();
        self.sign_2_text_rect.center = (600, 175);

        self.sign_3 = pg.Rect(880, 100, 300, 250);
        self.sign_3_border = pg.Rect(880, 100, 300, 250);
        self.sign_3_text = self.font.render(str(sign3text), True, (255, 255, 255));
        self.sign_3_text_rect = self.sign_1_text.get_rect();
        self.sign_3_text_rect.center = (1000, 175);

    def chooseAnswers(self, listAns, listSub1, listSub2):
        correctSign = random.randint(1,3)
        self.answerKey=correctSign
        answer = listAns[random.randint(0, len(listAns) - 1)];
        wrong1 = listSub1[random.randint(0, len(listSub1) - 1)];
        wrong2 = listSub2[random.randint(0, len(listSub2) - 1)];
        if correctSign==1:
            self.createSignObject(answer,wrong1,wrong2)
        elif correctSign==2:
            self.createSignObject(wrong1,answer,wrong2)
        else:
            self.createSignObject(wrong2,wrong1,answer)

    #Where initial image transformations should be organized
    def transformImages(self):
        self.initScaleImage('car', 0.9, 1);
        self.initScaleImage('Cactus_Short', 0.5, 0.5);
        self.initScaleImage('Cactus_Tall', 1, 2);
        self.initScaleImage('road', 3, 1.25);

    #Mixture of image object creation and basic geometry creation, may need to organize this later
    def createObjects(self):
        self.car = self.initImageObjectRect('car', self.WIDTH // 2 - self.imageSet['car'].get_width() // 2,(int)(self.HEIGHT * .75) - self.imageSet['car'].get_height() // 2 - self.rumbleDistance // 2)
        self.cactus_short = self.initImageObjectRect('Cactus_Short', 60, int(self.HEIGHT * .75) - self.imageSet['Cactus_Short'].get_height())
        self.cactus_tall = self.initImageObjectRect('Cactus_Tall', 950, int(self.HEIGHT * .75) - self.imageSet['Cactus_Tall'].get_height())

        self.road_first = self.initImageObjectRect('road', self.WIDTH // 2 - self.imageSet['road'].get_width() // 2, (int)(self.HEIGHT) - self.imageSet['road'].get_height())
        self.road_second = self.initImageObjectRect('road', self.WIDTH // 2 - self.imageSet['road'].get_width() // 2, (int)(self.HEIGHT) - 2 * self.imageSet['road'].get_height())

        self.ground = pg.Rect(0, int(self.HEIGHT * .75), self.WIDTH, self.HEIGHT - int(self.HEIGHT * .75))
        self.sky = pg.Rect(0, 0, self.WIDTH, int(self.HEIGHT * .75))

        self.bar_top = pg.Rect(0, 120, self.WIDTH, 40)
        question_mode = random.randint(0, 1);

        odds = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49];
        evens = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50];

        if question_mode==0: #Evens
            self.chooseAnswers(evens,odds,odds)
        else:
            self.chooseAnswers(odds,evens,evens)       


    def run_minigame(self):
        if(self.rumbleUp):
            self.car.y -= self.rumbleDistance
        else:
            self.car.y += self.rumbleDistance
        self.rumbleUp = not self.rumbleUp;

        keys_pressed = pg.key.get_pressed()
        self.handle_car_movement(keys_pressed);
        self.handle_cactus_movements();
        self.handle_road_movements();
        self.draw_window()

    def draw_window(self):
        self.move_timer+=1
        self.WIN.fill((155,155,155))
        #Ground and Sky
        pg.draw.rect(self.WIN, (255, 200, 50), self.ground)
        self.WIN.blit(self.imageSet['road'],(self.road_first.x, self.road_first.y))
        self.WIN.blit(self.imageSet['road'],(self.road_second.x, self.road_second.y))
        pg.draw.rect(self.WIN, (100, 175, 255), self.sky)

        pg.draw.rect(self.WIN, (200, 200, 200), self.bar_top)

        #Sign 1, 2, 3
        pg.draw.rect(self.WIN, (0, 175, 0), self.sign_1)
        pg.draw.rect(self.WIN, (255,255,255), self.sign_1_border, 4, border_radius= 15)
        self.WIN.blit(self.sign_1_text, self.sign_1_text_rect)

        pg.draw.rect(self.WIN, (0, 175, 0), self.sign_2)
        pg.draw.rect(self.WIN, (255,255,255), self.sign_2_border, 4, border_radius= 15)
        self.WIN.blit(self.sign_2_text, self.sign_2_text_rect)

        pg.draw.rect(self.WIN, (0, 175, 0), self.sign_3)
        pg.draw.rect(self.WIN, (255,255,255), self.sign_3_border, 4, border_radius= 15)
        self.WIN.blit(self.sign_3_text, self.sign_3_text_rect)

        self.WIN.blit(self.imageSet['Cactus_Short'],(self.cactus_short.x, self.cactus_short.y))
        self.WIN.blit(self.imageSet['Cactus_Tall'],(self.cactus_tall.x, self.cactus_tall.y))
        self.WIN.blit(self.imageSet['car'],(self.car.x, self.car.y))

        pg.display.update()

    def handle_car_movement(self, keys_pressed):
        #Coordinate based system with discrete position, -1 left, 0 center, 1 right

        #Better fix may be a state based system, ex. if moving then animation will play, as long as animation is playing, won't allow movement,
        if self.move_timer<10:
            quit
        elif keys_pressed[pg.K_LEFT] and self.CURRENT_POS != -1:
            self.move_timer=0
            self.CURRENT_POS = self.CURRENT_POS - 1;
            self.car.x-= self.imageSet['car'].get_width()-30

        elif keys_pressed[pg.K_RIGHT] and self.CURRENT_POS != 1:
            self.move_timer=0
            self.CURRENT_POS = self.CURRENT_POS + 1;
            self.car.x += self.imageSet['car'].get_width()-30

    def handle_cactus_movements(self):
        if(self.cactus_short.y >= self.HEIGHT):
            self.cactus_short.y = int(self.HEIGHT * .75) - self.imageSet['Cactus_Short'].get_height()
        self.cactus_short.y = self.cactus_short.y + 20;

        if(self.cactus_tall.y >= self.HEIGHT):
            self.cactus_tall.y = int(self.HEIGHT * .75) - self.imageSet['Cactus_Tall'].get_height()
        self.cactus_tall.y = self.cactus_tall.y + 20;

    def handle_road_movements(self):
        if(self.road_first.y >= self.HEIGHT):
            self.road_first.y = int(self.HEIGHT) - 2 * self.imageSet['road'].get_height()
        self.road_first.y = self.road_first.y + 20;

        if(self.road_second.y >= self.HEIGHT):
            self.road_second.y = int(self.HEIGHT) - 2 * self.imageSet['road'].get_height()
        self.road_second.y = self.road_second.y + 20;
