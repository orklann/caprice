# -*- coding=utf-8 -*-
"""
Classes represents PDF primitives objects
"""

from unittest import result


UNDEFINED_NUMBER = -1

class GObject:
    """
    Base class for all primitives class.
    """
    def __init__(self):
        self.obj_num = UNDEFINED_NUMBER
        self.generation_num = UNDEFINED_NUMBER
        self.offset = UNDEFINED_NUMBER

class GNumber(GObject):
    """
    GNumber is the Python class for PDF number object.
    """
    def __init__(self, val):
        super().__init__()
        self.value = val
    
    def __str__(self):
        if isinstance(self.value, int):
            return str(self.value)
        elif isinstance(self.value, float):
            return str(self.value)
        else:
            raise Exception('GNumber.value is invalid, should be either int or float')

    def bytes(self):
        return str.encode(self.__str__())

    def compile_str(self):
        return self.__str__()

    def compile_bytes(self):
        return self.bytes()

class GBoolean(GObject):
    """
    GBoolean is the Python class for PDF boolean object.
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

class GLiteralString(GObject):
    """
    GLiteralString is the Python class for PDF literal string object
    """
    ESCAPE_SEQUENCES = {
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t',
        '\b': '\\b',
        '\f': '\\f',
        '(': '\\(',
        ')': '\\)',
        '\\': '\\\\'
    }

    def __init__(self, val):
        super().__init__()
        self.value = val

    def __str__(self):
        if not isinstance(self.value, str):
            raise Exception("GLiteralString.value is not a str.")
        result = "("
        for c in self.value:
            if c in self.ESCAPE_SEQUENCES:
                esc = self.ESCAPE_SEQUENCES[c]
            else:
                esc = c
            result += esc
        result += ")"
        return result

    def bytes(self):
        return str.encode(self.__str__())

    def compile_str(self):
        return self.__str__()

    def compile_bytes(self):
        return self.bytes()

class GHexString(GObject):
    """
    GHexString is the Python class for hexademical string object.
    """
    def __init__(self, val):
        super().__init__()
        self.value = val
    
    def __str__(self):
        if not isinstance(self.value, str):
            raise Exception("GHexString.value is not a str.")
        result = "<"
        result += "".join("{:02X}".format(ord(c)) for c in self.value)
        result += ">"
        return result

    def bytes(self):
        return str.encode(self.__str__())

    def compile_str(self):
        return self.__str__()

    def compile_bytes(self):
        return self.bytes()

class GName(GObject):
    """
    GName is the Python class for PDF name objects.
    """
    def __init__(self, val):
        super().__init__()
        self.value = val

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        if not isinstance(self.value, str):
            raise Exception("GName.value is not a str.")
        # We compile GName by using the simplest method: Adding `/`` at the 
        # beginning, Because we assume self.value we pass in will be a normal 
        # string without special characters. For more details, see 7.3.5 
        return "/" + self.value

    def bytes(self):
        return str.encode(self.__str__())

    def compile_str(self):
        return self.__str__()

    def compile_bytes(self):
        return self.bytes()

class GNull(GObject):
    """
    GNull is the Python class for PDF null object
    """
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "null"

    def bytes(self):
        return str.encode("null")

    def compile_str(self):
        return self.__str__()

    def compile_bytes(self):
        return self.bytes()


class GArray(GObject):
    """
    GArray is the Python class for PDF array object
    """
    def __init__(self):
        super().__init__()
        self.array = []

    def __str__(self):
        result = "["
        result += " ".join(ele.compile_str() for ele in self.array)
        result += "]"
        return result

    def bytes(self):
        return str.encode(self.__str__())

    def compile_str(self):
        return self.__str__()

    def compile_bytes(self):
        return self.bytes()