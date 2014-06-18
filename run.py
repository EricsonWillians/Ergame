import pygame
import ergame

if __name__ == "__main__":

	app = ergame.EwApp("EW Application", 1024, 768)
	plot = ergame.get_standard_plot()
	print plot
	
	def update():
		
		pygame.display.flip()
		app.screen.fill((255,0,0))
		
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				app.state = True

	app.run(update)
