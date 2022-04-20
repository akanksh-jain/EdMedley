from pydoc import render_doc
import pygame as pg
import os
pg.font.init()
import random
from Minigame import Minigame

class Animals_Minigame(Minigame):

    #define aniaml minigame, initilize images and fonts
    def __init__(self, WIN, SCALE, NEXT_MINI, duration):
        super().__init__(WIN, SCALE, NEXT_MINI, duration);

        self.WIDTH = WIN.get_width();
        self.HEIGHT = WIN.get_height();

        self.imageSet = {};
        self.loadImages(['Detective_room.png', 'Mag_glass.png']);
        self.transformImages();

        self.CURRENT_POS = 0;
        self.move_timer = 100;
        self.tutorial_timer = 0;

        if(not pg.font.get_init):
            pg.font.init;
        self.font = pg.font.Font('Assets/FreeSansBold.ttf', 150);
        self.tutorial_font = pg.font.Font('Assets/FreeSansBold.ttf', 100);

        self.createObjects();
        self.createAnswerChoices();

    #transform magnifying glass image
    def transformImages(self):
        self.initScaleImage('Mag_glass', 2, 2.5)
        
    #transform the animal image depending on which animal is being shown on screen
    def transformAnimalImages(self, animal1, animal2, animal3):
        if animal1 == 'Fish':
            self.initScaleImage('Fish', 1, 1)
        elif animal1 == 'Frog':
            self.initScaleImage('Frog', 1.5, 1.5)
        elif animal1 == 'Axolotl':
            self.initScaleImage('Axolotl', 1.5, 1.5)
        elif animal1 == 'Snake':
            self.initScaleImage('Snake', 1.5, 1.5)
        elif animal1 == 'Swordfish':
            self.initScaleImage('Swordfish', 1.8, 1.8)
        elif animal1 == 'Dolphin':
            self.initScaleImage('Dolphin', 1.5, 1.5)
        elif animal1 == 'Monkey':
            self.initScaleImage('Monkey', 2, 2.5)
        elif animal1 == 'Ant':
            self.initScaleImage('Ant', 2, 2)

        if animal2 == 'Fish':
            self.initScaleImage('Fish', 1, 1)
        elif animal2 == 'Frog':
            self.initScaleImage('Frog', 1.5, 1.5)
        elif animal2 == 'Axolotl':
            self.initScaleImage('Axolotl', 1.5, 1.5)
        elif animal2 == 'Snake':
            self.initScaleImage('Snake', 1.5, 1.5)
        elif animal2 == 'Swordfish':
            self.initScaleImage('Swordfish', 1.8, 1.8)
        elif animal2 == 'Dolphin':
            self.initScaleImage('Dolphin', 1.5, 1.5)
        elif animal2 == 'Monkey':
            self.initScaleImage('Monkey', 2, 2.5)
        elif animal2 == 'Ant':
            self.initScaleImage('Ant', 2, 2)

        if animal3 == 'Fish':
            self.initScaleImage('Fish', 1, 1)
        elif animal3 == 'Frog':
            self.initScaleImage('Frog', 1.5, 1.5)
        elif animal3 == 'Axolotl':
            self.initScaleImage('Axolotl', 1.5, 1.5)
        elif animal3 == 'Snake':
            self.initScaleImage('Snake', 1.5, 1.5)
        elif animal3 == 'Swordfish':
            self.initScaleImage('Swordfish', 1.8, 1.8)
        elif animal3 == 'Dolphin':
            self.initScaleImage('Dolphin', 1.5, 1.5)
        elif animal3 == 'Monkey':
            self.initScaleImage('Monkey', 2, 2.5)
        elif animal3 == 'Ant':
            self.initScaleImage('Ant', 2, 2)

    #create the background image and magnifying glass as an object to be shown on screen
    def createObjects(self):
        self.background = pg.transform.scale(self.imageSet['Detective_room'], (1280,720))
        self.mag_glass = self.initImageObjectRect('Mag_glass', (self.WIDTH // 2 - self.imageSet['Mag_glass'].get_width() // 2) + 50, (int)(self.HEIGHT * .6) - self.imageSet['Mag_glass'].get_height() // 2)

    #determine which text for selection will be presented based on what the answer is
    def createTutorialText(self, question_mode):
        #if answer is a bird, display bird text
        if question_mode == 0:
            self.tutorial_text = self.tutorial_font.render("Select the Bird", True, (0,0,0))
        elif question_mode == 1:
            self.tutorial_text = self.tutorial_font.render("Select the Mammal", True, (0,0,0))
        elif question_mode == 2:
            self.tutorial_text = self.tutorial_font.render("Select the Reptile", True, (0,0,0))
        elif question_mode == 3:
            self.tutorial_text = self.tutorial_font.render("Select the Insect", True, (0,0,0))
        elif question_mode == 4:
            self.tutorial_text = self.tutorial_font.render("Select the Fish", True, (0,0,0))
        elif question_mode == 5:
            self.tutorial_text = self.tutorial_font.render("Select the Amphibian", True, (0,0,0))

        #transform text to rectangle, center it onto the screen
        self.tutorial_rect = self.tutorial_text.get_rect()
        self.tutorial_rect.center = (600,50)

    #get player input of keys, draw the window on users screen
    def run_minigame(self):
        keys_pressed = pg.key.get_pressed()
        self.handle_mag_glass_movement(keys_pressed);
        self.draw_window()
        
    #draws window with background and animal sprites
    def draw_window(self):
        #update move timer of mag_glass
        self.move_timer += 1
        self.WIN.blit(self.background,(0,0))
        
        self.WIN.blit(self.imageSet[self.animalname1], (self.animal1.x, self.animal1.y))
        self.WIN.blit(self.imageSet[self.animalname2], (self.animal2.x, self.animal2.y))
        self.WIN.blit(self.imageSet[self.animalname3], (self.animal3.x, self.animal3.y))

        self.WIN.blit(self.imageSet['Mag_glass'], (self.mag_glass.x, self.mag_glass.y))

        #display tutorial text for certain amount of time
        if self.tutorial_timer < 70:
            self.tutorial_timer += 1
            self.WIN.blit(self.tutorial_text,self.tutorial_rect)

        self.drawTimer();
        pg.display.update()

    #defines if answer choosen by user is the correct answer
    def correctAnswer(self):
        if self.answerKey - 2 == self.CURRENT_POS:
            return True
        else:
            return False

    #handles mag glass movement based on users input
    def handle_mag_glass_movement(self, keys_pressed):
        #only allow movement after 10 updates, so movement is not rapid
        if self.move_timer < 10:
            return
        elif keys_pressed[pg.K_LEFT] and self.CURRENT_POS != -1:
            self.move_timer = 0
            self.CURRENT_POS = self.CURRENT_POS - 1;
            self.mag_glass.x -= self.imageSet['Mag_glass'].get_width() - 100
        #check if right key clicked, moves glass to right position if not in furthest right position
        elif keys_pressed[pg.K_RIGHT] and self.CURRENT_POS != 1:
            self.move_timer = 0;
            self.CURRENT_POS = self.CURRENT_POS + 1;
            self.mag_glass.x += self.imageSet['Mag_glass'].get_width() - 100

    #randomly create answer choice for player to choose from
    def createAnswerChoices(self):
        question_mode = random.randint(0,5)
        #all possible options of animals to choose from
        birds = ['Seagull', 'Bird']
        mammals = ['Giraffe', 'Dolphin', 'Monkey']
        reptiles = ['Lizard', 'Snake']
        insects = ['Ladybug', 'Ant']
        fish = ['Fish', 'Swordfish']
        amphibian = ['Frog', 'Axolotl']

        #birds is correct answer
        if question_mode == 0:
            possible_wrong = [mammals, reptiles, insects, fish, amphibian];
            possible_wrong1 = random.randint(0,4)
            possible_wrong2 = random.randint(0,4)
            self.chooseAnswersFrom3(birds, possible_wrong[possible_wrong1], possible_wrong[possible_wrong2])
        #mammals is correct answer
        elif question_mode == 1:
            possible_wrong = [birds, reptiles, insects, fish, amphibian];
            possible_wrong1 = random.randint(0,4)
            possible_wrong2 = random.randint(0,4)
            self.chooseAnswersFrom3(mammals, possible_wrong[possible_wrong1], possible_wrong[possible_wrong2])
        #reptiles is the correct answer
        elif question_mode == 2:
            possible_wrong = [birds, mammals, insects, fish, amphibian];
            possible_wrong1 = random.randint(0,4)
            possible_wrong2 = random.randint(0,4)
            self.chooseAnswersFrom3(reptiles, possible_wrong[possible_wrong1], possible_wrong[possible_wrong2])
        #insects is the correct answer
        elif question_mode == 3:
            possible_wrong = [birds, reptiles, mammals, fish, amphibian];
            possible_wrong1 = random.randint(0,4)
            possible_wrong2 = random.randint(0,4)
            self.chooseAnswersFrom3(insects, possible_wrong[possible_wrong1], possible_wrong[possible_wrong2])
        #fish is the correct answer
        elif question_mode == 4:
            possible_wrong = [birds, reptiles, insects, mammals, amphibian];
            possible_wrong1 = random.randint(0,4)
            possible_wrong2 = random.randint(0,4)
            self.chooseAnswersFrom3(fish, possible_wrong[possible_wrong1], possible_wrong[possible_wrong2])
        #amphibians is the correct answer
        elif question_mode == 5:
            possible_wrong = [birds, reptiles, insects, fish, mammals];
            possible_wrong1 = random.randint(0,4)
            possible_wrong2 = random.randint(0,4)
            self.chooseAnswersFrom3(amphibian, possible_wrong[possible_wrong1], possible_wrong[possible_wrong2])

        #answerkey gets choosen in chooseANswersFrom3 function, based on that creates the animal objects in the correct position to display on screen
        if self.answerKey == 1:
            self.createAnimalObjects(self.getAnswer(), self.getWrong1(), self.getWrong2())
        elif self.answerKey == 2:
            self.createAnimalObjects(self.getWrong1(), self.getAnswer(), self.getWrong2())
        elif self.answerKey == 3:
            self.createAnimalObjects(self.getWrong1(), self.getWrong2(), self.getAnswer())

        #create the tutorial text based on which animal the user should choose
        self.createTutorialText(question_mode)

    #loads the 3 animals used to display
    def loadAnimals(self, animal1, animal2, animal3):
        self.loadImages([animal1 + '.png', animal2 + '.png', animal3 + '.png'])
        self.transformAnimalImages(animal1,animal2, animal3)

    #Creates animal objects based on which 3 animals were choosen to be displayed
    def createAnimalObjects(self, animal1, animal2, animal3):
        self.loadAnimals(animal1, animal2, animal3)
        if animal1 == 'Fish':
            self.animalname1 = 'Fish'
            self.animal1 = self.initImageObjectRect('Fish', self.WIDTH, self.HEIGHT)
        elif animal1 == 'Frog':
            self.animalname1 = 'Frog'
            self.animal1 = self.frog = self.initImageObjectRect('Frog', self.WIDTH // 2, self.HEIGHT // 2)
        elif animal1 == 'Bird':
            self.animalname1 = 'Bird'
            self.animal1 = self.bird = self.initImageObjectRect('Bird', self.WIDTH, self.HEIGHT)
        elif animal1 == 'Seagull':
            self.animalname1 = 'Seagull'
            self.animal1 = self.seagull = self.initImageObjectRect('Seagull', self.WIDTH, self.HEIGHT)
        elif animal1 == 'Giraffe':
            self.animalname1 = 'Giraffe'
            self.animal1 = self.giraffe = self.initImageObjectRect('Giraffe', self.WIDTH, self.HEIGHT)
        elif animal1 == 'Lizard':
            self.animalname1 = 'Lizard'
            self.animal1 = self.lizard = self.initImageObjectRect('Lizard', self.WIDTH, self.HEIGHT)
        elif animal1 == 'Ladybug':
            self.animalname1 = 'Ladybug'
            self.animal1 = self.ladybug = self.initImageObjectRect('Ladybug', self.WIDTH, self.HEIGHT)
        elif animal1 == 'Monkey':
            self.animalname1 = 'Monkey'
            self.animal1 = self.monkey = self.initImageObjectRect('Monkey', self.WIDTH, self.HEIGHT)
        elif animal1 == 'Dolphin':
            self.animalname1 = 'Dolphin'
            self.animal1 = self.dolphin = self.initImageObjectRect('Dolphin', self.WIDTH, self.HEIGHT)
        elif animal1 == 'Ant':
            self.animalname1 = 'Ant'
            self.animal1 = self.ant = self.initImageObjectRect('Ant', self.WIDTH, self.HEIGHT)
        elif animal1 == 'Snake':
            self.animalname1 = 'Snake'
            self.animal1 = self.snake = self.initImageObjectRect('Snake', self.WIDTH, self.HEIGHT)
        elif animal1 == 'Axolotl':
            self.animalname1 = 'Axolotl'
            self.animal1 = self.axolotl = self.initImageObjectRect('Axolotl', self.WIDTH, self.HEIGHT)
        elif animal1 == 'Swordfish':
            self.animalname1 = 'Swordfish'
            self.animal1 = self.swordfish = self.initImageObjectRect('Swordfish', self.WIDTH, self.HEIGHT)
        
        self.animal1.center = (213, 400);

        if animal2 == 'Fish':
            self.animalname2 = 'Fish'
            self.animal2 = self.initImageObjectRect('Fish', self.WIDTH, self.HEIGHT)
        elif animal2 == 'Frog':
            self.animalname2 = 'Frog'
            self.animal2 = self.frog = self.initImageObjectRect('Frog', self.WIDTH // 2, self.HEIGHT // 2)
        elif animal2 == 'Bird':
            self.animalname2 = 'Bird'
            self.animal2 = self.bird = self.initImageObjectRect('Bird', self.WIDTH, self.HEIGHT)
        elif animal2 == 'Seagull':
            self.animalname2 = 'Seagull'
            self.animal2 = self.seagull = self.initImageObjectRect('Seagull', self.WIDTH, self.HEIGHT)
        elif animal2 == 'Giraffe':
            self.animalname2 = 'Giraffe'
            self.animal2 = self.giraffe = self.initImageObjectRect('Giraffe', self.WIDTH, self.HEIGHT)
        elif animal2 == 'Lizard':
            self.animalname2 = 'Lizard'
            self.animal2 = self.lizard = self.initImageObjectRect('Lizard', self.WIDTH, self.HEIGHT)
        elif animal2 == 'Ladybug':
            self.animalname2 = 'Ladybug'
            self.animal2 = self.ladybug = self.initImageObjectRect('Ladybug', self.WIDTH, self.HEIGHT)
        elif animal2 == 'Monkey':
            self.animalname2 = 'Monkey'
            self.animal2 = self.monkey = self.initImageObjectRect('Monkey', self.WIDTH, self.HEIGHT)
        elif animal2 == 'Dolphin':
            self.animalname2 = 'Dolphin'
            self.animal2 = self.dolphin = self.initImageObjectRect('Dolphin', self.WIDTH, self.HEIGHT)
        elif animal2 == 'Ant':
            self.animalname2 = 'Ant'
            self.animal2 = self.ant = self.initImageObjectRect('Ant', self.WIDTH, self.HEIGHT)
        elif animal2 == 'Snake':
            self.animalname2 = 'Snake'
            self.animal2 = self.snake = self.initImageObjectRect('Snake', self.WIDTH, self.HEIGHT)
        elif animal2 == 'Axolotl':
            self.animalname2 = 'Axolotl'
            self.animal2 = self.axolotl = self.initImageObjectRect('Axolotl', self.WIDTH, self.HEIGHT)
        elif animal2 == 'Swordfish':
            self.animalname2 = 'Swordfish'
            self.animal2 = self.swordfish = self.initImageObjectRect('Swordfish', self.WIDTH, self.HEIGHT)
        
        self.animal2.center = (640, 400);

        if animal3 == 'Fish':
            self.animalname3 = 'Fish'
            self.animal3 = self.initImageObjectRect('Fish', self.WIDTH, self.HEIGHT)
        elif animal3 == 'Frog':
            self.animalname3 = 'Frog'
            self.animal3 = self.frog = self.initImageObjectRect('Frog', self.WIDTH // 2, self.HEIGHT // 2)
        elif animal3 == 'Bird':
            self.animalname3 = 'Bird'
            self.animal3 = self.bird = self.initImageObjectRect('Bird', self.WIDTH, self.HEIGHT)
        elif animal3 == 'Seagull':
            self.animalname3 = 'Seagull'
            self.animal3 = self.seagull = self.initImageObjectRect('Seagull', self.WIDTH, self.HEIGHT)
        elif animal3 == 'Giraffe':
            self.animalname3 = 'Giraffe'
            self.animal3 = self.giraffe = self.initImageObjectRect('Giraffe', self.WIDTH, self.HEIGHT)
        elif animal3 == 'Lizard':
            self.animalname3 = 'Lizard'
            self.animal3 = self.lizard = self.initImageObjectRect('Lizard', self.WIDTH, self.HEIGHT)
        elif animal3 == 'Ladybug':
            self.animalname3 = 'Ladybug'
            self.animal3 = self.ladybug = self.initImageObjectRect('Ladybug', self.WIDTH, self.HEIGHT)
        elif animal3 == 'Monkey':
            self.animalname3 = 'Monkey'
            self.animal3 = self.monkey = self.initImageObjectRect('Monkey', self.WIDTH, self.HEIGHT)
        elif animal3 == 'Dolphin':
            self.animalname3 = 'Dolphin'
            self.animal3 = self.dolphin = self.initImageObjectRect('Dolphin', self.WIDTH, self.HEIGHT)
        elif animal3 == 'Ant':
            self.animalname3 = 'Ant'
            self.animal3 = self.ant = self.initImageObjectRect('Ant', self.WIDTH, self.HEIGHT)
        elif animal3 == 'Snake':
            self.animalname3 = 'Snake'
            self.animal3 = self.snake = self.initImageObjectRect('Snake', self.WIDTH, self.HEIGHT)
        elif animal3 == 'Axolotl':
            self.animalname3 = 'Axolotl'
            self.animal3 = self.axolotl = self.initImageObjectRect('Axolotl', self.WIDTH, self.HEIGHT)
        elif animal3 == 'Swordfish':
            self.animalname3 = 'Swordfish'
            self.animal3 = self.swordfish = self.initImageObjectRect('Swordfish', self.WIDTH, self.HEIGHT)
        
        self.animal3.center = (1066, 400);

    #returns minigame tag for this minigame, which is animals
    def getMinigameTag(self):
        return 'animals'