#!/usr/bin/env python

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
	enemyProjectileList = pygame.sprite.Group()
	
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

		#enemy random fire pattern - unpredictable
		for enemyShip in enemyList:

			#each enemy will have a 1/200 chance of firing a projectile at the player
			number = random.randrange(0, 10)
			if (number == 5):
				enemyProjectile = EnemyProjectile((enemyShip.rect.x, enemyShip.rect.y))
				spriteList.add(enemyProjectile)
				enemyProjectileList.add(enemyProjectile)

		#hit detection of enemy projectiles with player
		enemyProjectileCollideList = pygame.sprite.spritecollide(player, enemyProjectileList, True)

		#reduce health if hit
		healthBar.hit(len(enemyProjectileCollideList))
		healthBarShadow.hit(len(enemyProjectileCollideList))

		#reduce lives if health becomes zero
		if healthBar.health <= 0:
			playerLives.decrease()
			healthBar.newHealth(100)
			healthBarShadow.newHealth(100)			

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
