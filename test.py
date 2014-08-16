import pygame
import ergame as er

if __name__ == "__main__":

    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768

    app = er.EwApp("Test App", SCREEN_WIDTH, SCREEN_HEIGHT)
    mov = er.EwMovable(0, 0, 0)

    def update():

        pygame.display.flip()
        app.screen.fill((0, 0, 0))

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            app.state = True

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                app.state = True

    app.run(update)
