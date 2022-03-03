from abc import *
import random as rand


class BQS(ABC):  # Basic Question System
    _QuestionType_Dictionary = {}
    _QuestionValue_Dictionary = {}

    @abstractmethod
    def __new__(cls, points: int, **kwargs: tuple) -> object:
        """
        Checks if their exists a key, and associated list, for both the points, and object name in the class
        dictionaries
        Args:
            points: The amount of points that the object attribute self._points will have
            **kwargs: Other keyword arguments that is not used in this method, but used in the __init__ method
        """
        if cls.__name__ not in cls._QuestionType_Dictionary.keys():
            cls._QuestionType_Dictionary[cls.__name__] = []
        if points not in cls._QuestionValue_Dictionary.keys():
            cls._QuestionValue_Dictionary[points] = []
        return object.__new__(cls)

    def __init__(self, question: str, answer: str, points: int):
        """
        Args:
            question: The questions text
            answer: The answer to the question
            points: The amount of points that the question is associated with
        """
        self._question = question.replace("\n", "")
        self._answer = answer.replace("\n", "").lower()
        self._points = points
        self._QuestionType_Dictionary[self.__class__.__name__].append(
            self)
        self._QuestionValue_Dictionary[points].append(self)

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

    def __eq__(self, answer: str) -> int:
        if self._answer == answer.lower():
            return self._points
        else:
            return 0

    def __len__(self) -> int:
        return len(vars(self))

    def __str__(self) -> str:
        return self[0]

    def __int__(self) -> int:
        return self._points


class SAQ(BQS):  # Single Answer Question
    def __new__(cls, question: str, answer: str) -> object:
        """
        Checks if both the question and the answer is of type str and calls the __new__ method from the superclass
        Args:
            question: The questions text
            answer: The answer to the question
        """
        if all([type(n) == str for n in [question, answer]]):
            super().__new__(cls, 10)
            return object.__new__(cls)
        else:
            raise TypeError()

    def __init__(self, question: str, answer: str):
        super().__init__(question, answer, 10)


class MAQ(BQS):  # Multiple Answer Question
    def __new__(cls, question: str, answer: str, alternatives: list):
        """
        Checks if the arguments are of the right type, if the answer is in the alternatives list, and calls the
        __new__ method from the superclass

        Args:
            question: The questions text
            answer: The answer to the question
            alternatives: A list of all alternatives, including the answer
        """
        if all([
            type(question) == str,
            type(answer) == str,
            type(alternatives) == list
        ]):
            if answer in alternatives:
                super().__new__(cls, 5, )
                return object.__new__(cls)
            else:
                raise ValueError()
        else:
            raise TypeError()

    def __init__(self, question: str, answer: str, alternatives: list):
        """
        Calls __init__ method from the superclass as well as creating a new parameter self._alternatives that is a
        shuffled dictionary of all alternatives with a corresponding key

        Args:
            question: The questions text
            answer: The answer to the question
            alternatives: A list of all alternatives, including the answer
        """
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

    def __eq__(self, answer: str) -> int:
        if answer.lower() == list(self._alternatives.keys())[
            list(map(lambda x: x.lower(), self._alternatives.values())).index(
                    self._answer)].lower() or answer.lower() == self._answer:
            return self._points
        else:
            return 0

    def __str__(self) -> str:
        return self[0] + "\n" + self[3]


class MaAQ(BQS):  # Mathematical Answer Question
    def __new__(cls, points: int) -> object:
        if points in [5, 10, 15]:
            super().__new__(cls, points, )
            return object.__new__(cls)
        else:
            raise ValueError

    def __init__(self, points: int):
        random_integers = [
            rand.randint(points - 4, points + 6),
            rand.randint(points - 4, points + 6)
        ]
        arithmetic_signs = ["+", "-", "*", "/"][rand.randint(0, 3)]
        if arithmetic_signs == "/":
            random_integers[0] = random_integers[0] * random_integers[1]
        _question = f"{random_integers[0]}{arithmetic_signs}{random_integers[1]}"
        _answer = str(round(eval(_question)))
        _points = points
        super().__init__(f"\nVad är:{_question}?\n", _answer, _points)
