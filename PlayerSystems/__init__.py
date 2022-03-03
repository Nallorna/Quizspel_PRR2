class Player:
    _Player_list = []
    _Database_Path = "PlayerDatabase.txt"

    def __new__(cls, name = False, playertag = False) -> object:
        """
        Check if the object should create a new player, load a previous and if the Args are correctly used. Also
        checks if the tag is usable.

        Args:
            name: The Players name
            playertag: The tag used to load a former player
        """
        if playertag or playertag == "":
            with open(cls._Database_Path) as f:
                playerinfo = [
                    n for n in f.readlines()
                    if playertag == n.split(",")[-1].replace("\n", "")
                ]
                if playerinfo and "#" in str(playertag):
                    return object.__new__(cls)
                else:
                    raise ReferenceError
        elif name or name == "":
            return object.__new__(cls)
        else:
            raise TypeError

    def __init__(self, name = "No name", playertag = "No tag"):
        """
        Initiates a Player-object. Can load former players using their tag and create new tags to new players

        Args:
            name: The players name
            playertag: If the user wants to load a former player using a Player tag
        """
        playerinfo = self._load_tag(playertag)
        if not playerinfo:
            playerinfo = [name.replace("#", ""), "0", self._create_tag()]
        self._name = playerinfo[0]
        self._score = playerinfo[1]
        self._playertag = playerinfo[2]
        self._save_data()
        self._Player_list.append(self)

    def __str__(self) -> str:
        return self._name

    def __int__(self) -> int:
        return int(self._score)

    def __add__(self, value: int) -> int:
        """
        Adds a value to the self._score attribute

        Args:
            value: A integer value that should be added to the self._score attribute
        """
        if type(value) == int:
            self._score = str(int(self._score) + value)
        else:
            raise TypeError()

    def __getitem__(self, index: int or str):
        """
        Checks if the given index is either a keyword for the objects attributes or their position within the
        __init__ method, and if so return the given attribute

        Args:
            index: Either a str containing the attributes name or its index according to __init__ position

        Returns: An object attribute
        """
        if index in list(vars(self).keys()):
            return getattr(self, index)
        elif index in [
            n for n in range(-(len(list(vars(self).values()))),
                             len(list(vars(self).values())))
        ]:
            return list(vars(self).values())[index]
        else:
            raise IndexError

    def _create_tag(self):
        """
        Creates a new tag based on the last tag in the player database

        Returns: A newly created tag
        """
        with open(self._Database_Path, "r") as file:
            last_tag = file.read().split(",")[-1]
            if last_tag:
                new_tag = "#" + str(
                    int(last_tag.replace("#", "").replace("\n", "")) + 1)
            else:
                new_tag = "#0"
        return new_tag

    def _load_tag(self, tag: str):
        """
        Checks if a tag exists, if so then fetches the player's information that is associated with the tag
        Args:
            tag: A tag consisting of # + a string of digits that is used load a player from a Database

        Returns: Either a list of information about the player that is associated with the tag, or returns False if
        the tag is not found in the Database
        """
        with open(self._Database_Path) as f:
            playerinfo = [n for n in f.readlines() if tag in n]
            if playerinfo:
                playerinfo = playerinfo[0].replace("\n", "").split(",")
            else:
                playerinfo = False
        return playerinfo

    def _save_data(self):
        """
        Stores the attributes of an object onto a database
        """
        playerinfo = self._load_tag(self[-1])
        with open(self._Database_Path, "r") as f:
            filetxt = f.read()
            if playerinfo:
                filetxt = filetxt.replace(",".join(playerinfo),
                                          ",".join(list(vars(self).values())))
            elif bool(filetxt):
                filetxt += "\n" + ",".join(list(vars(self).values()))
            else:
                filetxt += ",".join(list(vars(self).values()))
        with open(self._Database_Path, "w") as f:
            f.write(filetxt)
