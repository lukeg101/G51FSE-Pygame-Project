#import game modules
import sys, pygame, random
from pygame.sprite import Sprite
from pygame.locals import *
from pygame.mixer import *
from PlayerShip import PlayerShip
from EnemyShip import EnemyShip
from Projectile import Projectile
from PlayerScore import PlayerScore
from PlayerHealth import PlayerHealth
from PlayerLives import PlayerLives
from EnemyProjectile import EnemyProjectile
from LevelUpToken import PowerUp
from TriProjectile import TriProjectile
from PauseGameText import PauseGameText

"""class that runs the game loop"""
class MainLoop():
	
	#initialises Token object upon invocation
        def __init__(self):
		
		#initialise modules in use
		pygame.init()
		pygame.font.init()
		pygame.mixer.init()
		
		#game loop variables
	        self.runningGame = True
		self.pausedGame = False
		self.levelComplete = False
		self.enemiesRemaining = 0	
	
		#create and define the screen window
		self.screenHeight, self.screenWidth = 600, 400
		self.window = pygame.display.set_mode([self.screenWidth, self.screenHeight])
		pygame.display.set_caption("Logic Wars")
		self.screen = pygame.Surface([self.screenWidth, self.screenHeight])
		self.imagePath = "TestDayBackground.png"			#will be determined by level
		self.backgroundImage = pygame.image.load(self.imagePath).convert()		#will be determined by level
		self.yScaler = 0
		self.changeFrame = True	

		#create userShip, score and health sprites
		self.shipxPos, self.shipyPos = 200, 400						#player ship will be selected by user
		self.player = PlayerShip((self.shipxPos, self.shipyPos))					
		self.healthBarShadow = PlayerHealth("black", (51,586), self.player.health)			
		self.healthBar = PlayerHealth("white", (50,585), self.player.health)
		self.playerScoreShadow = PlayerScore("black", (35,10))					#player ship will be selected by user
		self.playerScore = PlayerScore("white", (34,10))					#player ship will be selected by user
		self.playerLivesShadow = PlayerLives("black", (351,586), self.player.lives) 			
		self.playerLives = PlayerLives("white", (350,585), self.player.lives) 			
		self.pauseText1 = PauseGameText("white", "PAUSED", 36, (200,200))
		self.pauseText2 = PauseGameText("white", "press 'p' to return", 26, (200, 250))	

		#create the sprite groups to which the respective sprites belong
		self.spriteList = pygame.sprite.LayeredUpdates()
		self.spriteList.add(self.playerScoreShadow)
		self.spriteList.add(self.playerScore)
		self.spriteList.add(self.healthBarShadow)
		self.spriteList.add(self.healthBar)
		self.spriteList.add(self.playerLivesShadow)
		self.spriteList.add(self.playerLives)
		self.spriteList.add(self.player)

		self.projectileList = pygame.sprite.Group()
		self.enemyList = pygame.sprite.Group()
		self.enemyProjectileList = pygame.sprite.Group()
		self.tokenList = pygame.sprite.Group()	
		self.pauseMenuItems = pygame.sprite.Group()
		self.pauseMenuItems.add(self.pauseText1)
		self.pauseMenuItems.add(self.pauseText2)

		#define game sounds and music		
		self.projectileSound = pygame.mixer.Sound("laser shot.wav")
		self.shipExplosion = pygame.mixer.Sound("ship explosion.wav")
		self.gameSuccess = pygame.mixer.Sound("success.wav")
		self.music = pygame.mixer.music.load("01_Make_It_Bun_Dem.wav")
		pygame.mixer.music.play()
	
		#control mapping for player
		self.key_map = {
			pygame.K_w: [self.player.keyUp, self.player.keyDown],
			pygame.K_s: [self.player.keyDown, self.player.keyUp],
			pygame.K_a: [self.player.keyLeft, self.player.keyRight],
			pygame.K_d: [self.player.keyRight, self.player.keyLeft],
			pygame.K_UP: [self.player.keyUp, self.player.keyDown],
	                pygame.K_DOWN: [self.player.keyDown, self.player.keyUp],
	                pygame.K_LEFT: [self.player.keyLeft, self.player.keyRight],
	                pygame.K_RIGHT: [self.player.keyRight, self.player.keyLeft]
		}
	
		#limit game clock 
		self.gameClock = pygame.time.Clock()
		self.gameClock.tick(30)

		#demo day enemies 
		for i in range(10):
			self.enemy = EnemyShip((random.randrange(0, 350), random.randrange(0, 350)))
			self.spriteList.add(self.enemy)
			self.enemyList.add(self.enemy)
			self.enemiesRemaining += 1
	
		# draw and display on screen
		pygame.display.update()
		pygame.display.flip()

	def gameLoop(self):
		#game loop
		while self.runningGame:
			
			#read in events from queue
			for event in pygame.event.get():
				#on QUIT event, exit the game loop
				if event.type == pygame.QUIT:
					self.runningGame = False
				#if a key is pressed, act based on library definition
				elif event.type == pygame.KEYDOWN and event.key in self.key_map:
					self.key_map[event.key][0]()
				#if a key is released, act based on library definition
				elif event.type == pygame.KEYUP and event.key in self.key_map:
					self.key_map[event.key][1]() 
				#if a space bar is pressed, fire the projectile
				#if p is pressed, pause the game
				elif event.type == pygame.KEYDOWN:
					self.keyPresses = pygame.key.get_pressed()
					#if a space bar is pressed, fire the projectile
					if self.keyPresses[K_SPACE] == 1:
						self.bullet = Projectile([self.player.rect.x + 17, self.player.rect.y])
						self.spriteList.add(self.bullet)
        					self.projectileList.add(self.bullet)
						self.projectileSound.play()
					#if p is pressed, pause the game
					elif self.keyPresses[K_p] == 1:
						self.pausedGame = not self.pausedGame

			#whilst the game is not paused
			if (not self.pausedGame):
				
				#move the background image - yTranslation
				if self.changeFrame:
					self.yScaler += 1
					self.changeFrame = False#moves every other frame
				else: 
					self.changeFrame = True 
			
				if self.yScaler == 1400:
					self.yScaler = 0		
			
				#sprite collision detection between sprites and projectiles
				for projectile in self.projectileList:
		
					#form the list of collisions
					self.hitList = pygame.sprite.spritecollide(projectile, self.enemyList, True)
					
					#for every collision, remove the sprite and increase player score
							
					for hits in self.hitList:
						#killing enemy has a 1/11 chance of producing a power up				
						self.tokenChance = random.randrange(0,1)				
						if (self.tokenChance == 0):
							self.levelUpToken = PowerUp(projectile.rect.center, random.randrange(1,4))
							self.tokenList.add(self.levelUpToken)
							self.spriteList.add(self.levelUpToken)
		
						projectile.kill()
						self.playerScore.increase()
						self.playerScoreShadow.increase()
						self.shipExplosion.play()
						self.enemiesRemaining -= 1
						
					if projectile.rect.y == 0:
						self.projectileList.remove(projectile)
						self.projectileList.remove(projectile)
						projectile.kill()
						self.gameSuccess.play()
		
				#enemy random fire pattern - unpredictable
				for enemyShip in self.enemyList:
		
					#each enemy will have a 1/200 chance of firing a projectile at the player
					self.number = random.randrange(0, 200)
					if (self.number == 5):
						self.enemyProjectile = EnemyProjectile((enemyShip.rect.x, enemyShip.rect.y))
						self.spriteList.add(self.enemyProjectile)
						self.enemyProjectileList.add(self.enemyProjectile)
		
				#hit detection of enemy projectiles with player
				self.enemyProjectileCollideList = pygame.sprite.spritecollide(self.player, self.enemyProjectileList, True)
		
				#reduce health if hit
				self.healthBar.hit(len(self.enemyProjectileCollideList))
				self.healthBarShadow.hit(len(self.enemyProjectileCollideList))
		
				#hit detection of tokens with player ship
				self.tokenCollideList = pygame.sprite.spritecollide(self.player, self.tokenList, True)
		
				for token in self.tokenCollideList:		
						
					#each token in the token list will grant the player a bonus
					#increase playerLives by one
					if (token.tokenType == 1):
						self.playerLives.increase()
						self.playerLivesShadow.increase()
					#increase playerHealth by 50
					elif (token.tokenType == 2):
						self.healthBar.increaseHealth(50)
						self.healthBarShadow.increaseHealth(50)
					#spawn 3 projectiles that travel in 3 directions		
					elif (token.tokenType == 3):
						projectile = TriProjectile((self.player.rect.x, self.player.rect.y), 0)
						projectile1 = TriProjectile((self.player.rect.x, self.player.rect.y), 1)
						projectile2 = TriProjectile((self.player.rect.x, self.player.rect.y), 2)
						self.projectileList.add(projectile)
						self.projectileList.add(projectile1)
						self.projectileList.add(projectile2)
						self.spriteList.add(projectile)
						self.spriteList.add(projectile1)
						self.spriteList.add(projectile2)
		
				#reduce lives if health becomes zero
				if self.healthBar.health <= 0:
					self.playerLives.decrease()
					self.healthBar.newHealth(100)
					self.healthBarShadow.newHealth(100)			
		
				#animate the wallpaper on screen
	        	        self.window.blit(self.backgroundImage, (0, self.yScaler))
	        	        self.window.blit(self.backgroundImage, (0,self.yScaler - 1400))
				
				#game finished upon success
				if self.enemiesRemaining == 0 and not self.levelComplete:
					self.gameSuccess.play()
					self.levelComplete = True
			
				#animate the sprites
				self.spriteList.update()
	        	        self.spriteList.draw(self.window)
			        pygame.display.flip()
				self.spriteList.clear(self.window, self.screen)
				
				self.gameClock.tick(120)	
			else:
				pygame.display.flip()
				self.spriteList.clear(self.window, self.screen)
				self.window.fill(pygame.Color("black"))
				self.pauseMenuItems.update()
				self.pauseMenuItems.draw(self.window)
				pygame.display.flip()
	
