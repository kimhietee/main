a,b,c,d = False,False,False,False

lambda x: True
txt = f'self.attacks[{[i for i in range(5)]}]'
# print(txt)
# for i in range(5):
#     print(f'self.attacks[{i}]')

class Sample:
    def __init__(self):
        self.x = 1
        self.exist = True
        self.__setattr__('y', None) # = self.y = None
        self.__getattribute__('x') # = 1
        try:
            getattr(self, 'z') # = conditional, boolean value
            print('YESS')
        except AttributeError:
            print('NOOO')
    def print_out(self):
        print(f'{'i'}')
        print(self.__dict__) # = object attributes, in dict
    
    def tryy(self):
        haha = lambda q: 100 > 50


klass = Sample()
# klass.print_out()
klass.tryy()

# help(Sample)
