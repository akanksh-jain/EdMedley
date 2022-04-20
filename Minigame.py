from logging import PlaceHolder
from pydoc import render_doc
from secrets import choice
import pygame as pg
import os
pg.font.init()

from abc import ABC, abstractmethod
import random

class Minigame(ABC):
    def __init__(self, WIN, SCALE, NEXT_MINI, duration):
        self.WIN = WIN;
        self.SCALE = SCALE;
        self.NEXT_MINI = NEXT_MINI;
        self.choices = [];
        self.answerKey = 1;
        self.duration = duration;
        self.timeLeft = self.duration;

    #May need to check if image name doesn't exist
    def loadImages(self, listOfImageNames):
        for name in listOfImageNames:
            if(os.path.exists(os.path.join('Assets', name))):
                self.imageSet.update({name[0:-4] : pg.image.load(os.path.join('Assets', name)).convert_alpha()})
            else:
                self.imageSet.update({name[0:-4] : pg.image.load(os.path.join('Assets', 'Placeholder.png')).convert_alpha()})

    #Automatically checks if image is loaded and does global scaling itself, manual scaling still present
    def initScaleImage(self, name, manWidth, manHeight):
        if(manWidth < 0 or manHeight < 0):
            return False;
        if name in self.imageSet:
            self.imageSet[name] = pg.transform.scale(self.imageSet[name], ((int)(self.WIDTH * self.SCALE * manWidth), (int)(self.HEIGHT * self.SCALE * manHeight)))
            return True
        print("Scaling failed, '" + name + "' is not a valid image.");
        return False

    #Creates the rectangle for a certain image, only needs x and y position and image name
    def initImageObjectRect(self, name, xpos, ypos):
        if name in self.imageSet:
            return pg.Rect(xpos, ypos, self.imageSet[name].get_width(), self.imageSet[name].get_height())
        print("Object creation failed, '" + name + "' is not a valid image.");

        #Size of placeholder texture
        return pg.Rect(xpos, ypos, 420, 420);
 
    def chooseAnswersFrom3(self, listAns, listSub1, listSub2):
        self.answerKey = random.randint(1,5) % 3 + 1;
        answer = listAns[random.randint(0, len(listAns) - 1)];
        wrong1 = listSub1[random.randint(0, len(listSub1) - 1)];
        wrong2 = listSub2[random.randint(0, len(listSub2) - 1)];
        if(self.answerKey == 1):
            self.choices = [answer, wrong1, wrong2];
            return
        elif(self.answerKey == 2):
            self.choices = [wrong1, answer, wrong2];
            return
        else:
            self.choices = [wrong1, wrong2, answer];
            return

    #Should always have 3 or more choices
    def getAnswer(self):
        if(len(self.choices) > 0):
            return self.choices[self.answerKey - 1]
        return "NULL";

    def getWrong1(self):
        if(len(self.choices) > 0):
            if(self.answerKey >= 2):
                return self.choices[0];
            else:
                return self.choices[1];
        return "NULL";

    def getWrong2(self):
        if(len(self.choices) > 0):
            if(self.answerKey <= 2):
                return self.choices[2];
            else:
                return self.choices[1];
        return "NULL";

    def drawTimer(self):
        #Debugging can set duration to 1
        if(self.duration >= 50):
            #Called every tick so based on FPS, need to change if FPS changes
            self.timeLeft = self.timeLeft - 33;
            #Red is increasing value, green is decreasing
            redVal = (int)(255 * abs(self.duration - self.timeLeft) / self.duration);
            greenVal = (int)(255 * abs(self.timeLeft) / self.duration);
            if(redVal >= 255):
                redVal = 255;

            if(greenVal <= 0):
                greenVal = 0;

            newLength = (int)(1200 * self.timeLeft / self.duration);
            if(newLength <= 0):
                newLength = 0;

            pg.draw.rect(self.WIN, (redVal, greenVal, 0), pg.Rect(40, 680, newLength, 30));

    def startRunningMinigame(self):
        #Will need to change to event that moves the queue foward
        # print("New Minigame")
        pg.time.set_timer(self.NEXT_MINI, self.duration, 1);

    #Should tick the minigame forwards
    @abstractmethod
    def run_minigame(self):
        pass

    @abstractmethod
    def draw_window(self):
        pass

    @abstractmethod
    def correctAnswer(self):
        pass

    @abstractmethod
    def getMinigameTag(self):
        pass

