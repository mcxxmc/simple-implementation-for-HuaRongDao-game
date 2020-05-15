import Block
import Character

class Field:
    ''' the 4 columns, 5 rows field for the game '''

    def __init__(self, blocklength, topleft, preset_dic, columns=4, rows=5):
        '''
        blocklength is sidelength in Block class;
        columns and rows are their quantities;
        preset_dic is the initial state of characters,
        format: name:(topleft, width, height). e.g. "CaoCao":((120, 70),2,2)
        '''

        self._bl = blocklength
        self._topleft = topleft
        self._x = topleft[0]
        self._y = topleft[1]
        self.preset_dic = preset_dic

        self.columns = columns
        self.rows = rows

        self.c = [topleft[0] + i*self._bl for i in range(columns)]
        self.r = [topleft[1] + i*self._bl for i in range(rows)]

        self.blocks = []
        self.characters = []

        id = 0
        for i in self.r:
            for j in self.c:
                self.blocks.append(Block.Block(id, self._bl, (j, i) ))
                id += 1

        '''
         so we have some thing like 
        0 1 2 3
        4 5 6 7 
        ......
        '''
        self.generate_characters()


    def generate_characters(self):
        for i in self.preset_dic:
            name = i
            width = self.preset_dic[i][1]
            height = self.preset_dic[i][2]
            topleft = self.preset_dic[i][0]
            character = Character.Character(name, width, height, topleft, self._bl)
            self.characters.append(character)
            self.deploy(character)

    def reset(self):
        ''' redeploy all characters '''
        self.characters = []
        for i in self.blocks:
            i.release()
        self.generate_characters()

    def deploy(self, character):
        ''' deploy the character, fill the block(s)'''
        print("deploying " + character.name)

        column_offset = ( character.topleft[0] - self._x ) // self._bl # x
        row_offset = ( character.topleft[1] - self._y ) // self._bl   # y
        start_id = row_offset * self.columns + column_offset  # some math here
        print("start id = " + str(start_id))

        for i in character.occupied:
            self.blocks[i].release()

        character.occupied = []

        for i in range(character.width):
            for j in range(character.height):
                current_id = start_id + j * self.columns + i
                print("current id = " + str(current_id))
                character.occupied.append(current_id)
                self.blocks[current_id].set_full()
        character.occupied.sort()

        print("character " + character.name + "'s occupied: ")
        print(character.occupied)
        print("\n")

    def movable(self, dirc, character):
        ''' takes in the direction and the character to be moved. Returns new topleft if movable, None otherwise'''
        # the first id is always the smallest and the left top most
        for i in character.occupied:
            if dirc == "up":
                if i - self.columns < 0 :
                    print("Error, out of field. Conflict ID: " + str(i) + " to " + str(i - self.columns ))
                    return None
                elif self.blocks[i-self.columns].is_filled() and i-self.columns not in character.occupied:
                    print("Error, Enemy in your way. Conflict ID: " + str(i) + " to " + str(i-self.columns))
                    return None
            elif dirc == "down":  # consider height
                if i+self.columns > (self.columns * self.rows - 1):
                    print("Error, out of field. Conflict ID: "+ str(i) + " to "  + str(i+self.columns))
                    return None
                elif self.blocks[i+self.columns].is_filled() and i+self.columns not in character.occupied:
                    print("Error, Enemy in your way. Conflict ID: "+ str(i) + " to "  + str(i+self.columns))
                    return None
            elif dirc == "left":
                if i-1 < 0:
                    print("Error, out of field. Conflict ID: " + str(i) + " to " + str(i - 1))
                    return None
                elif (i - 1)%self.columns == self.columns-1:
                    print("Error, out of field. Conflict ID: " + str(i) + " to " + str(i - 1))
                    return None
                elif self.blocks[i-1].is_filled() and i-1 not in character.occupied:
                    print("Error, Enemy in your way. Conflict ID: "+ str(i) + " to "  + str(i - 1))
                    return None
            elif dirc == "right":  # consider width
                if (i + 1)%self.columns == 0:
                    print("Error, out of field. Conflict ID: " + str(i) + " to " + str(i + character.width))
                    return None
                elif self.blocks[i+1].is_filled() and i+1 not in character.occupied:
                    print("Error, Enemy in your way. Conflict ID: "+ str(i) + " to "  + str(i + character.width))
                    return None

        d = {"up": [0, - self._bl], "down": [0, self._bl], "left": [ - self._bl, 0], "right": [self._bl, 0]}
        # the coordinate system is reversed by pygame's nature
        new_offset = (character.topleft[0]+d[dirc][0], character.topleft[1]+d[dirc][1])
        print("Moving " + character.name + " " + dirc + " by 1 block length")
        return new_offset




