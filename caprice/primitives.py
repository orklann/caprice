# -*- coding=utf-8 -*-

class GObject:
    """Base class for all primitives class.
    """
    UNDEFINED_NUMBER = -1

    def __init__(self):
        self.obj_num = self.UNDEFINED_NUMBER
        self.generation_num = self.UNDEFINED_NUMBER
        self.offset = self.UNDEFINED_NUMBER

class GNumber(GObject):
    """GNumber is the Python class for PDF number object.
    """
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

    def compile_str(self):
        return self.__str__()

    def compile_bytes(self):
        return self.bytes()

class GBoolean(GObject):
    """GBoolean is the Python class for PDF boolean object.
    """
    def __init__(self, val):
        super().__init__()
        self.value = val;

    def __str__(self):
        if not isinstance(self.value, bool):
            raise Exception('GBoolean.value is not a bool value.')
        if self.value:
            return "true"
        else:
            return "false"

    def bytes(self):
        return str.encode(self.__str__())

    def compile_str(self):
        return self.__str__()

    def compile_bytes(self):
        return self.bytes()