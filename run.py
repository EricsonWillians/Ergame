from erange import R
import pygame
import pygame.mouse as pymo
import ergame as er

if __name__ == "__main__":

	SCREEN_WIDTH = 1024
	SCREEN_HEIGHT = 768

	app = er.EwApp("Espace", SCREEN_WIDTH, SCREEN_HEIGHT)
	
	bg = er.EwScrollingImage(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, "bg.png", 1)
	
	PLAYER_SIZE = 32
	PLAYER_COLOR = (255, 255, 255)
	PLAYER_SPEED = 1
	PLAYER_BOOST = 1.8
	
	player = er.EwRect(((SCREEN_WIDTH/2)-(PLAYER_SIZE/2)), 768-PLAYER_SIZE*2, PLAYER_SIZE, PLAYER_SIZE, PLAYER_COLOR, 1)
	
	class Bullet(er.EwRect):
		
		def __init__(self, x, y):
			
			er.EwRect.__init__(self, x, y, PLAYER_SIZE/2, PLAYER_SIZE/2, PLAYER_COLOR, 1)
			self.shot = False

	ammo = []

	def update():
		
		pygame.display.flip()
		bg.draw(app.screen)
		player.draw(app.screen)
		
		if not pygame.key.get_pressed()[pygame.K_LSHIFT]:
			player.move(pygame.key.get_pressed()[pygame.K_UP], 0, PLAYER_SPEED)
			player.move(pygame.key.get_pressed()[pygame.K_w], 0, PLAYER_SPEED)
			player.move(pygame.key.get_pressed()[pygame.K_DOWN], 1, PLAYER_SPEED)
			player.move(pygame.key.get_pressed()[pygame.K_s], 1, PLAYER_SPEED)
			player.move(pygame.key.get_pressed()[pygame.K_LEFT], 2, PLAYER_SPEED)
			player.move(pygame.key.get_pressed()[pygame.K_a], 2, PLAYER_SPEED)
			player.move(pygame.key.get_pressed()[pygame.K_RIGHT], 3, PLAYER_SPEED)
			player.move(pygame.key.get_pressed()[pygame.K_d], 3, PLAYER_SPEED)
		else:
			player.move(pygame.key.get_pressed()[pygame.K_UP], 0, PLAYER_BOOST)
			player.move(pygame.key.get_pressed()[pygame.K_w], 0, PLAYER_BOOST)
			player.move(pygame.key.get_pressed()[pygame.K_DOWN], 1, PLAYER_BOOST)
			player.move(pygame.key.get_pressed()[pygame.K_s], 1, PLAYER_BOOST)
			player.move(pygame.key.get_pressed()[pygame.K_LEFT], 2, PLAYER_BOOST)
			player.move(pygame.key.get_pressed()[pygame.K_a], 2, PLAYER_BOOST)
			player.move(pygame.key.get_pressed()[pygame.K_RIGHT], 3, PLAYER_BOOST)
			player.move(pygame.key.get_pressed()[pygame.K_d], 3, PLAYER_BOOST)
			
		if pygame.key.get_pressed()[pygame.K_SPACE]:
			if len(ammo) < 16*16:
				ammo.append(Bullet(player.x+((PLAYER_SIZE/2)/2), player.y-PLAYER_SIZE))
			else:
				for bullet in ammo:
					if bullet.y < -bullet.h*3:
						ammo.pop(ammo.index(bullet))
		if len(ammo) > 0:
			for bullet in ammo:
				bullet.y -= 2
				bullet.draw(app.screen)

		if pygame.key.get_pressed()[pygame.K_ESCAPE]:
			app.state = True
		
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				app.state = True

	app.run(update)
