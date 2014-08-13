import pygame
import ergame as er

if __name__ == "__main__":

	SCREEN_WIDTH = 1024
	SCREEN_HEIGHT = 768
	
	PLAYER_SIZE = 32
	PLAYER_COLOR = (255, 255, 255)
	PLAYER_SPEED = 1
	PLAYER_BOOST = 1.8
	
	player = er.EwRect(((SCREEN_WIDTH/2)-(PLAYER_SIZE/2)), 768-PLAYER_SIZE*2, PLAYER_SIZE, PLAYER_SIZE, PLAYER_COLOR, 0)

	app = er.EwApp("Test App", SCREEN_WIDTH, SCREEN_HEIGHT)
	pos = er.EwPos(100, 200)

	def update():
		
		pygame.display.flip()
		app.screen.fill((0, 0, 0))
		
		player.draw(app.screen)
		player.move(pygame.key.get_pressed()[pygame.K_UP], 0, PLAYER_SPEED)
		player.move(pygame.key.get_pressed()[pygame.K_w], 0, PLAYER_SPEED)
		player.move(pygame.key.get_pressed()[pygame.K_DOWN], 1, PLAYER_SPEED)
		player.move(pygame.key.get_pressed()[pygame.K_s], 1, PLAYER_SPEED)
		player.move(pygame.key.get_pressed()[pygame.K_LEFT], 2, PLAYER_SPEED)
		player.move(pygame.key.get_pressed()[pygame.K_a], 2, PLAYER_SPEED)
		player.move(pygame.key.get_pressed()[pygame.K_RIGHT], 3, PLAYER_SPEED)
		player.move(pygame.key.get_pressed()[pygame.K_d], 3, PLAYER_SPEED)
		
		if pygame.key.get_pressed()[pygame.K_ESCAPE]:
			app.state = True
		
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				app.state = True
		
	app.run(update)
