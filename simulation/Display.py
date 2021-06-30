import pygame as pg
from Button import Button
from Scale import Scale
from Projectile import Projectile
from Output import Output


class Display:
    def __init__(self, screen, allFont, allColor):
        self.screen = screen
        self.allFont = allFont
        self.allColor = allColor

        # create Scale 
        self.sHeightScale = Scale("SHOOTING HEIGHT (m)", 0.45, 1, 35, 0.475, None)
        self.angleScale = Scale("SHOOTING ANGLE", 1, 89, 230, 45, None)
        self.springScale = Scale("SPRING CONSTANT (N/m)", 100, 1000, 425, 566.36, False)
        self.retractScale = Scale("RETRACTION DISTANCE (m)", 0.01, 0.20, 620, 0.13, True)
        self.targetDistance = Scale("TARGET DISTANCE (m)", 0.5, 3, 815, 2.05, None)
        self.allScale = [self.sHeightScale, self.angleScale, self.springScale, self.retractScale, self.targetDistance]

        for scale in self.allScale:
            scale.createScale(self.allFont, self.allColor)
            scale.updateToScreen(self.screen, self.allFont, self.allColor, scale.option)

        # create Projectile (default)
        self.Ball = Projectile(self.sHeightScale.value, self.angleScale.value, self.springScale.value, self.retractScale.value, 0.41, self.targetDistance.value, 100)
        self.Ball.createArea(self.allFont, self.allColor)
        self.Ball.drawShooterAndTarget(self.screen, self.targetDistance.value, self.sHeightScale.value, self.angleScale.value)
      
        # create Button
        self.startButton = Button("startbutton.png", 415, 1)
        self.resetButton = Button("resetbutton.png", 565, 2)
        self.allButton = [self.startButton, self.resetButton]

        for button in self.allButton:
            button.createButton(self.screen)

        # create Output 
        self.speedOutput = Output("SPEED : ", " m/s", 80, 150)
        self.distanceOutput = Output("DISTANCE : ", " m", 80, 220)
        self.timeOutput = Output("TIME : ", " s" ,80, 290)
        self.allOutput = [self.speedOutput, self.distanceOutput, self.timeOutput]

        for output in self.allOutput:
            output.createOutput(self.screen, self.allFont, self.allColor)

    def displayToScreen(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mpos = pg.mouse.get_pos()
                for scale in self.allScale:
                    if scale.button.collidepoint(mpos):
                        scale.press = True
                if(self.allScale[2].lockRect.collidepoint(mpos) or self.allScale[3].lockRect.collidepoint(mpos)):
                    if(self.allScale[2].option == True):
                        self.allScale[2].option = False
                        self.allScale[3].option = True
                    elif(self.allScale[2].option == False):
                        self.allScale[2].option = True
                        self.allScale[3].option = False
                for button in self.allButton:
                    if button.buttonRect.collidepoint(mpos):
                        button.press = True
            elif event.type == pg.MOUSEBUTTONUP:
                for scale in self.allScale:
                    scale.press = False
                for button in self.allButton:
                    button.press = False
        
        for scale in self.allScale:
            if scale.press:
                scale.updateValue()

        for scale in self.allScale:
            scale.updateToScreen(self.screen, self.allFont, self.allColor, scale.option)
            if self.targetDistance.press or self.sHeightScale.press or self.angleScale.press:
                self.Ball.drawShooterAndTarget(self.screen, self.targetDistance.value, self.sHeightScale.value, self.angleScale.value)
            
        for button in self.allButton:
            if button.press:
                if button.number == 1: # select start button
                    # create Projectile class (create here bacause values always change)
                    self.Ball = Projectile(self.sHeightScale.value, self.angleScale.value, self.springScale.value, self.retractScale.value, 0.41, self.targetDistance.value, 100)
                    self.Ball.createArea(self.allFont, self.allColor)
                    self.Ball.calculate()
                    fps = pg.time.Clock()
                    button.selectstart(self.Ball, self.allOutput, self.screen, self.allFont, self.allColor, fps, self.allScale)
                
                elif button.number == 2: # select reset button
                    button.selectreset(self.allScale, self.allOutput, self.Ball, self.screen, self.allFont, self.allColor)   
