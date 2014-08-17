import pygame
import ergame as er

if __name__ == "__main__":

    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768

    app = er.EwApp("Test App", SCREEN_WIDTH, SCREEN_HEIGHT)
    
    THICKNESS = 0
    RED = (255, 0, 0)
    player = er.EwRect(300, 300, 300, 300, RED, THICKNESS)
    
    def update():

        pygame.display.flip()
        app.screen.fill((0, 0, 0))
        
        player.draw(app.screen)
        
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            app.state = True

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                app.state = True

    app.run(update)
