class Trainer:
    def __init__(self, id, name, pokemon):
        self.__id = id  # Initialize the private attribute __id with the provided id
        self.__name = name
        self.__pokemon = pokemon

    @property
    def id(self):
        return self.__id  # Getter method for the private attribute

    @property
    def name(self):
        return self.__name

    @property
    def pokemon(self):
        return self.__pokemon
