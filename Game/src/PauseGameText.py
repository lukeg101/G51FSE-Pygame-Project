#import game modules
import sys, pygame
from pygame.sprite import Sprite
from pygame.locals import *

"""class to display and manage the state of the player lives"""
class PauseGameText(Sprite):

	#default constructor to define the state of the lives of the sprite
	def __init__(self, colour, text, size, spawnCoords):
	        pygame.sprite.Sprite.__init__(self)

		#define the colour and lives of the text display
	        self.colour = pygame.Color(colour)
		self.font = pygame.font.Font(None, size)
		self.text = text
	        self.renderText()
	        self.rect = self.image.get_rect()
	        self.rect.center = spawnCoords

	#method that renders the text on screen
	def renderText(self):
	        self.image = self.font.render(self.text, True, self.colour)

	def update(self):
		self.renderText()
