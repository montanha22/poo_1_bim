import pygame

class Button():

    def __init__(self, left, top, width, height, text, gm, image_mouse = "imgs/blue_button03.png", image_nomouse ="imgs/blue_button01.png"):
        self.contour =  pygame.Rect(left, top, width, height)
        self.mouse = image_mouse
        self.nomouse = image_nomouse
        self.text = text
    
    def draw_text(self, text, font, color, surface, pos):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (pos[0]-5,pos[1])
        surface.blit(textobj, textrect)

    def draw(self, mouse, gm):
        if mouse:
            image = self.mouse
        else:
            image = self.nomouse
        gm.fake_screen.blit(pygame.image.load(image).convert(), self.contour)
        self.draw_text(self.text, gm.font, (81,87,70), gm.fake_screen, self.contour.center)
    
    def sound(self, mouse, click, sound_mouse = "sounds/click1.ogg", sound_click = "sounds/switch3.ogg"):
        if mouse:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(sound_mouse))
        elif click:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(sound_click))
    
   
