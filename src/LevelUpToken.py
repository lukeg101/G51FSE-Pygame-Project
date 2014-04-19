#import game modules
import sys, pygame
from pygame.sprite import Sprite
from pygame.locals import *

"""class that defines and a level up token that increases player Live"""

class PowerUp(Sprite):
	
	#initialises Token object upon invocation
        def __init__(self, spawnCoords, powerUpType):
                pygame.sprite.Sprite.__init__(self)

		#tokenNumber used to determine which type of token is used
		self.tokenType = powerUpType		
		self.bulletImage = None

                #load the image for the Token
		
		#need to create image
		self.bulletImage = pygame.image.load("ANDgateShipRevision1.png")
                self.bulletImage = pygame.transform.scale(self.bulletImage, (20, 20))
		self.image = self.bulletImage

		#load the rectangle image behind the sprite
                self.rect = self.image.get_rect()
		self.rect.center = spawnCoords

	def update(self):
		self.rect.y += 1


