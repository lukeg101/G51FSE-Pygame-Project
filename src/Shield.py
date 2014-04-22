#import game modules
import sys, pygame
from pygame.sprite import Sprite
from pygame.locals import *

"""class for the power up item that grants the player a shield"""

class Shield(Sprite):

	#initialises Token object upon invocation
        def __init__(self, spawnCoords):
                pygame.sprite.Sprite.__init__(self)

		#load the shield 
		self.shieldImage = pygame.image.load("ANDgateShipRevision1.png")
                self.shieldImage = pygame.transform.scale(self.shieldImage, (60, 10))
		self.image = self.shieldImage

		#load the rectangle image behind the sprite
                self.rect = self.image.get_rect()
		self.rect.center = spawnCoords

	def updateLocation(self, newCoords):
		self.rect.center = newCoords
