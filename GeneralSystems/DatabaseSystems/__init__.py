import inspect
import shutil
from pathlib import Path
from abc import *


# Decorators to DBMS classes
def ReDe(func):  # Read Decorator
    def func_wrapper(self, *args):
        if type(self._file) == str:
            self._file = open(self._file, "r")
        return func(self, *args)

    return func_wrapper


def ApDe(func):  # Append Decorator
    def func_wrapper(self, *args):
        if type(self._file) == str:
            self._file = open(self._file, "a")
        return func(self, *args)

    return func_wrapper


def WiDe(func):  # Write Decorator
    def func_wrapper(self, *args):
        if type(self._file) == str:
            self._file = open(self._file, "w")
        return func(self, *args)

    return func_wrapper


class DBMS(ABC):  # Database Management System (WIP)
    @abstractmethod
    def __new__(cls, *args):
        if Path(str(args[0])).is_file():
            return object.__new__(cls)
        else:
            raise FileNotFoundError

    def __init__(self, file: str):
        self._file = file

    def __neg__(self):
        self._file.close()
        self._file = self._file.name

    # @ReDe
    def __iter__(self):
        return self

    def __next__(self):
        if type(self._file) == str:
            self._file = open(self._file, "r")
        if "dict" in inspect.stack()[1].code_context[0]:
            line = [self._file.readline(), self._file.readline()]
        else:
            line = self._file.readline()
        if not any(line):
            -self
            raise StopIteration
        else:
            return line

    @ReDe
    def __contains__(self, name):
        ret = name in self._file.read()
        -self
        return ret

    @ReDe
    def __str__(self):
        ret = str(self._file.read())
        -self
        return ret

    @ReDe
    def __len__(self):
        ret = len(self._file.readlines())
        -self
        return ret

    def backup(self):
        last_BkUp = 1
        while Path(f"BkUp{last_BkUp}_{self._file}").is_file():
            last_BkUp += 1
        shutil.copy2(self._file, f"BkUp{last_BkUp}_{self._file}")

    @WiDe
    def _replace_writing(self, new_string):
        self._file.write("".join(new_string))
        -self

    def replace(self,
                old_string: str,
                new_string: str,
                join="",
                filterNaN=False,
                backup=False):
        if backup:
            self.backup()
        new_string = [n.replace(old_string, new_string) for n in self]
        if filterNaN:
            new_string = list(filter(None, new_string))
        new_string = f"{join}".join(new_string)
        return self._replace_writing(new_string)

    @ApDe
    def dbappend(self, *args):
        for arg in args:
            self._file.write("\n" + str(arg) + "\n")


class mQDB(DBMS):  # Multiple Question Database (WIP)
    def __new__(cls, *args):
        if args[0] == "QuizQAalternativ.txt":
            try:
                open(args[0])
                return object.__new__(cls)
            except:
                raise TypeError
        else:
            raise NameError

    def __init__(self, file: str):
        super().__init__(file)

    @ReDe
    def __next__(self):
        line = [
            self._file.readline(), [self._file.readline() for n in range(3)]
        ]
        if not any([item for sublist in line for item in sublist]):
            -self
            raise StopIteration
        else:
            return line


class sQDB(DBMS):  # Single Question Database (WIP)
    def __new__(cls, *args):
        if args[0] == "QuizQA.txt":
            try:
                open(args[0])
                return object.__new__(cls)
            except:
                raise TypeError
        else:
            raise NameError

    def __init__(self, file: str):
        super().__init__(file)
