# Quizspel_PRR2 - Rapport
Programförklaring
## Innehåll
1. Genomgång av klasser
   1. BQS
   2. DBSM
   3. Player
   4. Turn
2. Klassers relation till varrandra 
   1. UML
3. Inkapsling
4. Polymorfism
5. Problem
6. Utvärdering


# Genomgång av klasser

### BQS - Basic Question System
I klassen BQS finns attributen _question, _answer och _points. Valet av attribut kommer ifrån vikten att separera frågan och svaret, samt attributet _points finns så andra klasser som ärver av BQS kan erhålla olika mycket poäng per rätt svar. Därför grundas alla metoderna i attributen och inte för vilken typ av fråga klassen grundar sig i.
<br>
Ex.
```
    def __int__(self):
        return self._points

    def __eq__(self, answer):
        if self._answer == answer.lower():
            return self._points
        else:
            return 0
```
<br>
Då BQS också är en standardklass, som andra klasser skall ärva från, ville jag också ha ett system för att urskillja alla objekt skapade av underklasser. Detta systemet blev två dictionaries varav en sorterade objekten utefter poäng och den andra utefter typen av fråga. Namnen för dessa dictionaries är:

1. _QuestionType_Dictionary
2. _QuestionValue_Dictionary

Då jag ville hålla BQS-klassen öppen för andra typer av underklasser än de angivna i uppgiften skapade jag ett system som kollade om underklassen fanns i _QuestionType_Dictionary samt om antalet poäng fanns i _QuestionValue_Dictionary. Om det saknades skulle en ny lista skapas med nyckeln av antigen poäng-värdet eller namnet på underklassen. Allt detta sker innan objektet är instansierat så inga objekt kan instansieras utan en index till båda dictionariesana.

```
class BQS(ABC):
    _QuestionType_Dictionary = {}
    _QuestionValue_Dictionary = {}

    @abstractmethod
    def __new__(cls, points: int):
        if cls.__name__ not in cls._QuestionType_Dictionary.keys():
            cls._QuestionType_Dictionary[cls.__name__] = []
        if points not in cls._QuestionValue_Dictionary.keys():
            cls._QuestionValue_Dictionary[points] = []
        return object.__new__(cls)
```
Alla objekt- och klass attribut är privata då metoderna och underklasserna skall hantera dem. Därefter får användaren kalla på dessa attribut via de olika metoderna. Därav "_" framför attributen.
Däremot ville jag ha ett system för att kalla på attributen och därav dundermetoden `__getitem__`.
```
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
```
Detta metod upplägget är använt av samtliga klasser i projektet. Relationen mellan de skapade underklasserna och överklassen, BQS, kan ses via det här UML-diagrammet.
![](/Users/carlsjoback/Desktop/Quizspel-PRR2/QuestionSystems.png)
<br> 
#### SAQ - Singel Answer Question
Single answer question är en underklass av BQS, vars uppgift är att hålla koll på frågor med ett svar. 
Den enda skillnaden mellan SAQ och BQS är att SAQ har en modifierad `__new__` metod.
```
    def __new__(cls, question, answer):
        if all([type(n) == str for n in [question, answer]]):
            super().__new__(cls, 10)
            return object.__new__(cls)
        else:
            raise TypeError()
            
    def __init__(self, question: str, answer: str):
        super().__init__(question, answer, 10)
```
Förändringen försäkrar så att objektet inte kan instansieras om något av parametrarna inte existerar samt om båda inte är av typen str. 
Observera att överklassen, BQS, egna `__new__` kallas för att potentiellt skapa nycklar till _QuestionType_Dictionary och _QuestionValue_Dictionary.
Därefter kallas överklassens `__init__` metod.
#### MAQ - Multiple Answer Question
#### MaAQ - Mathematics Answer Question

### BDMS - Database Management System (WIP)
#### mQDB - Multiple Question Database
#### sQDB - Single Question Database

### Player

### Turn

 - Förklara dina val när hur du implementerat dina klasser tex kring metoder och attribut
 - Förklara hur du tänkt kring relationerna mellan klasserna eller interface
 - Förklara hur du har tänkt angående inkapsling
 - Vilka fel har du stött på och hur har du åtgärdat dom
 - En utvärdering av programmet
 - Förklara hur du har tänkt angående koppling mellan klasser
 - Förklara hur du tänkt kring polymorfism
 - Användning av datavetenskapligt språk
