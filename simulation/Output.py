from typing import Text
import pygame as pg


class Output:
    def __init__(self, name, unit, xpos, ypos):
        self.name = name
        self.unit = unit
        self.xpos = xpos
        self.ypos = ypos
        self.value = 00.00

    def createOutput(self, screen, allFont, allColor):
        self.textArea = pg.Surface((200,50))
        self.textArea.fill(allColor[0])
        self.text = allFont[2].render(self.name + str(self.value) + self.unit, True, allColor[4])
        self.textArea.blit(self.text, (0,0))
        screen.blit(self.textArea, (self.xpos, self.ypos))