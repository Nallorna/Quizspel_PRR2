from abc import *
import random as rand


class BQS(ABC):  # Basic Question System
    _QuestionType_Dictionary = {}
    _QuestionValue_Dictionary = {5: [], 10: [], 15: []}

    @abstractmethod
    def __new__(cls, points: int):
        if cls.__name__ not in cls._QuestionType_Dictionary.keys():
            cls._QuestionType_Dictionary[cls.__name__] = []
        if points not in cls._QuestionValue_Dictionary.keys():
            cls._QuestionType_Dictionary[points] = []
        return object.__new__(cls)

    def __init__(self, question: str, answer: str, points: int):
        self._question = question.replace("\n", "")
        self._answer = answer.replace("\n", "").lower()
        self._points = points
        return self._QuestionType_Dictionary[self.__class__.__name__].append(
            self), self._QuestionValue_Dictionary[points].append(self)

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

    def __eq__(self, answer):
        if self._answer == answer.lower():
            return self._points
        else:
            return 0

    def __len__(self):
        return len(vars(self))

    def __str__(self):
        return self[0]

    def __int__(self):
        return self._points


class SAQ(BQS):  # Singel Answer Question
    def __new__(cls, *args):
        if len(args) == 2 and all([type(n) == str for n in args]):
            super().__new__(cls, 10)
            return object.__new__(cls)
        else:
            raise TypeError()

    def __init__(self, question: str, answer: str):
        answer = answer.replace("Svar: ", "")
        super().__init__(question, answer, 10)


class MAQ(BQS):  # Multiple Answer Question
    def __new__(cls, question: str, answer: str, alternatives: list):
        if all([
            type(question) == str,
            type(answer) == str,
            type(alternatives) == list
        ]):
            if answer in alternatives:
                super().__new__(cls, 5)
                return object.__new__(cls)
            else:
                raise ValueError()
        else:
            raise TypeError()

    def __init__(self, question: str, answer: str, alternatives: list):
        super().__init__(question, answer, 5)
        rand.shuffle(alternatives)
        self._alternatives = {["A", "B", "C"][n]: alternatives[n].replace("\n", "")
                              for n in range(3)}

    def __getitem__(self, index):
        attrlist = list(vars(self).values())
        if index <= len(attrlist):
            attr = attrlist[index]
            if type(attr) == dict:
                return "".join(
                    [f"\t{key}: {value}" for (key, value) in attr.items()])
            else:
                return attrlist[index]
        else:
            raise IndexError

    def __eq__(self, answer):

        if answer.lower() == list(self._alternatives.keys())[
            list(map(lambda x: x.lower(), self._alternatives.values())).index(
                    self._answer)].lower() or answer.lower() == self._answer:
            return self._points
        else:
            return 0

    def __str__(self):
        return self[0] + "\n" + self[3]


class MaAQ(BQS):  # Mathematic Answer Question
    def __new__(cls, points):
        if points in [5, 10, 15]:
            super().__new__(cls, points)
            return object.__new__(cls)
        else:
            raise "Points error"

    def __init__(self, points: int):
        Random_Integers = [
            rand.randint(points - 4, points + 6),
            rand.randint(points - 4, points + 6)
        ]
        Arithmetic_Signs = ["+", "-", "*", "/"][rand.randint(0, 3)]
        if Arithmetic_Signs == "/":
            Random_Integers[0] = Random_Integers[0] * Random_Integers[1]
        _question = f"{Random_Integers[0]}{Arithmetic_Signs}{Random_Integers[1]}"
        _answer = str(round(eval(_question)))
        _points = points
        super().__init__(f"\nVad är:{_question}?\n", _answer, _points)
