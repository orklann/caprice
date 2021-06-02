# -*- coding=utf-8 -*-
"""
Classes represents PDF primitives objects
"""

import zlib

UNDEFINED_NUMBER = -1

class GObject:
    """Base class for all primitives class.
    """
    def __init__(self):
        pass

class GNumber(GObject):
    """GNumber is the Python class for PDF number object.
    """
    def __init__(self, val):
        if not isinstance(val, (int, float)):
            raise TypeError("GNumber's value must be int or float")
        super().__init__()
        self.value = val
    
    def __str__(self):
        if isinstance(self.value, int):
            return str(self.value)
        elif isinstance(self.value, float):
            return str(self.value)
        else:
            raise TypeError('GNumber.value is invalid, should be either int or float')

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
        if not isinstance(val, bool):
            raise TypeError("GBoolean's value must be a bool.")
        super().__init__()
        self.value = val;

    def __str__(self):
        if not isinstance(self.value, bool):
            raise TypeError('GBoolean.value is not a bool value.')
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
    """GLiteralString is the Python class for PDF literal string object
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
        if not isinstance(val, str):
            raise TypeError("GLiteralString's value must be a str")
        super().__init__()
        self.value = val

    def __str__(self):
        if not isinstance(self.value, str):
            raise TypeError("GLiteralString.value is not a str.")
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
    """GHexString is the Python class for hexademical string object.
    """
    def __init__(self, val):
        if not isinstance(val, str):
            raise TypeError("GHexString's value must be a str.")
        super().__init__()
        self.value = val
    
    def __str__(self):
        if not isinstance(self.value, str):
            raise TypeError("GHexString.value is not a str.")
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
    """GName is the Python class for PDF name objects.
    """
    def __init__(self, val):
        if not isinstance(val, str):
            raise TypeError("GName's value must be a str.")
        super().__init__()
        self.value = val

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        if not isinstance(self.value, str):
            raise TypeError("GName.value is not a str.")
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
    """GNull is the Python class for PDF null object
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
    """GArray is the Python class for PDF array object
    """
    def __init__(self):
        super().__init__()
        self.array = []

    def __str__(self):
        result = "["
        result += " ".join(ele.compile_str() for ele in self.array)
        result += "]"
        return result

    def append(self, val):
        if not isinstance(val, (GBoolean, GHexString, GArray, GDictionary,\
            GNull, GNumber, GLiteralString, GName, GRef)):
            raise TypeError("GArray's append method's input is not invalid: "\
             + str(type(val)))
        self.array.append(val)

    def bytes(self):
        return str.encode(self.__str__())

    def compile_str(self):
        return self.__str__()

    def compile_bytes(self):
        return self.bytes()

class GDictionary(GObject):
    """GDictionary is the Python class for PDF dictionary object.
    """
    def __init__(self):
        super().__init__()
        self.dict = {}

    def set(self, key, obj):
        if not isinstance(key, GName):
            raise TypeError("GDictionary's key must be a GName instance, for set() method.")
        if not isinstance(obj, (GBoolean, GHexString, GArray, GDictionary,\
            GNull, GNumber, GLiteralString, GName, GRef)):
            raise TypeError("GDictionary's `obj` parameter in set method is not invalid: "\
             + str(type(obj)))
        self.dict[key] = obj

    def get(self, key):
        return self.dict[key]

    def __str__(self):
        result = "<<"
        result += " ".join(key.compile_str() + " " + val.compile_str() \
            for key, val in self.dict.items())
        result += ">>"
        return result
    
    def bytes(self):
        return str.encode(self.__str__())

    def compile_str(self):
        return self.__str__()

    def compile_bytes(self):
        return self.bytes()

class GStream(GObject):
    """GStream is the Python class for PDF stream object.
    """
    def __init__(self):
        super().__init__()
        self.dict = GDictionary()
        self.content = b""

    def set_content(self, c):
        if not isinstance(c, str):
            raise TypeError("GStream's `c` paramter of set_content method is not a str.")
        self.content = str.encode(c)

    def bytes(self):
        # Flate encoder by zlib
        encoded_bytes = self.encoded_bytes()
        
        # Set /Length in dictionary 
        length = len(encoded_bytes)
        self.dict.set(GName("Length"), GNumber(length))
        
        # We use FlateDecode filter, that's to say, 
        # we encode content by using flate encoder.
        # Set /Filter in dictionary
        self.dict.set(GName("Filter"), GName("FlateDecode"))

        # Construct result as bytes
        result = self.dict.compile_bytes() + b"\r\n" # dictionary bytes
        result += b"stream\r\n" # stream keyword bytes
        result += encoded_bytes + b"\r\n" # encoded content bytes
        result += b"\r\n" + b"endstream\r\n"
        return result

    def encoded_bytes(self):
        # Flate encoder by zlib, flate encoding is our default encoding for
        # GStream object.
        return zlib.compress(self.content)

    def compile_bytes(self):
        return self.bytes()

class GIndirect(GObject):
    """GIndirect is the Python class for PDF indirect object.
    """
    def __init__(self):
        super().__init__()
        self.obj_num = UNDEFINED_NUMBER
        self.generation_num = UNDEFINED_NUMBER
        self.offset = UNDEFINED_NUMBER
        self.object = None
    
    def set_obj_num(self, val):
        if not isinstance(val, int):
            raise TypeError("GIndirect's set_obj_num()'s argument is not a int")
        self.obj_num = val

    def set_generation_num(self, val):
        if not isinstance(val, int):
            raise TypeError("GIndirect's set_generation_num()'s argument is not a int")
        self.generation_num = val

    def set_offset(self, val):
        if not isinstance(val, int):
            raise TypeError("GIndirect's set_offset()'s argument is not a int")
        self.offse = val

    def set_object(self, obj):
        if not isinstance(obj, (GBoolean, GHexString, GArray, GDictionary,\
            GNull, GNumber, GLiteralString, GName, GStream)):
            raise TypeError("GIndirect's set_object()'s argument is invalid: " \
                + str(type(obj)))
        self.object = obj

    def bytes(self):
        if self.object is None:
            raise Exception("GIndirect's object is None.")
        result = str.encode("%d %d obj\r\n" % (self.obj_num, self.generation_num))
        result += self.object.compile_bytes()
        if (isinstance(self.object, GStream)):
            result += b"endobj\r\n\r\n"
        else:
            result += b"\r\nendobj\r\n\r\n"
        return result

    def compile_bytes(self):
        return self.bytes()

    def compile_str(self):
        if self.object is None:
            raise Exception("GIndirect's object is None.")
        result = "%d %d obj\r\n" % (self.obj_num, self.generation_num)
        result += self.object.compile_str()
        if (isinstance(self.object, GStream)):
            result += "endobj\r\n\r\n"
        else:
            result += "\r\nendobj\r\n\r\n"
        return result

    def get_ref(self):
        r = GRef()
        r.set_obj_num(self.obj_num)
        r.set_generation_num(self.generation_num)
        return r

    def get_ref_str(self):
        return self.get_ref().compile_str()

class GRef(GObject):
    """GRef is the Python class for PDF ref string. 
    A ref string is like: 1 0 R
    """

    def __init__(self):
        super().__init__()
        self.obj_num = UNDEFINED_NUMBER
        self.generation_num = UNDEFINED_NUMBER

    def set_obj_num(self, val):
        if not isinstance(val, int):
            raise TypeError("GRef's set_obj_num()'s argument is not a int")
        self.obj_num = val

    def set_generation_num(self, val):
        if not isinstance(val, int):
            raise TypeError("GRef's set_generation_num()'s argument is not a int")
        self.generation_num = val

    def __str__(self):
        return "%d %d R" % (self.obj_num, self.generation_num)

    def bytes(self):
        return str.encode(self.__str__())

    def compile_str(self):
        return self.__str__()

    def compile_bytes(self):
        return self.bytes()