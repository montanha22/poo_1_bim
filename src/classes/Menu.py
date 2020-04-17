import pygame
import sys
from classes.Spritesheet import SpriteSheet

def post_resize_event(resolution):
    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size = resolution, w = resolution[0],h=resolution[1]))

def post_fullscreen():
    pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))

def draw_text(text, font, color, surface, pos):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (pos[0]-5,pos[1])
    surface.blit(textobj, textrect)

class Button():

    def __init__(self):
        pass


def main_menu(gm):
    click=False
    button_nomouseover = pygame.image.load("sprites/menu/blue_button01.png").convert()
    button_mouseover = pygame.image.load("sprites/menu/blue_button03.png").convert()
    background = pygame.image.load("sprites/menu/game_background_4.png").convert()
    mouseover_sound = pygame.mixer.Sound("sprites/menu/click1.ogg")
    click_sound = pygame.mixer.Sound("sprites/menu/switch3.ogg")
    can_play_sound=True
    while True:
        gm.clock.tick(60)
        gm.fake_screen.blit(background,background.get_rect())
        draw_text('main menu', gm.font, (255, 255, 255), gm.fake_screen, (960,20))
        mx, my = gm.mousepos
 
        play_button = pygame.Rect(860, 100, 200, 50)
        options_button = pygame.Rect(860, 200, 200, 50)
        quit_button = pygame.Rect(860, 300, 200, 50)  

        if play_button.collidepoint((mx, my)):
            gm.fake_screen.blit(button_mouseover,play_button)
            draw_text("Play Game",gm.font,(81, 87, 70),gm.fake_screen,play_button.center)
            if can_play_sound:
                can_play_sound = False
                pygame.mixer.Sound.play(mouseover_sound)
            if click:
                pygame.mixer.Sound.play(click_sound)
                gm.restartGame()
                gm.onExecute()
        else:
            gm.fake_screen.blit(button_nomouseover,play_button)
            draw_text("Play Game",gm.font,(81, 87, 70),gm.fake_screen,play_button.center)
            can_play_sound = True

        if options_button.collidepoint((mx, my)):
            gm.fake_screen.blit(button_mouseover,options_button)
            draw_text("Settings",gm.font,(81, 87, 70),gm.fake_screen,options_button.center)
            if click:
                options(gm)
        else:
            gm.fake_screen.blit(button_nomouseover,options_button)
            draw_text("Settings",gm.font,(81, 87, 70),gm.fake_screen,options_button.center)

        if quit_button.collidepoint((mx, my)):
            gm.fake_screen.blit(button_mouseover,quit_button)
            draw_text("Quit Game",gm.font,(81, 87, 70),gm.fake_screen,quit_button.center)
            if click:
                quit_confirmation(gm) 
        else:
            gm.fake_screen.blit(button_nomouseover,quit_button)
            draw_text("Quit Game",gm.font,(81, 87, 70),gm.fake_screen,quit_button.center)
        
 
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gm.onCleanup()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit_confirmation(gm)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        

        #Display refresh
        gm.screen.blit(pygame.transform.scale(gm.fake_screen, gm.window_resolution), (0, 0))
        pygame.display.flip()

        #Fix mouse position because of resizing
        gm.mousepos = list(pygame.mouse.get_pos())
        gm.mousepos = [int(gm.mousepos[0]*gm.original_resolution[0]/gm.window_resolution[0]),int(gm.mousepos[1]*gm.original_resolution[1]/gm.window_resolution[1])]
        gm.mousepos=tuple(gm.mousepos)

def options(gm):
    running = True
    click=False
    button_nomouseover = pygame.image.load("sprites/menu/blue_button01.png").convert()
    button_mouseover = pygame.image.load("sprites/menu/blue_button03.png").convert()
    while running:
        gm.clock.tick(60)
        gm.fake_screen.fill((0,0,0))
        draw_text('options', gm.font, (255, 255, 255), gm.fake_screen, ((960,20)))

        mx, my = gm.mousepos

        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        button_3 = pygame.Rect(50, 300, 200, 50)
        button_4 = pygame.Rect(50, 400, 200, 50)
        mainmenu_button = pygame.Rect(50, 500, 200, 50)
        if button_1.collidepoint((mx, my)):
            gm.fake_screen.blit(button_mouseover,button_1)
            draw_text("960 x 540",gm.font,(81, 87, 70),gm.fake_screen,button_1.center)
            if click:
                post_resize_event((960,540))
        else:
            gm.fake_screen.blit(button_nomouseover,button_1)
            draw_text("960 x 540",gm.font,(81, 87, 70),gm.fake_screen,button_1.center)
        if button_2.collidepoint((mx, my)):
            gm.fake_screen.blit(button_mouseover,button_2)
            draw_text("1280 x 720",gm.font,(81, 87, 70),gm.fake_screen,button_2.center)
            if click:
                post_resize_event((1280,720))
        else:
            gm.fake_screen.blit(button_nomouseover,button_2)
            draw_text("1280 x 720",gm.font,(81, 87, 70),gm.fake_screen,button_2.center)
        if button_3.collidepoint((mx, my)):
            gm.fake_screen.blit(button_mouseover,button_3)
            draw_text("1920 x 1080",gm.font,(81, 87, 70),gm.fake_screen,button_3.center)
            if click:
                post_resize_event((1920,1080))
        else:
            gm.fake_screen.blit(button_nomouseover,button_3)
            draw_text("1920 x 1080",gm.font,(81, 87, 70),gm.fake_screen,button_3.center)
        if button_4.collidepoint((mx, my)):
            gm.fake_screen.blit(button_mouseover,button_4)
            draw_text("Fullscreen",gm.font,(81, 87, 70),gm.fake_screen,button_4.center)
            if click:
                post_fullscreen()        
        else:
            gm.fake_screen.blit(button_nomouseover,button_4)
            draw_text("Fullscreen",gm.font,(81, 87, 70),gm.fake_screen,button_4.center)
        if mainmenu_button.collidepoint((mx, my)):
            gm.fake_screen.blit(button_mouseover,mainmenu_button)
            draw_text("Main Menu",gm.font,(81, 87, 70),gm.fake_screen,mainmenu_button.center)
            if click:
                return 
        else:
            gm.fake_screen.blit(button_nomouseover,mainmenu_button)
            draw_text("Main Menu",gm.font,(81, 87, 70),gm.fake_screen,mainmenu_button.center)
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gm.onCleanup()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running=False
            
            if event.type == pygame.VIDEORESIZE:
                if gm.window_resolution != event.size:
                    gm.fullscreen = False
                    gm.window_resolution=event.size
                    gm.screen = pygame.display.set_mode(event.size)
                    gm.screen.blit(pygame.transform.scale(gm.fake_screen, gm.window_resolution), (0, 0))
                    pygame.display.flip()
            
            if event.type == pygame.USEREVENT + 1:
                if not gm.fullscreen:
                    gm.fullscreen = True
                    gm.window_resolution = gm.monitor_resolution
                    gm.screen = pygame.display.set_mode(gm.window_resolution, pygame.FULLSCREEN)
                    gm.screen.blit(pygame.transform.scale(gm.fake_screen, gm.window_resolution), (0, 0))
                    pygame.display.flip()

        #Display refresh
        gm.screen.blit(pygame.transform.scale(gm.fake_screen, gm.window_resolution), (0, 0))
        pygame.display.flip()

        #Fix mouse position because of resizing
        gm.mousepos = list(pygame.mouse.get_pos())
        gm.mousepos = [int(gm.mousepos[0]*gm.original_resolution[0]/gm.window_resolution[0]),int(gm.mousepos[1]*gm.original_resolution[1]/gm.window_resolution[1])]
        gm.mousepos=tuple(gm.mousepos)

def game_over(gm):
    click = False
    running = True
    gm.endGame()
    button_nomouseover = pygame.image.load("sprites/menu/blue_button01.png").convert()
    button_mouseover = pygame.image.load("sprites/menu/blue_button03.png").convert()
    while running:
        gm.clock.tick(60)
        gm.fake_screen.fill((0,0,0))
        draw_text('Game Over', gm.font, (255, 255, 255), gm.fake_screen, (960,20))
 
        mx, my = gm.mousepos
 
        mainmenu_button = pygame.Rect(50, 100, 200, 50)
        if mainmenu_button.collidepoint((mx, my)):
            gm.fake_screen.blit(button_mouseover,mainmenu_button)
            draw_text("Main Menu",gm.font,(81, 87, 70),gm.fake_screen,mainmenu_button.center)
            if click:
                return 
        else:
            gm.fake_screen.blit(button_nomouseover,mainmenu_button)
            draw_text("Main Menu",gm.font,(81, 87, 70),gm.fake_screen,mainmenu_button.center)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gm.onCleanup()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        #Display refresh
        gm.screen.blit(pygame.transform.scale(gm.fake_screen, gm.window_resolution), (0, 0))
        pygame.display.flip()

        #Fix mouse position because of resizing
        gm.mousepos = list(pygame.mouse.get_pos())
        gm.mousepos = [int(gm.mousepos[0]*gm.original_resolution[0]/gm.window_resolution[0]),int(gm.mousepos[1]*gm.original_resolution[1]/gm.window_resolution[1])]
        gm.mousepos=tuple(gm.mousepos)

def pause_menu(gm):
    click=False
    running = True
    button_nomouseover = pygame.image.load("sprites/menu/blue_button01.png").convert()
    button_mouseover = pygame.image.load("sprites/menu/blue_button03.png").convert()
    while running:
        gm.clock.tick(60)
        gm.fake_screen.fill((0,0,0))
        draw_text('pause menu', gm.font, (255, 255, 255), gm.fake_screen, (960,20))
 
        mx, my = gm.mousepos
 
        resume_button = pygame.Rect(50, 100, 200, 50)
        mainmenu_button = pygame.Rect(50, 200, 200, 50)
        if resume_button.collidepoint((mx, my)):
            gm.fake_screen.blit(button_mouseover,resume_button)
            draw_text("Resume",gm.font,(81, 87, 70),gm.fake_screen,resume_button.center)
            if click:
                return 
        else:
            gm.fake_screen.blit(button_nomouseover,resume_button)
            draw_text("Resume",gm.font,(81, 87, 70),gm.fake_screen,resume_button.center)
        if mainmenu_button.collidepoint((mx, my)):
            gm.fake_screen.blit(button_mouseover,mainmenu_button)
            draw_text("Main Menu",gm.font,(81, 87, 70),gm.fake_screen,mainmenu_button.center)
            if click:
                gm.endGame()
                return 
        else:
            gm.fake_screen.blit(button_nomouseover,mainmenu_button)
            draw_text("Main Menu",gm.font,(81, 87, 70),gm.fake_screen,mainmenu_button.center)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gm.onCleanup()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        #Display refresh
        gm.screen.blit(pygame.transform.scale(gm.fake_screen, gm.window_resolution), (0, 0))
        pygame.display.flip()

        #Fix mouse position because of resizing
        gm.mousepos = list(pygame.mouse.get_pos())
        gm.mousepos = [int(gm.mousepos[0]*gm.original_resolution[0]/gm.window_resolution[0]),int(gm.mousepos[1]*gm.original_resolution[1]/gm.window_resolution[1])]
        gm.mousepos=tuple(gm.mousepos)

def quit_confirmation(gm):
    click=False
    button_nomouseover = pygame.image.load("sprites/menu/blue_button01.png").convert()
    button_mouseover = pygame.image.load("sprites/menu/blue_button03.png").convert()
    while True:
        gm.clock.tick(60)
        gm.fake_screen.fill((0,0,0))
        draw_text('do you really want to quit?', gm.font, (255, 255, 255), gm.fake_screen, (960,20))
 
        mx, my = gm.mousepos
 
        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(350, 100, 200, 50)

        if button_1.collidepoint((mx, my)):
            gm.fake_screen.blit(button_mouseover,button_1)
            draw_text("Cancel",gm.font,(81, 87, 70),gm.fake_screen,button_1.center)
            if click:
                return
        else:
            gm.fake_screen.blit(button_nomouseover,button_1)
            draw_text("Cancel",gm.font,(81, 87, 70),gm.fake_screen,button_1.center)
        if button_2.collidepoint((mx, my)):
            gm.fake_screen.blit(button_mouseover,button_2)
            draw_text("Quit",gm.font,(81, 87, 70),gm.fake_screen,button_2.center)
            if click:
                gm.onCleanup()
        else:
            gm.fake_screen.blit(button_nomouseover,button_2)
            draw_text("Quit",gm.font,(81, 87, 70),gm.fake_screen,button_2.center)

 
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gm.onCleanup()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        #Display refresh
        gm.screen.blit(pygame.transform.scale(gm.fake_screen, gm.window_resolution), (0, 0))
        pygame.display.flip()

        #Fix mouse position because of resizing
        gm.mousepos = list(pygame.mouse.get_pos())
        gm.mousepos = [int(gm.mousepos[0]*gm.original_resolution[0]/gm.window_resolution[0]),int(gm.mousepos[1]*gm.original_resolution[1]/gm.window_resolution[1])]
        gm.mousepos=tuple(gm.mousepos)