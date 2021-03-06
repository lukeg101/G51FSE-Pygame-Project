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
from Shield import Shield

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
		self.inMainMenu = True
		self.inControlMenu = False
		self.enemiesRemaining = 0	
		self.hasShield = False
		self.gameOver = False
	
		#create and define the screen window
		self.screenHeight, self.screenWidth = 600, 400
		self.window = pygame.display.set_mode([self.screenWidth, self.screenHeight])
		pygame.display.set_caption("Logic Wars")
		pygame.display.set_icon(pygame.image.load("ORgateShipRevision1.png"))

		#define game background
		self.screen = pygame.Surface([self.screenWidth, self.screenHeight])
		self.imagePath = "TestDayBackground.png"			
		self.backgroundImage = pygame.image.load(self.imagePath).convert()		
		self.yScaler = 0
		self.changeFrame = True	

		#create all sprites for the game
		#ship sprite
		self.shipxPos, self.shipyPos = 200, 400						
		self.player = PlayerShip((self.shipxPos, self.shipyPos))		
		#health bar sprites
		self.healthBarShadow = PlayerHealth("black", (51,586), self.player.health)			
		self.healthBar = PlayerHealth("white", (50,585), self.player.health)
		self.playerScoreShadow = PlayerScore("black", (35,10))					
		self.playerScore = PlayerScore("white", (34,10))					
		self.playerLivesShadow = PlayerLives("black", (351,586), self.player.lives) 			
		self.playerLives = PlayerLives("white", (350,585), self.player.lives) 		
		#pause menu sprites	
		self.pauseText1 = PauseGameText("white", "PAUSED", 36, (200,200))
		self.pauseText2 = PauseGameText("white", "press 'p' to return", 26, (200, 250))	
		#main menu sprites
		self.mainMenuText1 = PauseGameText("white", "Logic Wars", 36, (200, 200))
		self.mainMenuText2 = PauseGameText("white", "Press SPACE to Start!", 26, (200, 250))
		self.mainMenuText3 = PauseGameText("white", "Press 'c' to see the controls", 26, (200, 300))
		#control menu sprites
		self.controlMenuText1 = PauseGameText("white", "SHIP CONTROLS", 36, (200, 200))
		self.controlMenuText2 = PauseGameText("white", "w,a,s,d for ship movement", 26, (200, 250))
		self.controlMenuText3 = PauseGameText("white", "arrow keys for ship movement", 26, (200, 300))
		self.controlMenuText4 = PauseGameText("white", "SPACE to fire", 26, (200, 350))
		self.controlMenuText5 = PauseGameText("white", "p to pause the game", 26, (200, 400))
		self.controlMenuText6 = PauseGameText("white", "press c to return to menu ", 26, (200, 500))
		self.controlMenuText7 = PauseGameText("white", "or SPACE to start game", 26, (200, 520))
		#game over sprites
		self.gameOverText1 = PauseGameText("white", "GAME OVER", 36, (200, 200))
		self.gameOverText2 = PauseGameText("white", "you lost the game", 26, (200, 400))
		self.gameOverText3 = PauseGameText("white", "press ENTER to retry", 26, (200, 420))
		
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

		#adds sprites to the pause menu group
		self.pauseMenuItems = pygame.sprite.Group()
		self.pauseMenuItems.add(self.pauseText1)
		self.pauseMenuItems.add(self.pauseText2)

		#adds sprites to the main menu group
		self.mainMenuItems = pygame.sprite.Group()
		self.mainMenuItems.add(self.mainMenuText1)
		self.mainMenuItems.add(self.mainMenuText2)
		self.mainMenuItems.add(self.mainMenuText3)

		#adds sprites to the control menu group
		self.controlMenuItems = pygame.sprite.Group()
		self.controlMenuItems.add(self.controlMenuText1)
		self.controlMenuItems.add(self.controlMenuText2)
		self.controlMenuItems.add(self.controlMenuText3)
		self.controlMenuItems.add(self.controlMenuText4)
		self.controlMenuItems.add(self.controlMenuText5)
		self.controlMenuItems.add(self.controlMenuText6)
		self.controlMenuItems.add(self.controlMenuText7)

		#adds sprites to the game over group
		self.gameOverMenuItems = pygame.sprite.Group()
		self.gameOverMenuItems.add(self.gameOverText1)
		self.gameOverMenuItems.add(self.gameOverText2)
		self.gameOverMenuItems.add(self.gameOverText3)
		

		#define game sounds and music		
		self.projectileSound = pygame.mixer.Sound("laser shot.wav")
		self.shipExplosion = pygame.mixer.Sound("ship explosion.wav")
		self.bomb = pygame.mixer.Sound("bomb.wav")
		self.triProjectileSound = pygame.mixer.Sound("triProjectile.ogg")
		self.shieldSound = pygame.mixer.Sound("shield.wav")
		self.addHealth = pygame.mixer.Sound("addHealth.wav")
		self.gameOverSound = pygame.mixer.Sound("gameOver.wav")
		self.oneUp = pygame.mixer.Sound("oneUp.ogg")
		self.music = pygame.mixer.music.load("01_Make_It_Bun_Dem.wav")

		#pygame.mixer.music.play()

		#control mapping for player in game
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

		#spawns the first batch of enemies
		self.spawnEnemies()
	
		# draw and display on screen
		pygame.display.update()
		pygame.display.flip()

	"""displays the main menu items"""
	def mainMenu(self):
		self.spriteList.clear(self.window, self.screen)
		self.window.fill(pygame.Color("black"))
		self.mainMenuItems.update()	
		self.mainMenuItems.draw(self.window)
		pygame.display.flip()

	"""stars the game"""
	def startGame(self):
		self.inMainMenu = not self.inMainMenu

	"""displaus the control menu items"""
	def controlMenu(self):
		self.spriteList.clear(self.window, self.screen)
		self.window.fill(pygame.Color("black"))
		self.controlMenuItems.update()	
		self.controlMenuItems.draw(self.window)
		pygame.display.flip()

	"""determines whether or not the player is in the control menu"""
	def controlsEvent(self):
		self.inControlMenu = not self.inControlMenu

	"""displays the pause menu items"""
	def pauseMenu(self):
		self.spriteList.clear(self.window, self.screen)
		self.window.fill(pygame.Color("black"))
		self.pauseMenuItems.update()
		self.pauseMenuItems.draw(self.window)
		pygame.display.flip()

	"""displays the game over menu"""
	def gameOverMenu(self):
		pygame.display.flip()
		self.spriteList.clear(self.window, self.screen)
		self.window.fill(pygame.Color("black"))
		self.gameOverMenuItems.update()
		self.gameOverMenuItems.draw(self.window)
		pygame.display.flip()

	"""game controls for when the player is in the main menu"""
	def readMainMenuControls(self):
		#read in events from queue - MAIN MENU CONTROLS
		for event in pygame.event.get():
			#on QUIT event, exit the game loop
			if event.type == pygame.QUIT:
				self.runningGame = False
				#a key is pressed - check the mapping
			elif event.type == pygame.KEYDOWN:
				self.keyPresses = pygame.key.get_pressed()
				#if space is pressed, start the game
				if self.keyPresses[K_SPACE] == 1:
					self.startGame()
				#if c is pressed, show the controls
				elif self.keyPresses[K_c] == 1:
					self.controlsEvent()
				#if p is pressed, pause the game
				elif self.keyPresses[K_p] == 1:
					self.pausedGame = not self.pausedGame

	"""game controls for when the player is at game over screen"""
	def readGameOverControls(self):
		#read in events from queue - GAME OVER CONTROLS
		for event in pygame.event.get():
			#on QUIT event, exit the game loop
			if event.type == pygame.QUIT:
				self.runningGame = False
			#press enter to restart the game
			elif event.type == pygame.KEYDOWN:
				self.keyPresses = pygame.key.get_pressed()
				if self.keyPresses[K_RETURN] == 1:
					self.spriteList.empty()
					self.__init__()
	
	"""game controls for when the player is playing the game"""
	def readGameControls(self):
		#read in events from queue - IN GAME CONTROLS
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

	"""spawns 20 enemies in random locations"""
	def spawnEnemies(self):
		#spawn 20 enemies above the screen frame
		for i in range(20):
			self.enemyShipType = random.randrange(0, 2)
			self.enemy = EnemyShip((random.randrange(0, 350, 50), random.randrange(-100, -33, 40)), self.enemyShipType)
			self.spriteList.add(self.enemy)
			self.enemyList.add(self.enemy)
			self.enemiesRemaining += 1
	
	"""loops until player quit the game"""
	def gameLoop(self):
		#game loop
		while self.runningGame:
			
			#if the game is in the main menu
			if self.inMainMenu:	
	
				#read in the controls for the start menu
				self.readMainMenuControls()

				#controls menu access from main menu
				if self.inControlMenu:
					self.controlMenu()
				else:				
					self.mainMenu()
			
			#if the game is paused
			elif self.pausedGame:
				self.pauseMenu()
				self.readGameControls()

			#if you lose the game - display game over screen
			elif self.gameOver:
				self.gameOverMenu()
				self.readGameOverControls()			

			#whilst the game is not paused or in the main menu or on the game over screen
			if (not self.pausedGame and not self.inMainMenu and not self.gameOver):
	
				#read controls for the player ship
				self.readGameControls()

				#if the player runs out of lives - game over
				if self.player.lives == -1:
					self.gameOver = True
					self.gameOverSound.play()

				#if there are <=5 enemies left, spawn more
				if (self.enemiesRemaining <= 5):
					self.spawnEnemies()

				#adjust the current coords of a shield, if the player has it
				if self.hasShield:
					self.shield.updateLocation((self.player.rect.x + 15, self.player.rect.y - 2))
						
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
		
					#for every collision, remove the sprite and increase player score
					self.hitList = pygame.sprite.spritecollide(projectile, self.enemyList, True)
					
					#if the projectile goes out of bounds - remove it
					if projectile.rect.y <= -20 or projectile.rect.x <= -10 or projectile.rect.x >= 400:
						projectile.kill()

					#for every projectile that hits an enemy
					for hits in self.hitList:
						#killing enemy has a 1/20 chance of producing a power up				
						self.tokenChance = random.randrange(0,20)				
						if (self.tokenChance == 0):
							self.levelUpToken = PowerUp(projectile.rect.center, random.randrange(1,6))
							self.tokenList.add(self.levelUpToken)
							self.spriteList.add(self.levelUpToken)
		
						#remove projectile, reduce enemy count and increase score
						projectile.kill()
						self.playerScore.increase()
						self.playerScoreShadow.increase()
						self.shipExplosion.play()
						self.enemiesRemaining -= 1
		
				#enemy random fire pattern - unpredictable
				for enemyShip in self.enemyList:
		
					#if they reach the bottom of the map - remove enemy
					if enemyShip.rect.y >= 700:
						enemyShip.kill()
						self.enemiesRemaining -= 1

					#each enemy will have a 1/200 chance of firing a projectile at the player
					self.number = random.randrange(0, 200)
					if (self.number == 5):
						self.enemyProjectile = EnemyProjectile((enemyShip.rect.x, enemyShip.rect.y))
						self.spriteList.add(self.enemyProjectile)
						self.enemyProjectileList.add(self.enemyProjectile)
		
				#hit detection of enemy projectiles with player
				self.enemyProjectileCollideList = pygame.sprite.spritecollide(self.player, self.enemyProjectileList, True)
				
				#reduce health if hit
				self.player.takeHit(5 * len(self.enemyProjectileCollideList))
				self.healthBar.newHealth(self.player.health)
				self.healthBarShadow.newHealth(self.player.health)
				self.playerLives.newLives(self.player.lives)
				self.playerLivesShadow.newLives(self.player.lives)
				
				#if enemy ship collides with player ship
				self.enemyShipCollideList = pygame.sprite.spritecollide(self.player, self.enemyList, True)
				
				#reduce player health if collides with enemy ship
				self.player.takeHit(5* len(self.enemyShipCollideList))
				self.healthBar.newHealth(self.player.health)
				self.healthBarShadow.newHealth(self.player.health)
				self.playerLives.newLives(self.player.lives)
				self.playerLivesShadow.newLives(self.player.lives)

				#collision of enemy projectiles and shields 
				for enemyProjectile in self.enemyProjectileList:

					#if enemy projectile goes out of range remove it
					if enemyProjectile.rect.y >= 610:
						enemyProjectile.kill()
					
					#remove shield if it is hit by a projectile
					if self.hasShield and pygame.sprite.collide_rect(self.shield, enemyProjectile):
						enemyProjectile.kill()
						self.shield.kill()
						self.hasShield = not self.hasShield 
		
				#hit detection of tokens with player ship
				self.tokenCollideList = pygame.sprite.spritecollide(self.player, self.tokenList, True)
		
				for token in self.tokenCollideList:							

					#each token in the token list will grant the player a bonus
					#increase playerLives by one
					if (token.tokenType == 1):
						self.player.addLives(1)
						self.playerLives.newLives(self.player.lives)
						self.playerLivesShadow.newLives(self.player.lives)
						self.oneUp.play()
					#increase playerHealth by 20
					elif (token.tokenType == 2):
						self.addHealth.play()
						self.player.addHealth(20)
					#spawn 3 projectiles that travel in 3 directions		
					elif (token.tokenType == 3):
						self.triProjectileSound.play()
						projectile = TriProjectile((self.player.rect.x, self.player.rect.y), 0)
						projectile1 = TriProjectile((self.player.rect.x, self.player.rect.y), 1)
						projectile2 = TriProjectile((self.player.rect.x, self.player.rect.y), 2)
						self.projectileList.add(projectile)
						self.projectileList.add(projectile1)
						self.projectileList.add(projectile2)
						self.spriteList.add(projectile)
						self.spriteList.add(projectile1)
						self.spriteList.add(projectile2)
					#spawns a shield for the player, if they don't already have one
					elif (token.tokenType == 4 and not self.hasShield):
						self.shieldSound.play()
						self.shield = Shield((self.player.rect.x + 15, self.player.rect.y - 2))
						self.spriteList.add(self.shield)
						self.hasShield = True	
					#drops a bomb that destroys all enemy ships
					elif (token.tokenType == 5):
						self.enemiesRemaining = 0
						self.bomb.play()
						for enemy in self.enemyList:
							enemy.remove([self.spriteList, self.enemyList])
		
				#animate the wallpaper on screen
	        	        self.window.blit(self.backgroundImage, (0, self.yScaler))
	        	        self.window.blit(self.backgroundImage, (0,self.yScaler - 1400))
			
				#animate the sprites
				self.spriteList.update()
	        	        self.spriteList.draw(self.window)
			        pygame.display.flip()
				self.spriteList.clear(self.window, self.screen)
				self.gameClock.tick(120)	
