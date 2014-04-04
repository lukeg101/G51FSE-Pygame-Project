#import game modules
import sys, pygame
from pygame.sprite import Sprite
from pygame.locals import *
"""method defines the state and behaviour of various enemy ships"""
class EnemyShip(Sprite):

#need different classes of ships and enemy mothership

	#default constructor - initisalises ship object on creation
	def __init__(self, spawnCoords):
		pygame.sprite.Sprite.__init__(self)
		
		#set the initial image state and ship x/y Coords 
		self.shipImages = []	
		self.xCoord = 0
		self.yCoord = 0
		self.moveCounter = 0
		self.moveDirection = 0 #0 is left, 1 is right
		#load the image for the ship
		#image, ship health will change with classification
		
		#load the image for the ship
                for i in range(1,5):
                        self.curImage = pygame.image.load("enemyNORGateShip" + str(i) + ".png")
                        self.curImage = pygame.transform.scale(self.curImage, (33, 49))
			self.curImage = pygame.transform.rotate(self.curImage, 180)
                        self.shipImages.append(self.curImage)
                        self.image = self.shipImages[0]


		#get the sprite rect and render coords
		self.rect = self.image.get_rect()
		self.rect.center = spawnCoords
	
	#method moves the ship right
	def moveRight(self):
		self.xCoord += 1

	#method moves the ship left
	def moveLeft(self):
		self.xCoord -= 1
	
	#method moves the ship down
	def moveDown(self):
		self.yCoord += 1
	
	#method moves the ship up
	def moveUp(self):
		self.yCoord -= 1

	def moveSprite(self):
		self.moveCounter += 1

                if self.rect.left == 0:
                        self.moveDirection = 1
                        self.moveRight()
                        self.rect.y += 5
                        self.moveCounter = 0
                elif self.rect.left == 367:
                        self.moveDirection = 0
                        self.moveLeft()
                        self.rect.y += 5
                        self.moveCounter = 0
			
                if self.moveCounter == 20:
                        if self.moveDirection == 0:
                                self.moveLeft()
				self.image = self.shipImages[2]	
                        elif self.moveDirection == 1:
                                self.moveRight()
				self.image = self.shipImages[3]
	
	#updates the ship object state on screen
	def update(self):
		
		self.moveSprite()		
		self.rect.move_ip(self.xCoord, self.yCoord)
		
		#define the boundaries in which the game can move
		self.rect.top = max(0, self.rect.top)
		self.rect.bottom = min(600, self.rect.bottom)
		self.rect.left = min(367, self.rect.left)
		self.rect.right = max(33, self.rect.right)

