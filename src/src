#!/usr/bin/env python

#import game modules
import sys, pygame, random
from pygame.sprite import Sprite
from pygame.locals import *
from pygame.mixer import *

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
                        self.curImage = pygame.image.load("ORgateShipRevision" + str(i) + ".png")
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
				self.image = self.shipImages[1]	
                        elif self.moveDirection == 1:
                                self.moveRight()
				self.image = self.shipImages[2]
	
	#updates the ship object state on screen
	def update(self):
		
		self.moveSprite()		
		self.rect.move_ip(self.xCoord, self.yCoord)
		
		#define the boundaries in which the game can move
		self.rect.top = max(0, self.rect.top)
		self.rect.bottom = min(600, self.rect.bottom)
		self.rect.left = min(367, self.rect.left)
		self.rect.right = max(33, self.rect.right)

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

"""class to measure and display player health on screen"""
class PlayerHealth(Sprite):
        
	#initialises the object upon invocation - sets player health and display
	def __init__(self, colour, spawnCoords, health):
                pygame.sprite.Sprite.__init__(self)
 
		#initialise the player health and colour the font will be
                self.health = health
                self.colour = pygame.Color(colour)

		#set rect and render coordinates of health sprite
                self.font = pygame.font.Font(None, 26)                
		self.renderText()
		self.rect = self.image.get_rect()
		self.rect.center = spawnCoords

	#function simply renders text on screen
        def renderText(self):
                self.image = self.font.render("Health: %d" % self.health, True, self.colour)

	#function simply removes 10 health if the player ship is hit 					#needs sorting 
        def hit(self):
                self.health -= 10
                self.renderText()

	#function updates sprite state on screen 
        def update(self):
                self.renderText()	

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
	        self.render_text()
	
	#method to update the state of the object on screen
	def update(self):
		self.renderText()

"""main function where the game runs"""						#game will be classified after prototype
def main():
	#initialise modules in use
	pygame.init()
	pygame.font.init()
	pygame.mixer.init()
	
	#game loop variables
        runningGame = True
	levelComplete = False
	enemiesRemaining = 0	

	#create and define the screen window
	screenHeight, screenWidth = 600, 400
	window = pygame.display.set_mode([screenWidth, screenHeight])
	pygame.display.set_caption("Logic Wars")
	screen = pygame.Surface([screenWidth, screenHeight])
	imagePath = "TestDayBackground.png"			#will be determined by level
	backgroundImage = pygame.image.load(imagePath).convert()		#will be determined by level
	yScaler = 0
	changeFrame = True
	
	#create userShip, score and health sprites
	shipxPos, shipyPos = 200, 400						#player ship will be selected by user
	player = PlayerShip((shipxPos, shipyPos))					
	healthBarShadow = PlayerHealth("black", (51,586), player.health)			
	healthBar = PlayerHealth("white", (50,585), player.health)
	playerScoreShadow = PlayerScore("black", (35,10))					#player ship will be selected by user
	playerScore = PlayerScore("white", (34,10))					#player ship will be selected by user
	playerLivesShadow = PlayerLives("black", (351,586), player.lives) 			
	playerLives = PlayerLives("white", (350,585), player.lives) 			

	#create the sprite groups to which the respective sprites belong
	spriteList = pygame.sprite.LayeredUpdates()
	spriteList.add(playerScoreShadow)
	spriteList.add(playerScore)

	spriteList.add(healthBarShadow)
	spriteList.add(healthBar)
	spriteList.add(playerLivesShadow)
	spriteList.add(playerLives)
	spriteList.add(player)
	projectileList = pygame.sprite.Group()
	enemyList = pygame.sprite.Group()
	
	#demo day enemies 
	for i in range(10):
		enemy = EnemyShip((random.randrange(0, 350), random.randrange(0, 350)))
		spriteList.add(enemy)
		enemyList.add(enemy)
		enemiesRemaining += 1
	
	#define game sounds and music						#music will change on each level
	projectileSound = pygame.mixer.Sound("laser shot.wav")
	shipExplosion = pygame.mixer.Sound("ship explosion.wav")
	gameSuccess = pygame.mixer.Sound("success.wav")
	music = pygame.mixer.music.load("01_Make_It_Bun_Dem.wav")
	pygame.mixer.music.play()

	#control mapping for player
	key_map = {
		pygame.K_w: [player.keyUp, player.keyDown],
		pygame.K_s: [player.keyDown, player.keyUp],
		pygame.K_a: [player.keyLeft, player.keyRight],
		pygame.K_d: [player.keyRight, player.keyLeft],
		pygame.K_UP: [player.keyUp, player.keyDown],
                pygame.K_DOWN: [player.keyDown, player.keyUp],
                pygame.K_LEFT: [player.keyLeft, player.keyRight],
                pygame.K_RIGHT: [player.keyRight, player.keyLeft]
	}

	#limit game clock 
	gameClock = pygame.time.Clock()
	gameClock.tick(30)

	# draw and display on screen
	pygame.display.update()
	pygame.display.flip()

	#game loop
	while runningGame:

		PlayerLives.decrease
		
		#read in events from queue
		for event in pygame.event.get():
			#on QUIT event, exit the game loop
			if event.type == pygame.QUIT:
				runningGame = False
			#if a key is pressed, act based on library definition
			elif event.type == pygame.KEYDOWN and event.key in key_map:
				key_map[event.key][0]()
			#if a key is released, act based on library definition
			elif event.type == pygame.KEYUP and event.key in key_map:
				key_map[event.key][1]() 
			#if a space bar is pressed, fire the projectile
			elif event.type == pygame.KEYDOWN:
				keyPresses = pygame.key.get_pressed()
				if keyPresses[K_SPACE] == 1:
					bullet = Projectile([player.rect.x + 17, player.rect.y])
					spriteList.add(bullet)
        				projectileList.add(bullet)
					projectileSound.play()
					
		#move the background image - yTranslation
		if changeFrame:
			yScaler += 1
			changeFrame = False#moves every other frame
		else: 
			changeFrame = True 
	
		if yScaler == 1400:
			yScaler = 0		
	
		#sprite collision detection between sprites and projectiles
		for projectile in projectileList:

			#form the list of collisions
			hitList = pygame.sprite.spritecollide(projectile, enemyList, True)
			
			#for every collision, remove the sprite and increase player score			
			for hits in hitList:
				projectile.kill()
				playerScore.increase()
				playerScoreShadow.increase()
				shipExplosion.play()
				enemiesRemaining -= 1

			if projectile.rect.y == 0:
				projectileList.remove(projectile)
				projectileList.remove(projectile)
				projectile.kill()
				gameSuccess.play()

		#animate the wallpaper on screen
                window.blit(backgroundImage, (0, yScaler))
                window.blit(backgroundImage, (0,yScaler - 1400))
		
		#game finished upon success
		if enemiesRemaining == 0 and not levelComplete:
			gameSuccess.play()
			levelComplete = True
	
		#animate the sprites
		spriteList.update()
                spriteList.draw(window)
	        pygame.display.flip()
		spriteList.clear(window, screen)
		
		gameClock.tick(120)	

#makes the game script run the main function
if __name__ == "__main__":
	main()
