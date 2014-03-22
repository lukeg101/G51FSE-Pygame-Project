#import game modules
import sys, pygame
from pygame.sprite import Sprite
from pygame.locals import *

"""class that defines the state and behaviour of the player ship"""
class PlayerShip(Sprite):

#need to do different classes of ship

	#default constructor - initisalises ship object on creation
	def __init__(self, spawnCoords):
		pygame.sprite.Sprite.__init__(self)

		#define the ship image, health, lives and ship x/y coords
		self.shipImages = []	
		self.xCoord = 0
		self.yCoord = 0						#ship classification will change ship image 
		self.health=100
		self.lives=4

		#load the image for the ship
		for i in range(1,5):
			self.curImage = pygame.image.load("ORgateShipRevision" + str(i) + ".png")
			self.curImage = pygame.transform.scale(self.curImage, (33, 49))
			self.shipImages.append(self.curImage)
			self.image = self.shipImages[0]

		#load the rectangle image behind the sprite
		self.rect = self.image.get_rect()
		self.rect.center = spawnCoords

	#method moves ship down	
	def keyDown(self):
		self.yCoord += 3

	#method moves ship up
	def keyUp(self):
		self.yCoord -= 3
	
	#method moves ship left
	def keyLeft(self):
		self.xCoord -= 3

	#method moves ship right
	def keyRight(self):
		self.xCoord += 3
	
	#method reduces ship health upon hit						#need to implement varying health and enemy/player collision
	def takeHit(self, damageVal):

		#if damage dealt is < current health: reduce current health
		if damageVal < self.health:
			self.health - damageVal
		#else reduce lives and reset health counter
		else:
			self.lives -= 1
			self.health = 100

	#updates sprite state on screen - x/y coordinates
	def update(self):
		self.rect.move_ip(self.xCoord, self.yCoord)
	
		#animate the sprite with correct image
		if self.xCoord < 0:
			self.image = self.shipImages[2]
			self.image = pygame.transform.scale(self.image, (33, 49))
		elif self.xCoord > 0:
			self.image = self.shipImages[1]
			self.image = pygame.transform.scale(self.image, (33, 49))
		elif self.yCoord < 0:
			self.image = self.shipImages[3]
			self.image = pygame.transform.scale(self.image, (33, 64))
		else:		
			self.image = self.shipImages[0]
			self.image = pygame.transform.scale(self.image, (33, 49))

		#define the boundaries in which the ship can move
		self.rect.top = max(350, self.rect.top)
		self.rect.bottom = min(575, self.rect.bottom)
		self.rect.left = min(367, self.rect.left)
		self.rect.right = max(33, self.rect.right)

