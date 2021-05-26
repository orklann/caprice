# -*- coding=utf-8 -*-

class GObject(object):
    UNDEFINED_NUMBER = -1

    def __init__(self):
        self.obj_num = self.UNDEFINED_NUMBER
        self.generation_num = self.UNDEFINED_NUMBER
        self.offset = self.UNDEFINED_NUMBER

class GNumber(GObject):
    def __init__(self, val):
        super().__init__()
        self.value = val
    
    def __str__(self):
        if isinstance(self.value, int):
            return "%d" % self.value
        elif isinstance(self.value, float):
            return "%f" % self.value
        else:
            raise Exception('GNumber.value is invalid, should be either int or float')

    def bytes(self):
        return str.encode(self.__str__())