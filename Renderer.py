import pygame
import numpy as np
import math
from GameTools import Vector2, Vector3


class Renderer:
    
    def __init__(self, parent):
        self.parent = parent
        self.w, self.h = 1280, 720
               
        self.screen = pygame.display.set_mode((self.w,self.h))
        self.gui = GUI()
        
        self.cameras = []  
        self.selectedCamera = None
        self.renderables = []
        
        self.centerOffset = Vector2(int(self.w/2), int(self.h/2))        
        self.drawQueue = []
    

    def FillScreen(self):
        self.screen.fill("black")

    def RenderDrawables(self):
        for drawable in self.drawQueue:
            if drawable[0] == pygame.draw.circle:
                center = drawable[1][1]+self.cameraOffset
                pygame.draw.circle(self.screen, drawable[1][0], (center.x, center.y) , drawable[1][2])
    
    def RenderShots(self, shots):        
        for shot in shots:
            self.screen.blit(shot, (self.centerOffset - Vector2(*shot.get_size())/2).vecList)


        
    def Flip(self):        
        pygame.display.flip()
      

    
    def NoiseRadii(self, signal):
        pygame.draw.circle(self.screen, (255,0,0,64), (signal.position.x, signal.position.z), signal.volume)

           
class GUI:
    
    def __init__(self):
        self.UIfeatures = []
        
    def AddLabel(self):
        pass

