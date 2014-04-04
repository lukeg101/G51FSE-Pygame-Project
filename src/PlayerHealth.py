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

	#function simply removes health if the player ship is hit 					#needs sorting 
        def hit(self, hitValue):
                self.health -= hitValue
                self.renderText()
	
	#function sets the health of the player - used when they lose a life
	def newHealth(self, newValue):
		self.health = newValue

	#function updates sprite state on screen 
        def update(self):
                self.renderText()	
