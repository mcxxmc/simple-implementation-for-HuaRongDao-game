import pygame

class Character():
    ''' the class for 10 characters '''

    def __init__(self, name, width, height, topleft, blocklength):
        ''' width and height are in the unit of blocklength; 1 or 2 for example '''

        self.name = name
        self.width = width
        self.height = height
        self.topleft = topleft
        self.blocklength = blocklength

        self.occupied = []  # index(es) of occupied block(s) in Field.blocks

        self.fontname = None
        self.fontsize = 24
        self.fontcolor = (166, 166, 166)
        self.font = pygame.font.Font(self.fontname, self.fontsize)
        self.img = self.font.render(str(self.name), True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.topleft
        self.rect.width = self.width * self.blocklength - 30  # leave some space
        self.rect.height = self.height * self.blocklength - 30  # leave some space

    def change_location(self, topleft):
        self.topleft = topleft
        self.rect.topleft = self.topleft
        self.rect.width = self.width * self.blocklength - 30
        self.rect.height = self.height * self.blocklength - 30
