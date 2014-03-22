#import game modules
import sys, pygame
from pygame.sprite import Sprite
from pygame.locals import *

"""class to measure and display player score on screen"""
class PlayerScore(Sprite):
	
	#initialises the object upon invocation
	def __init__(self, colour, spawnCoords):
		pygame.sprite.Sprite.__init__(self)
		
		#set the initial score and font of the score
		self.colour = pygame.Color(colour)
		self.score = 0 
		
		#sets the rect and render coords for score sprite
		self.font = pygame.font.Font(None, 26)
		self.renderText()
		self.rect = self.image.get_rect()
		self.rect.center = spawnCoords

	#simply renders the text on screen 
	def renderText(self):
		self.image = self.font.render("Score: %d" % self.score, True, self.colour)

	#method increases player score 							#get multiplier sorted
	def increase(self):
		self.score += 1
		
	#method updates sprite state on screen
	def update(self):
		self.renderText()
