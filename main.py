from PlayerSystems import *
from QuestionSystems import *
from DatabaseSystems import *
import random as rand
import time
import os


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def ask(question: str, *args: list) -> str:
    """
    Asks the user to answer a question and will only accept pre-showed alternatives
    Args:
        question: The Question that the user will give their input to
        *args: A list of every alternative that is acceptable to answer

    Returns: A string of the users answer

    """
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
    active = False
    def __new__(cls) -> object:
        """
        Kollar om det finns tillräckligt med frågor per spelare
        """
        if cls._Player_list and cls._QuestionType_Dictionary and (len([
            item for sublist in cls._QuestionType_Dictionary.values()
            for item in sublist
        ]) >= 6 * len(cls._Player_list)):
            return object.__new__(cls)
        else:
            raise "Need to initiate at least six Question per Player per round"

    def __init__(self):
        """
        Skapar en dictionary med alla spelare och frågor med hjälp av __neg__(self) och "aktiverar" Turn objektet
        """
        self._QnPDict = -self
        Turn.active = True

    def __neg__(self):
        """
        Checks if any MaAQ objects has been initiated, and if so removes the old ones and creates new ones. Also creates a dictionary with questions to every player

        Returns: A dictionary with questions to every player

        """
        if "MaAQ" in self._QuestionType_Dictionary.keys() and Turn.active:
            for n in range(len(self._QuestionType_Dictionary["MaAQ"])):
                points = int(self._QuestionType_Dictionary["MaAQ"][n])
                del self._QuestionType_Dictionary["MaAQ"][n]
                MaAQ(points)
        for key in self._QuestionValue_Dictionary.keys():
            rand.shuffle(self._QuestionValue_Dictionary[key])
        retdict = {}
        for n in range(5,len(self._Player_list)*5+5,5):
            playerquestions = []
            for value in self._QuestionValue_Dictionary.values():
                playerquestions += value[n-5:n]
                rand.shuffle(playerquestions)
            retdict[self._Player_list[(n-1)//5]] = playerquestions
        return retdict

    def __call__(self):
        for m in range(6):
            for n in self._Player_list:
                print(f"{n}: {self._QnPDict[n][m]}")
                svar = input() == self._QnPDict[n][m]
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
        """
        Creates a scoreboard from all active players players, as well as all players stored in the database
        Returns:

        """
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
        MaAQ(15)

    for key, value in dict(sQDB("QuizQA.txt")).items():
        SAQ(key, value.replace("Svar: ",""))

    for n in range(-(-len(BQS._QuestionValue_Dictionary[15])//2)):
        [MaAQ(5),MaAQ(10),MaAQ(15)]

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
