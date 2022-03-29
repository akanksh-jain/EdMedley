from logging import PlaceHolder
from pydoc import render_doc
import pygame as pg
import os
pg.font.init()

from abc import ABC, abstractmethod

class Minigame(ABC):
    def __init__(self, WIN, SCALE, NEXT_MINI):
        self.WIN = WIN;
        self.SCALE = SCALE;
        self.NEXT_MINI = NEXT_MINI;

    #May need to check if image name doesn't exist
    def loadImages(self, listOfImageNames):
        numberOfFailedLoaded = 0;
        for name in listOfImageNames:
            if(os.path.exists(os.path.join('Assets', name))):
                self.imageSet.update({name[0:-4] : pg.image.load(os.path.join('Assets', name))})
            else:
                self.imageSet.update({name[0:-4] : pg.image.load(os.path.join('Assets', 'PlaceHolder.png'))})
                numberOfFailedLoaded = numberOfFailedLoaded + 1;
        return numberOfFailedLoaded;

    #Automatically checks if image is loaded and does global scaling itself, manual scaling still present
    def initScaleImage(self, name, manWidth, manHeight):
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
        return pg.Rect(xpos, ypos, 420, 420);

    @abstractmethod
    def run_minigame(self):
        pass

    @abstractmethod
    def draw_window(self):
        pass
