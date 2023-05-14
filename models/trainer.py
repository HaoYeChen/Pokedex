class Trainer:
    def __init__(self, id, name, pokemon):
        self.__id = id
        self.__name = name
        self.__pokemon = pokemon

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def pokemon(self):
        return self.__pokemon