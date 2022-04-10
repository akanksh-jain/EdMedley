from pydoc import render_doc
import pygame as pg
import os
pg.font.init()
import random
from Minigame import Minigame

class Spelling_Minigame(Minigame):

    def __init__(self, WIN, SCALE, NEXT_MINI):
        super().__init__(WIN, SCALE, NEXT_MINI);

        self.WIDTH = WIN.get_width();
        self.HEIGHT = WIN.get_height();

        #Simply list the names of the files you want to load, will auto load them for you, named after their file name sans file type
        self.imageSet = {};
        self.loadImages(['notebook_background.png', 'pencil.png']);
        self.transformImages();

        self.CURRENT_POS = 0;
        self.rumbleUp = True;
        self.rumbleDistance = 2;
        self.move_timer = 100;
        self.tutorial_timer = 0;

        if(not pg.font.get_init):
            pg.font.init;
        self.font = pg.font.Font('freesansbold.ttf', 150);
        self.tutorial_font = pg.font.Font('freesansbold.ttf', 100);

        self.createObjects();
        #self.createAnswerChoices();

    def transformImages(self):
        self.initScaleImage('pencil', 0.9, 1)

    def createObjects(self):
        self.pencil = self.initImageObjectRect('pencil', self.WIDTH // 2 - self.imageSet['pencil'].get_width() // 2,(int)(self.HEIGHT * .75) - self.imageSet['pencil'].get_height() // 2 - self.rumbleDistance // 2)
        self.background = pg.transform.scale(pg.image.load(os.path.join('Assets','notebook_background.png')),(1280,720))

    def startRunningMinigame(self):
        #Will need to change to event that moves the queue foward
        print("New Minigame")
        pg.time.set_timer(self.NEXT_MINI, self.duration, 1);
    
    def createTutorialText(self, question_mode):
        self.tutorial_text=self.tutorial_font.render("Choose the Correct Spelling", True, (255, 255, 255))
        self.tutorial_rect=self.tutorial_text.get_rect()
        self.tutorial_rect.center = (600, 50)
        
    def run_minigame(self):
        keys_pressed = pg.key.get_pressed()
        self.handle_pencil_movement(keys_pressed)
        self.draw_window()

    def draw_window(self):
        self.move_timer+=1
        self.WIN.blit(self.background,(0,0))
        self.WIN.blit(self.imageSet['pencil'],(self.pencil.x, self.pencil.y))
        self.drawTimer();
        pg.display.update()

    def correctAnswer(self):
        if self.answerKey-2==self.CURRENT_POS:
            return True
        else:
            return False

    def handle_pencil_movement(self, keys_pressed):
        if self.move_timer<10:
            quit
        elif keys_pressed[pg.K_LEFT] and self.CURRENT_POS != -1:
            self.move_timer=0
            self.CURRENT_POS = self.CURRENT_POS - 1;
            self.pencil.x-= self.imageSet['pencil'].get_width()-30

        elif keys_pressed[pg.K_RIGHT] and self.CURRENT_POS != 1:
            self.move_timer=0
            self.CURRENT_POS = self.CURRENT_POS + 1;
            self.pencil.x += self.imageSet['pencil'].get_width()-30