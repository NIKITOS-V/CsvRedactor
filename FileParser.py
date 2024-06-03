import csv
import os
from copy import deepcopy


class FileParser:
    SupportedExtension = 'csv'
    Yes = 'Y'
    Not = 'n'

    def __init__(self):
        self.CommandsDict = {
            'print': [self.PrintFile, 2,
                      {'Description': 'Выводит данные файла в консоль',
                       'Required parameters': 'Имя файла'}
                      ],
            'create': [self.CreateFile, 2,
                       {'Description': 'Создаёт файл в установленной директории',
                        'Required parameters': 'Имя файла'}
                       ],
            'append': [self.AppendToFile, 2,
                       {'Description': 'Добавляет информацию в файл',
                        'Required parameters': 'Имя файла'}
                       ],
            'change': [self.ChangeFile, 2,
                       {'Description': 'Меняет информацию в рядах',
                        'Required parameters': 'Имя файла'}
                       ],
            'del': [self.RemoveFile, 2,
                    {'Description': 'Удаляет файл',
                     'Required parameters': 'Имя файла'}
                    ],
            'exit': [self.Exit, 1, {'Description': 'Выводит данные файла в консоль'}],
            'clear': [self.Clear, 1, {'Description': 'Очищает консоль'}],
            'commands': [self.PrintCommandsList, 1, {'Description': 'Выводит список всех команд'}],
            'dir': [self.PrintFilesIntoDirectory, 1, {'Description': 'Выводит список файлов в текущей директории'}],
            'path': [self.PrintPathToDirectory, 1, {'Description': 'Выводит полный путь к текущей директории'}],
            'cd': [self.ChangeDirectory, 2,
                   {'Description': 'Меняет директорию для работы',
                    'Required parameters': 'Полный путь до директории',
                    }
                   ],
            'mkdir': [self.MakeDirectory, 2,
                      {'Description': 'Создаёт директорию',
                       'Required parameters': 'Полный путь до директории'}
                      ],
            'rmdir': [self.RemoveDirectory, 1, {'Description': 'Удаляет текущую директорию'}],
            'clrdir': [self.ClearDirectory, 1, {'Description': 'Очищает директорию'}]
        }
        self.RunConsole = 1

        self.Dir = f"{os.path.abspath(os.curdir)}\\Data"

        self.FileName = None

    def MainLoop(self):
        while self.RunConsole:
            UserInput = input("\nCONSOLE: ").split()

            LenUserInput = len(UserInput)

            if LenUserInput == 0:
                self.ConsoleError("The console cannot be empty")

            else:
                if UserInput[0] in self.CommandsDict.keys():
                    Manual = self.CommandsDict[UserInput[0]]

                    if LenUserInput == Manual[1]:
                        Manual[0](UserInput)

                    elif LenUserInput < Manual[1]:
                        self.ConsoleError("There is too little input data")

                    else:
                        self.ConsoleError("There is too many input data")

                else:
                    self.ConsoleError("Unknown command")

    def PrintFile(self, UserInput):
        Output = ''
        Path = self.CreatePath(UserInput[1])

        if self.ExpansionIsCorrect(Path):
            if self.PathIsCorrect(Path):
                for Count, List in enumerate(self.ReadFile(Path, 1)):
                    for Value in List:
                        Output += f"{Value:20}"

                    print(f"\n\t{Count + 1} {Output}")

                    Output = ''

    def ReadFile(self, Path, TypeOfReading):
        with open(Path, 'r', encoding='utf-8') as Data:
            try:
                ReadData = csv.DictReader(Data)

                if TypeOfReading == 0:
                    return list(ReadData), list(ReadData.fieldnames)

                elif TypeOfReading == 1:
                    DataList = list(map(lambda Dict: list(Dict.values()), list(ReadData)))
                    DataList.insert(0, list(ReadData.fieldnames))

                    return DataList

            except TypeError:
                self.ConsoleError("File without header")

    def AppendToFile(self, UserInput):
        Path = self.CreatePath(UserInput[1])

        if self.ExpansionIsCorrect(UserInput[1]):
            if self.PathIsCorrect(Path):
                OldData, Head = self.ReadFile(Path, 0)
                NewData = deepcopy(OldData)

                Row = len(OldData) + 1

                try:
                    Data = open(Path, 'w', encoding='utf-8', newline='')

                    while True:
                        ContinueAppend = input(f"\n\tContinue? {self.Yes} / {self.Not}: ")

                        if ContinueAppend == self.Yes:
                            Dict = {Colum: '' for Colum in Head}

                            print(f"\n\tRow: {Row}\n")

                            for Colum in Head:
                                Dict[Colum] = input(f"\t\t{Colum}: ")

                            NewData.append(Dict)
                            Row += 1

                        elif ContinueAppend == self.Not:
                            ReadData = csv.DictWriter(Data, fieldnames=Head)
                            ReadData.writeheader()
                            ReadData.writerows(OldData)
                            Data.close()
                            break

                except Exception:
                    with open(Path, 'w', encoding='utf-8', newline='') as Data:
                        Data = csv.DictWriter(Data, fieldnames=Head)
                        Data.writeheader()
                        Data.writerows(OldData)

    def ChangeFile(self, UserInput):
        Path = self.CreatePath(UserInput[1])

        if self.ExpansionIsCorrect(UserInput[1]):
            if self.PathIsCorrect(Path):
                OldData, OldHead = self.ReadFile(Path, 0)
                NewData, NewHead = deepcopy(OldData), deepcopy(OldHead)
                MaxRow = len(OldData) + 1

                try:
                    Data = open(Path, 'w', encoding='utf-8', newline='')

                    while True:
                        ContinueAppend = input(f"\n\tContinue? {self.Yes} / {self.Not}: ")

                        if ContinueAppend == self.Yes:
                            Row = input("\n\tRow number: ")
                            print()

                            try:
                                Row = int(Row)

                                if Row == 1:
                                    for Index, Colum in enumerate(NewHead):
                                        NewHead[Index] = input(f"\t\tRename '{Colum}': ")

                                    NewData = list(map(
                                        lambda Dict: {Key: Value for Key, Value in zip(NewHead, Dict.values())},
                                        OldData))

                                elif 1 < Row < MaxRow:
                                    for Colum in NewHead:
                                        NewData[Row - 2][Colum] = input(f"\t\t{Colum}: ")
                                else:
                                    self.ConsoleError("The row does not exist")

                            except ValueError:
                                self.ConsoleError("The row must have an int value")

                        elif ContinueAppend == self.Not:
                            ReadData = csv.DictWriter(Data, fieldnames=NewHead)
                            ReadData.writeheader()
                            ReadData.writerows(NewData)
                            Data.close()
                            break

                except Exception:
                    with open(Path, 'w', encoding='utf-8', newline='') as Data:
                        Data = csv.DictWriter(Data, fieldnames=OldHead)
                        Data.writeheader()
                        Data.writerows(OldData)

    def CreateFile(self, UserInput, Separate='\n\t'):
        Header = input(f"{Separate}Header: ").split(',')

        with open(self.CreatePath(UserInput[1]), 'w', encoding='utf-8', newline='') as Data:
            csv.DictWriter(Data, fieldnames=list(map(lambda Str: Str.strip(), Header))).writeheader()

        print("\n\tSuccessfully!")

    def RemoveFile(self, UserInput):
        Path = self.CreatePath(UserInput[1])

        if self.PathIsCorrect(Path):
            os.remove(Path)
        else:
            self.ConsoleError("The file was not found")

    def ConsoleError(self, Message, Separate='\n\t'):
        print(f"{Separate}CONSOLE ERROR: {Message}")

    def CreatePath(self, FileName):
        return f"{self.Dir}\\{FileName}"

    def PathIsCorrect(self, Path, PrintError=0):
        if os.path.exists(Path):
            return 1

        if PrintError:
            self.ConsoleError("Not found")

        return 0

    def ExpansionIsCorrect(self, FileName, PrintError=1):
        if FileName[FileName.rfind('.') + 1:] == self.SupportedExtension:
            return 1

        if PrintError:
            self.ConsoleError('The extension is incorrect')

        return 0

    def ChangeDirectory(self, UserInput):
        if self.PathIsCorrect(UserInput[1]):
            self.Dir = UserInput[1]

            print("\n\tSuccessfully!")

    def PrintPathToDirectory(self, *args, Separate='\n\t'):
        print(f"{Separate}{self.Dir}")

    def PrintFilesIntoDirectory(self, *args, Separate='\n\t'):
        for FileName in os.listdir(self.Dir):
            print(f"{Separate}{FileName}")

    def MakeDirectory(self, UserInput):
        if self.PathIsCorrect(UserInput[1][:UserInput[1].rfind("\\")]):
            try:
                os.mkdir(UserInput[1])

                print("\n\tSuccessfully!")

            except FileExistsError:
                self.ConsoleError("Failed to execute")

    def RemoveDirectory(self, *args):
        try:
            os.rmdir(self.Dir)

            print("\n\tSuccessfully!")

        except FileExistsError:
            self.ConsoleError("Failed to execute")

    def ClearDirectory(self, *args):
        print("\n\tFiles in the directory:")

        self.PrintFilesIntoDirectory(Separate='\n\t\t')

        while True:
            UserInput = input(f"\n\tAre you sure? {self.Yes} / {self.Not}: ")

            if UserInput == self.Yes:
                for FileName in os.listdir(self.Dir):
                    os.remove(self.CreatePath(FileName))

                print("\n\tSuccessfully!")

                break

            elif UserInput == self.Not:

                print("\n\tThe operation was canceled")
                break

    def PrintCommandsList(self, *args):
        for Command in self.CommandsDict.keys():
            print(f"\n\t{Command}:")

            Parameters = self.CommandsDict[Command][2]

            for Description in Parameters.keys():
                print(f"\t\t{Description}: {Parameters[Description]}")

    def Exit(self, *args):
        self.RunConsole = 0

    def Clear(self, *args):
        os.system('cls')


if __name__ == "__main__":
    FileParser().MainLoop()
