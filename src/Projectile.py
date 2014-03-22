#import game modules
import sys, pygame
from pygame.sprite import Sprite
from pygame.locals import *

"""class that defines and characterises projectile objects within the game"""
class Projectile(Sprite):
	
#need to do different types of object and strength


	#initialises projectile object upon invocation
        def __init__(self, spawnCoords):
                pygame.sprite.Sprite.__init__(self)
		
		self.counter = 0
		self.projectileClock = 0
		self.bulletImages = []
                #load the image for the ship
                for i in range(1,3):
			self.curImage = pygame.image.load("plasmaProjectile" + str(i)  + ".png")
                	self.curImage = pygame.transform.scale(self.curImage, (15, 15))
			self.bulletImages.append(self.curImage)
			self.image = self.bulletImages[0]

		#load the rectangle image behind the sprite
                self.rect = self.image.get_rect()
		self.rect.center = spawnCoords		

	#method updates sprite state - moves projectiles along a linear path
	def update(self):
		self.rect.y -= 5
		
		if self.projectileClock == 0  and self.counter == 40:
			self.image = self.bulletImages[0]
			self.counter = 0
			self.projectileClock = 1
		elif self.projectileClock == 1 and self.counter == 40:
			self.image = self.bulletImages[1]
			self.counter = 0
			self.projectileClock = 0
		else:
			self.counter += 1

