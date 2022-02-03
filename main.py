from GeneralSystems.PlayerSystems import *
from GeneralSystems.QuestionSystems import *
from GeneralSystems.DatabaseSystems import *
import random as rand
import time
import os


def ask(question: str, *args):
    userinput = ""
    if type(list(args)[0]) != list:
        args = [args]
    args = [
        str(arg).lower()
        for arg in [item for sublist in args for item in sublist]
    ]
    indices = [str(n + 1) for n in range(len(args))]
    while userinput.lower() not in args + indices:
        userinput = input("{}\n\t{}\n".format(
            question, "\n\t".join(
                [f"{index}) {arg}" for index, arg in zip(indices, args)])))
        os.system("clear")
    return userinput


class Turn(Player, BQS):
    def __new__(cls):
        if cls._Player_list and cls._QuestionType_Dictionary and (len([
            item for sublist in cls._QuestionType_Dictionary.values()
            for item in sublist
        ]) >= 6 * len(cls._Player_list)):
            return object.__new__(cls)
        else:
            raise "Need to initiate atleast six Question per Player per round"

    def __init__(self):
        self.QnPDict = -self
        self.active = True

    def __neg__(self):
        if "MaAQ" in self._QuestionType_Dictionary.keys():
            for n in range(len(self._QuestionType_Dictionary["MaAQ"])):
                points = int(self._QuestionType_Dictionary["MaAQ"][n])
                del self._QuestionType_Dictionary["MaAQ"][n]
                MaAQ(points)
        return {
            self._Player_list[n]: rand.sample([
                item for sublist in [
                                        rand.choices(n, k=1)
                                        for n in self._QuestionType_Dictionary.values()
                                    ] + [
                                        rand.choices(n, k=1)
                                        for n in self._QuestionValue_Dictionary.values()
                                    ] for item in sublist
            ], k=6)
            for n in range(len(self._Player_list))
        }

    def __call__(self):
        for m in range(6):
            for n in self._Player_list:
                print(f"{n}: {self.QnPDict[n][m]}")
                svar = input() == self.QnPDict[n][m]
                if svar:
                    print("Rätt!\n")
                else:
                    print("Fel!\n")
                n + svar
        self._Player_list.sort(key=lambda x: x[1])
        score_str = f"{self._Player_list[0][0]} vann!\n"
        for n in self._Player_list:
            score_str += f"\n{n[0]}: {n[1]}"
            n._save_data()
        self.QnPDict = -self
        return print(score_str), input("Klicka enter för att fortsätta\n"), time.sleep(1)

    def scoreboard(self):
        with open(self._Database_Path, "r") as file:
            scoreboard_str = [
                f"{player[0]} - {player[1]} Poäng" for player in sorted(
                    [player.split(",")[0:2] for player in file.readlines()],
                    key=lambda x: x[1],
                    reverse=True)[0:3]
            ]
            scoreboard_str = "- S C O R E B O A R D -\n" + "\n".join([
                f"{n + 1}: " + scoreboard_str[n]
                for n in range(len(scoreboard_str))
            ])
            return scoreboard_str


if __name__ == '__main__':
    for key, value in dict(mQDB("QuizQAalternativ.txt")).items():
        MAQ(key, value[0], value)
    for key, value in dict(sQDB("QuizQA.txt")).items():
        SAQ(key, value)
    [(MaAQ(5), MaAQ(15)) for n in range(17)]
    [MaAQ(10) for n in range(16)]

    player_creator = True
    while player_creator:
        player_amount = ""
        while not player_amount.isnumeric():
            player_amount = input("Hur många spelare?\n")
        for player in range(int(player_amount)):

            loadplayer = ""
            while type(loadplayer) != bool:
                os.system("clear")
                loadplayer = ask(
                    f"Spelare {player + 1}\nVill du ladda in en tidigare spelare med en spelaretag?",
                    "ja", "nej")
                if loadplayer.lower() == "ja":
                    playertag = input("Vad är din tag\n")
                    try:
                        playerexists = Player(playertag=playertag)
                        loadplayer = True
                    except ReferenceError:
                        print("Använd en gilltig tag")
                        time.sleep(2)
                elif loadplayer.lower() == "nej":
                    Player(input("Vad vill du heta?\n"))
                    loadplayer = True
        player_creator = False

    GameRound = Turn()

    while GameRound.active:
        os.system("clear")
        direction_dict = {
            "1": "spela en omgång",
            "2": "scoreboard",
            "3": "avsluta"
        }
        direction = ask("Vill du", list(direction_dict.values()))
        direction_dict = list(direction_dict.items())

        if direction in direction_dict[0]:
            GameRound()
        elif direction in direction_dict[1]:
            print(GameRound.scoreboard())
            input("\nKlicka enter om du är klar")
        else:
            GameRound.active = False
