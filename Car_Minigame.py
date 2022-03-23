from pydoc import render_doc
import pygame as pg
import os
pg.font.init()

#Need to add win/lose condition and exit event so minigame queue knows to load next game.
class Car_Minigame():
    
    def __init__(self, WIN, SCALE):
        self.WIN = WIN;
        self.SCALE = SCALE;

        self.WIDTH = WIN.get_width();
        self.HEIGHT = WIN.get_height();

        #Simply list the names of the files you want to load, will auto load them for you, named after their file name sans file type
        self.imageSet = {};
        self.loadImages(['car.png', 'Cactus_Short.jpg', 'Cactus_Tall.png']);
        self.transformImages();

        self.CURRENT_POS = 0;
        self.rumbleUp = True;
        self.rumbleDistance = 2;

        if(not pg.font.get_init):
            pg.font.init;
        self.font = pg.font.Font('freesansbold.ttf', 150);

        self.createObjects();

    #May need to check if image name doesn't exist
    def loadImages(self, listOfImageNames):
        for name in listOfImageNames:
            self.imageSet.update({name[0:-4] : pg.image.load(os.path.join('Assets', name)).convert()})

    #Automatically checks if image is loaded and does global scaling itself, manual scaling still present
    def initScaleImage(self, name, manWidth, manHeight):
        if name in self.imageSet:
            self.imageSet[name] = pg.transform.scale(self.imageSet[name], ((int)(self.WIDTH * self.SCALE * manWidth), (int)(self.HEIGHT * self.SCALE * manHeight)))
            return
        print("Scaling failed, '" + name + "' is not a valid image.");

    #Where initial image transformations should be organized
    def transformImages(self):
        self.initScaleImage('car', 0.9, 1);
        self.initScaleImage('Cactus_Short', 0.5, 0.5);
        self.initScaleImage('Cactus_Tall', 1, 2);

    #Creates the rectangle for a certain image, only needs x and y position and image name
    def initImageObjectRect(self, name, xpos, ypos):
        if name in self.imageSet:
            return pg.Rect(xpos, ypos, self.imageSet[name].get_width(), self.imageSet[name].get_height())
        print("Object creation failed, '" + name + "' is not a valid image.");

    #Mixture of image object creation and basic geometry creation, may need to organize this later
    def createObjects(self):
        self.car = self.initImageObjectRect('car', self.WIDTH // 2 - self.imageSet['car'].get_width() // 2,(int)(self.HEIGHT * .75) - self.imageSet['car'].get_height() // 2 - self.rumbleDistance // 2)
        self.cactus_short = self.initImageObjectRect('Cactus_Short', 60, int(self.HEIGHT * .75) - self.imageSet['Cactus_Short'].get_height())
        self.cactus_tall = self.initImageObjectRect('Cactus_Tall', 950, int(self.HEIGHT * .75) - self.imageSet['Cactus_Tall'].get_height())

        self.ground = pg.Rect(0, int(self.HEIGHT * .75), self.WIDTH, self.HEIGHT - int(self.HEIGHT * .75))
        self.sky = pg.Rect(0, 0, self.WIDTH, int(self.HEIGHT * .75))
        self.sign_1 = pg.Rect(30, 100, 300, 250);
        self.sign_1_border = pg.Rect(30, 100, 300, 250);
        self.sign_1_text = self.font.render('50', True, (255, 255, 255));
        self.sign_1_text_rect = self.sign_1_text.get_rect();
        self.sign_1_text_rect.center = (165, 175);

    def run_minigame(self):
        if(self.rumbleUp):
            self.car.y -= self.rumbleDistance
        else:
            self.car.y += self.rumbleDistance
        self.rumbleUp = not self.rumbleUp;

        keys_pressed = pg.key.get_pressed()
        self.handle_car_movement(keys_pressed);
        self.handle_cactus_movements();
        self.draw_window()

    def draw_window(self):
        self.WIN.fill((155,155,155))
        pg.draw.rect(self.WIN, (255, 200, 50), self.ground)
        pg.draw.rect(self.WIN, (100, 175, 255), self.sky)

        pg.draw.rect(self.WIN, (0, 175, 0), self.sign_1)
        pg.draw.rect(self.WIN, (255,255,255), self.sign_1_border, 4, border_radius= 15)
        self.WIN.blit(self.sign_1_text, self.sign_1_text_rect)

        self.WIN.blit(self.imageSet['Cactus_Short'],(self.cactus_short.x, self.cactus_short.y))
        self.WIN.blit(self.imageSet['Cactus_Tall'],(self.cactus_tall.x, self.cactus_tall.y))
        self.WIN.blit(self.imageSet['car'],(self.car.x, self.car.y))

        pg.display.update()

    def handle_car_movement(self, keys_pressed):
        #Coordinate based system with discrete position, -1 left, 0 center, 1 right

        #Still need to fix this delay thing, shouldn't be pausing the minigame, maybe count ticks since last movement?
        if keys_pressed[pg.K_LEFT] and self.CURRENT_POS != -1:
            pg.time.delay(100)
            self.CURRENT_POS = self.CURRENT_POS - 1;
            self.car.x-= self.imageSet['car'].get_width()

        if keys_pressed[pg.K_RIGHT] and self.CURRENT_POS != 1:
            pg.time.delay(100)
            self.CURRENT_POS = self.CURRENT_POS + 1;
            self.car.x += self.imageSet['car'].get_width()

    def handle_cactus_movements(self):
        if(self.cactus_short.y >= self.HEIGHT):
            self.cactus_short.y = int(self.HEIGHT * .75) - self.imageSet['Cactus_Short'].get_height()
        self.cactus_short.y = self.cactus_short.y + 20;

        if(self.cactus_tall.y >= self.HEIGHT):
            self.cactus_tall.y = int(self.HEIGHT * .75) - self.imageSet['Cactus_Tall'].get_height()
        self.cactus_tall.y = self.cactus_tall.y + 20;
