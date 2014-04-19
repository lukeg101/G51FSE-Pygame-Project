#import game modules
import sys, pygame
from pygame.sprite import Sprite
from pygame.locals import *

"""class that defines and characterises projectile objects within the game"""
class TriProjectile(Sprite):
	
#need to do different types of object and strength


	#initialises projectile object upon invocation
        def __init__(self, spawnCoords, direction):
                pygame.sprite.Sprite.__init__(self)
	
		self.fireDirection = direction
		
                #load the image for the ship
		self.curImage = pygame.image.load("plasmaProjectile1.png")
                self.curImage = pygame.transform.scale(self.curImage, (15, 15))
		self.image = self.curImage

		#load the rectangle image behind the sprite
                self.rect = self.image.get_rect()
		self.rect.center = spawnCoords		

	#method updates sprite state - moves projectiles along a linear path
	def update(self):

		if (self.fireDirection == 1):
			self.rect.x += 1.1
		elif (self.fireDirection == 0):
			self.rect.x -= 1.1
		self.rect.y -= 2


