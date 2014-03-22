#import game modules
import sys, pygame
from pygame.sprite import Sprite
from pygame.locals import *

"""class to measure and display player health on screen"""
class PlayerHealth(Sprite):
        
	#initialises the object upon invocation - sets player health and display
	def __init__(self, colour, spawnCoords, health):
                pygame.sprite.Sprite.__init__(self)
 
		#initialise the player health and colour the font will be
                self.health = health
                self.colour = pygame.Color(colour)

		#set rect and render coordinates of health sprite
                self.font = pygame.font.Font(None, 26)                
		self.renderText()
		self.rect = self.image.get_rect()
		self.rect.center = spawnCoords

	#function simply renders text on screen
        def renderText(self):
                self.image = self.font.render("Health: %d" % self.health, True, self.colour)

	#function simply removes 10 health if the player ship is hit 					#needs sorting 
        def hit(self):
                self.health -= 10
                self.renderText()

	#function updates sprite state on screen 
        def update(self):
                self.renderText()	
