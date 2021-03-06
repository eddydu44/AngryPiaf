import pygame,sys
import functions.init as init
import functions.move as move
from functions.classes import *

def run():
    # Fausse boucle for afin de récupérer les évènements
    for event in pygame.event.get():
        # Cas du déclenchement de la croix de la fenêtre
        if event.type == pygame.QUIT:
            init.running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN :
            if 19 < init.pygame.mouse.get_pos()[0] < 71 and 19 < init.pygame.mouse.get_pos()[1] < 71 :
                if init.muteVerif:
                    init.muteVerif = False
                    pygame.mixer.music.play(-1)
                else:
                    init.muteVerif = True
                    pygame.mixer.music.pause()
        # Si l'utilisateur appuie sur escape
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                init.inMove = False
                init.middle.empty()
                for obj in init.allSprites :
                    obj.reset()
            if event.key == pygame.K_ESCAPE:
                init.running = False
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_b : # on remet l'oiseau sur catapulte si b
                init.inMove = False
                for obj in init.allSprites :
                    if type(obj) == birdObj :
                        obj.reset()
            if event.key == pygame.K_i:
                if init.muteVerif:
                    init.muteVerif = False
                    pygame.mixer.music.play(-1)
                else:
                    init.muteVerif = True
                    pygame.mixer.music.pause()


        # Si l'utilisateur redimensionne la fenêtre
        '''elif event.type == pygame.VIDEORESIZE:
            init.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            # On remet à l'échelle l'image de fond
            init.background = pygame.transform.scale(init.background, (event.w, event.h))'''
        # Des qu'on lache la souris après avoir bougé l'oiseau, on lance la simu
        if event.type == pygame.MOUSEBUTTONUP and init.verif and init.inMove == False:
            init.verif = False
            move.run()

    # Update des tous les groupes de sprite
    init.middle.update()
    init.middle.draw(init.surface)

    init.front.update()
    init.front.draw(init.surface)

    if init.muteVerif :
        init.surface.blit(init.mute, (20, 20))
    else :
        init.surface.blit(init.music, (20, 20))

    init.pygame.display.update()

    # Vérification que l'oiseau est en mouvement
    if init.bird.pointnb == -1:
            init.inMove = False