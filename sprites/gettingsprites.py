import pygame
class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
 
    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """
        pygame.init()
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name)
        self.width = self.sprite_sheet.get_width()
        self.height = self.sprite_sheet.get_height()
 
    def get_image(self, n):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """
        x = int(n * self.width/4)
        y = self.height
        # Create a new blank image
        image = pygame.Surface([x, self.height])
 
        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, int(self.width/4), self.height))
 
        # Assuming black works as the transparent color
        image.set_colorkey((0,0,0))
 
        # Return the image
        return image

def get_image2(filepath):
    img = pygame.image.load(filepath)
    cut = img.get_width()
    imglist = []
    for i in range(4):
        imglist.append(img[:,int(i*cut):int(cut*(i+1)),:])
    return imglist
ss = SpriteSheet('sprites/TopDownCharacter/Character/Character_Down.png')

img = ss.get_image(4)
print(img)