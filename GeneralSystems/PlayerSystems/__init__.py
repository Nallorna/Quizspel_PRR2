class Player:
    _Player_list = []
    _Database_Path = "PlayerDatabase.txt"

    def __new__(cls, name=False, playertag=False):
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

    def __init__(self, name="No name", playertag="No tag"):

        playerinfo = self._load_tag(playertag)
        if not playerinfo:
            playerinfo = [name.replace("#", ""), "0", self._create_tag()]
        self._name = playerinfo[0]
        self._score = playerinfo[1]
        self._playertag = playerinfo[2]
        self._save_data()
        return self._Player_list.append(self)

    def __str__(self):
        return self._name

    def __int__(self):
        return int(self._score)

    def __add__(self, value):
        if type(value) == int:
            self._score = str(int(self._score) + value)
        else:
            raise TypeError()

    def __getitem__(self, index):
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
        with open(self._Database_Path, "r") as file:
            last_tag = file.read().split(",")[-1]
            if last_tag:
                new_tag = "#" + str(
                    int(last_tag.replace("#", "").replace("\n", "")) + 1)
            else:
                new_tag = "#0"
        return new_tag

    def _load_tag(self, tag):
        with open(self._Database_Path) as f:
            playerinfo = [n for n in f.readlines() if tag in n]
            if playerinfo:
                playerinfo = playerinfo[0].replace("\n", "").split(",")
            else:
                playerinfo = False
        return playerinfo

    def _save_data(self):
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
