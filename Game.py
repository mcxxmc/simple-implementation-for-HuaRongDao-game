import pygame

import Block
import Field

RED = (255, 0, 0)
BLUE = (0, 0, 255)

default_size = (640,640)
default_bl = 100
default_topleft = (120, 70)
default_preset = {"CaoCao": ((120, 270), 2, 2), "ZhangFei": ((120, 70), 1, 2),
                  "ZhaoYun": ((220, 70), 1, 2), "HuangZhon": ((320, 70), 1, 2),
                  "GuanYu": ((320, 470), 2, 1),"Machao": ((420,70), 1, 2),
                  "Soldier1": ((320, 270), 1, 1), "Soldier2": ((420, 270), 1, 1),
                  "Soldier3": ((120, 470), 1, 1), "Soldier4": ((220, 470), 1, 1)
                  }  # 横刀立马

default_field_size = [5, 4]  # [rows, columns]
default_exit = [13, 14, 17, 18]

valid_directions = {pygame.K_w: "up", pygame.K_s: "down", pygame.K_a: "left", pygame.K_d: "right"}


class Game:
    ''' the main file'''

    def __init__(self, size, bl, topleft):

        pygame.init()
        pygame.display.set_caption("Hua Rong Dao")

        self.screen = pygame.display.set_mode(size)

        self.running = True

        self.field = Field.Field(bl, topleft, default_preset)

        self.test_mode = False

        self.select = False  # whether a character has been selected
        self.selected_character = None
        self.monitor = self.get_monitor()   # it should be CaoCao


        self.win = False

        self.resetButton = Block.Block("Reset", 50, (80, 560))  # reset
        self.resetButton.rect.width = 130

        self.font = pygame.font.Font(None, 24)

        self.text = "Moving CaoCao to Button Mid"
        self.render(self.text)

    def render(self, text):
        self.text = text
        self.img = self.font.render(text, True, RED)

    def get_monitor(self):
        for i in self.field.characters:
            if i.name == ("CaoCao"):
                return i


    def begin_test(self):
        self.test_mode = True

    def end_test(self):
        self.test_mode = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.resetButton.rect.collidepoint(event.pos):
                        self.field.reset()
                        print("Field Reset")
                        self.monitor = self.get_monitor()
                    else:
                        for i in self.field.characters: # every instances should have attributes img and rect
                            if i.rect.collidepoint(event.pos):
                                if self.select == False:
                                    self.selected_character = i
                                    self.select = True
                                    self.render(i.name + " is selected and ready to move; use WASD for directions")
                                    print(i.name + " is selected and ready to move; use WASD for directions")
                                    break
                elif event.type == pygame.KEYDOWN and self.select:
                    direction = event.key
                    if direction in valid_directions:
                        new_topleft = self.field.movable(valid_directions[direction], self.selected_character)
                        if new_topleft != None:
                            self.selected_character.change_location(new_topleft)
                            self.field.deploy(self.selected_character)
                            self.render(self.selected_character.name + " has moved.")
                            print(self.selected_character.name + " has moved.")
                            self.selected_character = None
                            self.select = False

                        else:
                            self.selected_character = None
                            self.select = False
                            self.render("Invalid Move! Please reselect.")
                            print("Invalid Move! Please reselect.")
                    else:
                        self.selected_character = None
                        self.select = False
                        self.render("Invalid Instruction! Please reselect.")
                        print("Invalid Instruction! Please reselect.")


            # print(self.monitor.topleft)
            if self.monitor.occupied == default_exit:
                self.win = True

            if self.win:
                self.render("congratulations!")
                print("congratulations!")
                self.field.reset()
                print("Field Reset")
                self.monitor = self.get_monitor()
                self.win = False

            self.screen.fill(BLUE)

            for character in self.field.characters:
                pygame.draw.rect(self.screen, RED, character.rect)
                self.screen.blit(character.img, character.topleft)

            if self.test_mode:
                for block in self.field.blocks:
                    self.screen.blit(block.img, block._topleft)

            pygame.draw.rect(self.screen, RED, self.resetButton)
            self.screen.blit(self.resetButton.img, (80, 560))
            self.screen.blit(self.img, (10, 10))
            pygame.display.flip()

        pygame.quit()

test_game = Game(default_size, default_bl, default_topleft)
# test_game.begin_test()

if __name__ == '__main__':
    test_game.run()