import pygame

class Block:
    ''' the basic block class for both Field and Character'''

    def __init__(self, id, sidelength, topleft):
        '''
        id is the number for identification; sidelength is the width and height;
        topleft is the topleft corner, or (x,y)
        '''
        self._id = id
        self._sl = sidelength
        self._topleft = topleft

        self.is_full = False

        self.fontname = None
        self.fontsize = 36
        self.fontcolor = (166, 166, 166)
        self.font = pygame.font.Font(self.fontname, self.fontsize)
        self.img = self.font.render(str(self._id), True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self._topleft
        self.rect.width = self._sl
        self.rect.height = self._sl

    def set_full(self):
        self.is_full = True

    def is_filled(self):
        return self.is_full

    def get_id(self):
        return self._id

    def get_sl(self):
        return self._sl

    def release(self):
        self.is_full = False