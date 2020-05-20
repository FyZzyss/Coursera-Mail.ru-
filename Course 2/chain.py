class NullHandler:

    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, value):
        if self.__successor:
           return self.__successor.handle(obj, value)


class StrHandler(NullHandler):

    def handle(self, obj, value):
        if value.get_type() is str:
            if isinstance(value, EventGet):
               return obj.string_field
            elif isinstance(value, EventSet):
                obj.string_field = value.get_data()
        else:
            return super().handle(obj, value)


class FloatHandler(NullHandler):

    def handle(self, obj, value):
        if value.get_type() is float:
            if isinstance(value, EventGet):
                return obj.float_field
            elif isinstance(value, EventSet):
                obj.float_field = value.get_data()
        else:
            return super().handle(obj, value)


class IntHandler(NullHandler):

    def handle(self, obj, value):
        if value.get_type() is int:
            if isinstance(value, EventGet):
                return obj.integer_field
            elif isinstance(value, EventSet):
                obj.integer_field = value.get_data()
        else:
            return super().handle(obj, value)


class EventGet:

    def __init__(self, type):
        self.__type = type

    def get_type(self):
        return self.__type


class EventSet:

    def __init__(self, data):
        self.__data = data
        self.__type = type(self.__data)

    def get_type(self):
        return self.__type

    def get_data(self):
        return self.__data

'''obj = SomeObject()
obj.integer_field = 42
obj.float_field = -18.6664
obj.string_field = "some text"

chain = IntHandler(FloatHandler(StrHandler(NullHandler)))
print(chain.handle(obj, EventGet(float)))
print(chain.handle(obj, EventGet(str)))

print(type(-18.6664))'''