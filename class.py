class shape:
    def __init__(self, x=0, y=0):

        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x
    def set_x(self, value):
        self.__x = value

obj = shape("5","5")
print(obj.get_x())

