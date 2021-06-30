import pygame as pg


class Button:
    def __init__(self, name, xpos, number):
        self.name = name
        self.xpos = xpos
        self.ypos = 530
        self.number = number
        self.press = False

    def createButton(self, screen): 
        self.pic = pg.image.load(self.name)
        height, width = self.pic.get_size()
        self.pic = pg.transform.smoothscale(self.pic,(int(height/2), int(width/2)))       
        self.buttonRect = self.pic.get_rect()
        screen.blit(self.pic, (self.xpos, self.ypos))
        self.buttonRect.move_ip(self.xpos, self.ypos)

    # start simulation
    def selectstart(self, Ball, allOutput, screen, allFont, allColor, fps, allScale):
        allOutput[0].value = round(Ball.speed, 2) # set speed answer
        allOutput[1].value = round(Ball.distance, 2) # set distance answer
        allOutput[2].value = round(Ball.time, 2) # set time answer
        for output in allOutput:
            output.createOutput(screen, allFont, allColor)
        Ball.plot(screen, allFont, allColor, fps, allScale) # plot ball moving

    # set everything to default
    def selectreset(self, allScale, allOutput, Ball, screen, allFont, allColor):
        allOutput[0].value = 0.00 # set speed to 0
        allOutput[1].value = 0.00 # set distance to 0
        allOutput[2].value = 0.00 # set time to 0
        allScale[2].option = False # set spring constant option 0
        allScale[3].option = True # set retraction distance option 1
        for output in allOutput:
            output.createOutput(screen, allFont, allColor)
        for scale in allScale:
            scale.value = scale.default
            scale.updateToScreen(screen, allFont, allColor, scale.option)
            Ball.drawShooterAndTarget(screen, allScale[4].value, allScale[0].value, allScale[1].value)
