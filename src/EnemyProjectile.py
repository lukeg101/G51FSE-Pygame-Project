#import game modules
import sys, pygame
from pygame.sprite import Sprite
from pygame.locals import *

"""class that defines and characterises projectile objects within the game"""

class EnemyProjectile(Sprite):

	#initialises projectile object upon invocation
        def __init__(self, spawnCoords):
                pygame.sprite.Sprite.__init__(self)
		
		self.counter = 0
		self.projectileClock = 0
		self.bulletImage = None

                #load the image for the ship
		self.bulletImage = pygame.image.load("enemyPlasmaProjectile.png")
                self.bulletImage = pygame.transform.scale(self.bulletImage, (15, 15))
		self.image = self.bulletImage

		#load the rectangle image behind the sprite
                self.rect = self.image.get_rect()
		self.rect.center = spawnCoords

		#method updates sprite state - moves projectiles along a linear path
	def update(self):
		self.rect.y += 2
		
		if self.projectileClock == 0  and self.counter == 40:
			self.counter = 0
			self.projectileClock = 1
		elif self.projectileClock == 1 and self.counter == 40:
			self.counter = 0
			self.projectileClock = 0
		else:
			self.counter += 1
		
