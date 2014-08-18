import pygame
import pygame.mouse as pymo
import ergame as er
from random import randrange
from random import uniform

if __name__ == "__main__":

    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    DISTANCE_LIMIT = 2048

    app = er.EwApp("Espace", SCREEN_WIDTH, SCREEN_HEIGHT)
    
    bg = er.EwScrollingImage(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, "bg.png", er.EwDirection("SOUTH"))
    
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
    
    class Enemy(er.EwRect):
        
        SIZES = [x for x in range(0, 64, 16)]
        
        def __init__(self):

            self.health = 0
            self.speed = uniform(0.3, 0.8)
            w = randrange(16, Enemy.SIZES[len(Enemy.SIZES)-1])
            h = randrange(16, Enemy.SIZES[len(Enemy.SIZES)-1])
            c = (randrange(125, 255), randrange(125, 255), randrange(125, 255))
            er.EwRect.__init__(self, randrange(8, SCREEN_WIDTH-w), -randrange(h, DISTANCE_LIMIT), w, h, c)
            
        def translate(self):
            self.y += self.speed
            
    class Raid:
        
        def __init__(self):
            
            pass 
            
    en = [Enemy() for x in range(1, 128)]

    ammo_state = er.EwFont(16, 16, 128+16, 16, "Squares Bold Free.otf", "Ammo State: Normal", (255, 255, 255))

    def update():
        
        pygame.display.flip()
        bg.draw(app.screen)
        ammo_state.draw(app.screen)
        player.draw(app.screen)
        [x.draw(app.screen) for x in en]
        [x.translate() for x in en]

        if not pygame.key.get_pressed()[pygame.K_LSHIFT]:
            player.move(pygame.key.get_pressed()[pygame.K_UP], er.EwDirection("NORTH"), PLAYER_SPEED)
            player.move(pygame.key.get_pressed()[pygame.K_w], er.EwDirection("NORTH"), PLAYER_SPEED)
            player.move(pygame.key.get_pressed()[pygame.K_DOWN], er.EwDirection("SOUTH"), PLAYER_SPEED)
            player.move(pygame.key.get_pressed()[pygame.K_s], er.EwDirection("SOUTH"), PLAYER_SPEED)
            player.move(pygame.key.get_pressed()[pygame.K_LEFT], er.EwDirection("WEST"), PLAYER_SPEED)
            player.move(pygame.key.get_pressed()[pygame.K_a], er.EwDirection("WEST"), PLAYER_SPEED)
            player.move(pygame.key.get_pressed()[pygame.K_RIGHT], er.EwDirection("EAST"), PLAYER_SPEED)
            player.move(pygame.key.get_pressed()[pygame.K_d], er.EwDirection("EAST"), PLAYER_SPEED)
        else:
            player.move(pygame.key.get_pressed()[pygame.K_UP], er.EwDirection("NORTH"), PLAYER_BOOST)
            player.move(pygame.key.get_pressed()[pygame.K_w], er.EwDirection("NORTH"), PLAYER_BOOST)
            player.move(pygame.key.get_pressed()[pygame.K_DOWN], er.EwDirection("SOUTH"), PLAYER_BOOST)
            player.move(pygame.key.get_pressed()[pygame.K_s], er.EwDirection("SOUTH"), PLAYER_BOOST)
            player.move(pygame.key.get_pressed()[pygame.K_LEFT], er.EwDirection("WEST"), PLAYER_BOOST)
            player.move(pygame.key.get_pressed()[pygame.K_a], er.EwDirection("WEST"), PLAYER_BOOST)
            player.move(pygame.key.get_pressed()[pygame.K_RIGHT], er.EwDirection("EAST"), PLAYER_BOOST)
            player.move(pygame.key.get_pressed()[pygame.K_d], er.EwDirection("EAST"), PLAYER_BOOST)
            
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if app.check_if_time_has_elapsed_in_milliseconds(80):
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
            #   if er.EwCol(bullet, test_wall)():

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            app.state = True
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                app.state = True

    app.run(update)
