from pydoc import render_doc
import pygame as pg
import os
pg.font.init()

from abc import ABC, abstractmethod

class Minigame(ABC):
    def __init__(self, WIN, SCALE):
        self.WIN = WIN;
        self.SCALE = SCALE;

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

    #Creates the rectangle for a certain image, only needs x and y position and image name
    def initImageObjectRect(self, name, xpos, ypos):
        if name in self.imageSet:
            return pg.Rect(xpos, ypos, self.imageSet[name].get_width(), self.imageSet[name].get_height())
        print("Object creation failed, '" + name + "' is not a valid image.");

    @abstractmethod
    def run_minigame(self):
        pass

    @abstractmethod
    def draw_window(self):
        pass
