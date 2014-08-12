import pygame
import ergame as er

if __name__ == "__main__":

	SCREEN_WIDTH = 1024
	SCREEN_HEIGHT = 768

	app = er.EwApp("Test App", SCREEN_WIDTH, SCREEN_HEIGHT)
	scenes = [er.EwScene("Scene " + str(x)) for x in range(10)]
	plot = er.EwPlot(scenes)
	print plot.current
	
	def update():
		
		pygame.display.flip()
		app.screen.fill((0, 0, 0))
		
		if app.check_if_time_has_elapsed_in_milliseconds(150):
			if pygame.key.get_pressed()[pygame.K_RIGHT]:
				plot.next()
			if pygame.key.get_pressed()[pygame.K_LEFT]:
				plot.previous()
		
		if plot.get_scene() == "Scene 0":
			er.EwFont(100, 100, 300, 100, None, "Scene 0", (255, 255, 255)).draw(app.screen)
		if plot.get_scene() == "Scene 1":
			er.EwFont(100, 100, 300, 100, None, "Scene 1", (255, 255, 255)).draw(app.screen)
		if plot.get_scene() == "Scene 2":
			er.EwFont(100, 100, 300, 100, None, "Scene 2", (255, 255, 255)).draw(app.screen)
		if plot.get_scene() == "Scene 3":
			er.EwFont(100, 100, 300, 100, None, "Scene 3", (255, 255, 255)).draw(app.screen)
		if plot.get_scene() == "Scene 4":
			er.EwFont(100, 100, 300, 100, None, "Scene 4", (255, 255, 255)).draw(app.screen)
		if plot.get_scene() == "Scene 5":
			er.EwFont(100, 100, 300, 100, None, "Scene 5", (255, 255, 255)).draw(app.screen)
		if plot.get_scene() == "Scene 6":
			er.EwFont(100, 100, 300, 100, None, "Scene 6", (255, 255, 255)).draw(app.screen)
		if plot.get_scene() == "Scene 7":
			er.EwFont(100, 100, 300, 100, None, "Scene 7", (255, 255, 255)).draw(app.screen)
		if plot.get_scene() == "Scene 8":
			er.EwFont(100, 100, 300, 100, None, "Scene 8", (255, 255, 255)).draw(app.screen)
		if plot.get_scene() == "Scene 9":
			er.EwFont(100, 100, 300, 100, None, "Scene 9", (255, 255, 255)).draw(app.screen)
		
		if pygame.key.get_pressed()[pygame.K_ESCAPE]:
			app.state = True
		
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				app.state = True
		
	app.run(update)
