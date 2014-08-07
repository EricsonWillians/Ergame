import pygame
import pygame.mouse as pymo
import ergame as er

if __name__ == "__main__":
	
	pos = er.EwPositioningSystem(2, 1)
	app = er.EwApp("EW Application", pos.get_w(), pos.get_h())

	def update():
		
		pygame.display.flip()
		app.screen.fill((0,0,0))
		
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				app.state = True

	app.run(update)
