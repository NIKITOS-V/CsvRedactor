import csv
import os


class FileParser:
    def __init__(self):
        self.Dir = f"{os.path.abspath(os.curdir)}\\Data"

        self.FileCommandsDict = {
            'print': [self.PrintFile, 2,
                     {'Description': 'Выводит данные файла в консоль',
                      'Required parameters': 'Имя файла'}
                     ],
            'create': [self.CreateFile, 2,
                       {'Description': 'Создаёт файл в установленной директории',
                        'Required parameters': 'Имя файла'}
                       ],
            'remove': [self.RemoveFile, 2,
                       {'Description': 'Удаляет файл',
                        'Required parameters': 'Имя файла'}
                       ]
        }

        self.ConsoleCommandsDict = {
            'exit': [self.Exit, 1, {'Description': 'Выводит данные файла в консоль'}],
            'clear': [self.Clear, 1, {'Description': 'Очищает консоль'}],
            'commands': [self.PrintCommandsList, 1, {'Description': 'Выводит список всех команд'}],
            'dir': [self.PrintFilesIntoDirectory, 1, {'Description': 'Выводит список файлов в текущей директории'}],
            'path': [self.PrintPathToDirectory, 1, {'Description': 'Выводит полный путь к текущей директории'}],
            'change_dir': [self.ChangeDirectory, 2,
                           {'Description': 'Меняет директорию для работы',
                            'Required parameters': 'Полный путь до директории',
                            }
                           ],
            'create_dir': [self.MakeDirectory, 2,
                           {'Description': 'Создаёт директорию',
                            'Required parameters': 'Полный путь до директории'}
                           ],
            'remove_dir': [self.RemoveDirectory, 1,
                           {'Description': 'Удаляет директорию текущую',
                            'initial value': self.Dir}
                           ],
            'clear_dir': [self.ClearDirectory, 1, {'Description': 'Очищает директорию'}]
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
                if UserInput[0] in self.ConsoleCommandsDict.keys():
                    Parameters = self.ConsoleCommandsDict[UserInput[0]]

                    if Parameters[1] == 1:
                        Parameters[0]()

                    else:
                        if LenUserInput < Parameters[1]:
                            self.ConsoleError("There is too little input data")

                        elif LenUserInput == Parameters[1]:
                            Parameters[0](UserInput[1])

                        else:
                            self.ConsoleError("There is too many input data")

                else:

                    if UserInput[0] in self.FileCommandsDict.keys():
                        Parameters = self.FileCommandsDict[UserInput[0]]

                        if LenUserInput < Parameters[1]:
                            self.ConsoleError("There is too little input data")

                        elif LenUserInput == Parameters[1]:
                            FileName = UserInput[1].split('.')

                            if len(FileName) == 2 and FileName[1] == 'csv':

                                self.FileName = self.CreatePath(UserInput[1])

                                Parameters[0]()


                            else:
                                self.ConsoleError("Unknown file format")

                        else:
                            self.ConsoleError("There is too many input data")

                    else:
                        self.ConsoleError("Unknown command")

    def PrintFile(self):
        Output = ''

        for Count, List in enumerate(self.ReadFile(1)):
            for Value in List:
                Output += f"{Value:20}"

            print(f"\n\t{Count} {Output}")

            Output = ''

    def ReadFile(self, TypeOfReading):
        if os.path.exists(self.FileName):
            with open(self.FileName, 'r', encoding='utf-8') as Data:
                ReadData = csv.DictReader(Data)

                if TypeOfReading == 0:
                    Header = list(ReadData.fieldnames)
                    DataList = list(ReadData)
                    DataList.insert(0, Header)

                elif TypeOfReading == 1:
                    DataList = list(map(lambda Dict: list(Dict.values()), list(ReadData)))
                    DataList.insert(0, list(ReadData.fieldnames))

                return DataList
        else:
            self.ConsoleError("The file was not found")

    def AppToFile(self):
        if os.path.exists(self.FileName):
            Data = self.ReadFile(0)
            NumberRows = len(Data)

            StartAppend = 'Y'

            while StartAppend == 'Y':
                while True:
                    StartAppend = input(f"\n\t")



        else:
            self.ConsoleError("The file was not found")

    def CreateFile(self):
        Header = input("\n\tHeader: ").split(',')

        with open(self.FileName, 'w', encoding='utf-8', newline='') as Data:
            csv.DictWriter(Data, fieldnames=list(map(lambda str: ' '.join(str.split()), Header))).writeheader()

    def RemoveFile(self):
        if os.path.exists(self.FileName):
            os.remove(f"{self.FileName}")
        else:
            self.ConsoleError("The file was not found")

    def ConsoleError(self, Message):
        print(f"\n\tCONSOLE ERROR: {Message}")

    def CreatePath(self, FileName):
        return f"{self.Dir}\\{FileName}"

    def ChangeDirectory(self, NewDir):
        if os.path.exists(NewDir):
            self.Dir = NewDir
        else:
            self.ConsoleError("The directory was not found")

    def PrintPathToDirectory(self):
        print(f"\n\t{self.Dir}")

    def PrintFilesIntoDirectory(self):
        for FileName in os.listdir(self.Dir):
            print(f"\n\t{FileName}")

    def MakeDirectory(self, NewDir):
        os.mkdir(NewDir)

    def RemoveDirectory(self, Dir):
        os.rmdir(f"{Dir}")

    def ClearDirectory(self):
        FilesList = os.listdir(self.Dir)

        print("\n\tFiles in the directory:")

        for FileName in FilesList:
            print(f"\n\t\t{FileName}")

        while True:
            UserInput = input(f"\n\tAre you sure? Y / n: ")

            if UserInput == 'Y':
                for FileName in FilesList:
                    os.remove(f"{self.Dir}\\{FileName}")
                break

            elif UserInput == 'n':
                break

    def PrintCommandsList(self):
        for Command in self.FileCommandsDict.keys():
            print(f"\n\t{Command}:")

            Parameters = self.FileCommandsDict[Command][2]

            for Description in Parameters.keys():
                print(f"\t\t{Description}: {Parameters[Description]}")

        for Command in self.ConsoleCommandsDict.keys():
            print(f"\n\t{Command}:")

            Parameters = self.ConsoleCommandsDict[Command][2]

            for Description in Parameters.keys():
                print(f"\t\t{Description}: {Parameters[Description]}")

    def Exit(self):
        self.RunConsole = 0

    def Clear(self):
        os.system('cls')


if __name__ == "__main__":
    FileParser().MainLoop()
