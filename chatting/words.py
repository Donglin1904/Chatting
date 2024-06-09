import pygame.font
from pygame.sprite import Sprite

class Words(Sprite):

    def __init__(self,main):
        super().__init__()
        self.screen=main.screen
        self.screen_rect=self.screen.get_rect()
        self.data=main.data
        self.words_colour=(30,30,30)
        self.font=pygame.font.SysFont(None,48)
        self._print_words()

    def _print_words(self):
        self.words_image=self.font.render(self.data,True,self.words_colour,None)
        self.words_rect=self.words_image.get_rect()
        self.words_height=self.words_image.get_height()
        self.words_rect.bottom=self.screen_rect.bottom
        self.words_rect.left=self.screen_rect.left

    def draw_words(self):
        self.screen.blit(self.words_image,self.words_rect)

    def move(self):
        self.words_rect.y -= self.words_height
        
            