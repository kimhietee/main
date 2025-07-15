class Player:
    def __init__(self):
        self.x = 69

class Fire_Wizard(Player):
    def __init__(self, hp):
        super().__init__()
        self.hp = hp
    def prnt(self):
        pass
import pprint
hah = Fire_Wizard

class Bot(hah):
    def prnt(self):
        # super().prnt()
        pprint.pprint(hah.__name__)

hero = Bot(100)

hero.prnt()