import csv
import os


class FileParser:
    TB = '\t'
    NL = '\n'
    Dir = f"{os.path.abspath(os.curdir)}\\Data"

    def __init__(self):
        self.FileCommandsDict = {
            'read': [self.ReadFile, 2],
            'create': [self.CreateFile, 2],
            'remove': [self.RemoveFile, 2]
        }

        self.ConsoleCommandDict = {
            'exit': [self.Exit, 1],
            'clear': [self.Clear, 1],
            'cd': [self.ChangeDirectory, 2],
            'md': [self.MakeDirectory, 2],
            'rd': [self.RemoveDirectory, 2]
        }

        self.RunConsole = 1

        self.FileName = None

    def MainLoop(self):
        while self.RunConsole:
            UserInput = input("\nCONSOLE: ").split()

            LenUserInput = len(UserInput)

            if LenUserInput == 0:
                self.ConsoleError("The console cannot be empty")

            else:
                try:
                    Parameters = self.ConsoleCommandDict[UserInput[0]]

                    if Parameters[1] == 1:
                        Parameters[0]()

                    else:
                        if LenUserInput < Parameters[1]:
                            self.ConsoleError("There is too little input data")

                        elif LenUserInput == Parameters[1]:
                                Parameters[0](UserInput[1])

                        else:
                            self.ConsoleError("There is too many input data")

                except KeyError:

                    Parameters = self.FileCommandsDict[UserInput[0]]

                    if LenUserInput < Parameters[1]:
                        self.ConsoleError("There is too little input data")

                    elif LenUserInput == Parameters[1]:
                        FileName = UserInput[1].split('.')

                        if len(FileName) == 2 and FileName[1] == 'csv':

                            self.FileName = self.CreatePath(UserInput[1])

                            try:
                                Parameters[0]()

                            except KeyError:
                                self.ConsoleError("Unknown command")
                        else:
                            self.ConsoleError("Unknown file format")

                    else:
                        self.ConsoleError("There is too many input data")

    def ReadFile(self):
        if os.path.exists(self.FileName):
            with open(self.FileName, 'r', encoding='utf-8') as Data:
                for Dict in list(csv.DictReader(Data)):
                    print(Dict)
        else:
            self.ConsoleError("The file was not found")

    def SystemReadFile(self):
        with open(self.FileName, 'r', encoding='utf-8') as Data:
            return list(csv.DictReader(Data))

    def CreateFile(self):
        Header = input("\n\tHeader: ").split(',')

        with open(self.FileName, 'w', encoding='utf-8', newline='') as Data:
            csv.DictWriter(Data, fieldnames=list(map(
                lambda str: str[:-1] if str[-1] == ' ' else (str[1:] if str[0] == ' ' else str), Header))).writeheader()

    def RemoveFile(self):
        if os.path.exists(self.FileName):
            os.remove(f"{self.FileName}")
        else:
            self.ConsoleError("The file was not found")

    def ConsoleError(self, Message):
        print(f"{self.NL}{self.TB}CONSOLE ERROR: {Message}")

    def CreatePath(self, FileName):
        return f"{self.Dir}\\{FileName}"

    def ChangeDirectory(self, NewDir):
        if os.path.exists(NewDir):
            self.Dir = NewDir
        else:
            self.ConsoleError("The directory was not found")

    def MakeDirectory(self, NewDir):
        os.mkdir(NewDir)

    def RemoveDirectory(self, Dir):
        os.rmdir(f"{Dir}")

    def Exit(self):
        self.RunConsole = 0

    def Clear(self):
        os.system('cls')


if __name__ == "__main__":
    FileParser().MainLoop()
