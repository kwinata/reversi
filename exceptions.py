class ReversiException(Exception):
    pass


class InvalidLocationException(ReversiException):
    def __str__(self):
        return self.__name__
