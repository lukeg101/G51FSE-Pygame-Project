#import game modules
import sys, pygame
from pygame.sprite import Sprite
from pygame.locals import *

"""class to display and manage the state of the player lives"""
class PlayerLives(Sprite):

	#default constructor to define the state of the lives of the sprite
	def __init__(self, colour, spawnCoords, playerLives):
	        pygame.sprite.Sprite.__init__(self)

		#define the colour and lives of the text display
	        self.colour = pygame.Color(colour)
	        self.lives = playerLives
	        
		self.font = pygame.font.Font(None, 26)
	        self.renderText()
	        self.rect = self.image.get_rect()
	        self.rect.center = spawnCoords

	#method that renders the text on screen
	def renderText(self):
	        self.image = self.font.render("Lives: %d" % self.lives, True, self.colour)

	#method to decrease the player lives
	def decrease(self):
	        self.lives -= 1
	        self.renderText()

	#methof to increase player lives	
	def increase(self):
		self.lives += 1
		self.renderText()

	#method to update the state of the object on screen
	def update(self):
		self.renderText()
