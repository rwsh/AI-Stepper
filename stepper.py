import random

Actions = ("up", "down", "left", "right") # возможные перемещения ноги

# класс описание ноги
class TLeg: 
    def __init__(self):
        self.H = 0 # высота ноги: 0 - нога на земле, 1 - поднята
        self.S = 0 # сдвиг ноги: 0 - нет сдвига, 1 - сдвиг вправо, -1 сдвиг влево
    def __str__(self):
        return self.H.__str__() + " : " + self.S.__str__()

# класс степпера
class TStepper:
    def __init__(self):
        self.History = [] # история состояний
        self.X = 0 # положение степпера
        self.Legs = [TLeg(), TLeg()] # создаем ноги
        self.History.append([self.X, self.Legs[0].H, self.Legs[0].S, self.Legs[1].H, self.Legs[1].S])

    # получение списка возможных ходов для ноги n \in {0, 1}
    def Actions(self, n):
        Res = []
        n_ = (n + 1) % 2 # вычислить номер другой ноги
        if self.Legs[n_].H == 1: # если другая нога поднята, то для этой ноги нет возможных ходов
            return Res

        if self.Legs[n].H == 0: # если нога стоит на земле
            return [0] # в этом случае возможен только ход "up"

        Res.append(1) # если нога поднята, то всегда возможен ход "down"

        if self.Legs[n].S == 0:
            Res.append(2) # ход "left"
            Res.append(3) # ход "right"
        if self.Legs[n].S == 1:
            Res.append(2) # ход "left"
        if self.Legs[n].S == -1:
            Res.append(3) # ход "right"

        return Res
    
    # произвести действие Action = [n, a], где a - номер ноги, a - действие
    def Go(self, Action):
        R = -1 # подкрепление -1 если не продвинемся

        Can = self.Actions(Action[0]) # получаем возможные ходы для указанной ноги
        if Action[1] not in Can: # если предложенный ход невозможен, то ошибка
            print("Error!")
            return

        if Action[1] == 0: # если действие "up"
            self.Legs[Action[0]].H = 1 # тогда поднимаем ногу
        if Action[1] == 1: # если действие "down"
            self.Legs[Action[0]].H = 0 # тогда опускаем ногу
        if Action[1] == 2: # если действие "left"
            self.Legs[Action[0]].S -= 1 # тогда ногу влево
            n_ = (Action[0] + 1) % 2 # вычислить номер другой ноги
            self.Legs[n_].S += 1 # изменить состояние другой ноги в противополжную строну

            if Action[0] == 0: # если это нулевая нога, то изменяем положение
                self.X -= 1 # считаем, что степпер ушел левее
                R = -10 # уменьшаем подкрепление, поскольку уходим от цели
        if Action[1] == 3: # если действие "right"
            self.Legs[Action[0]].S += 1 # тогда ногу вправо
            n_ = (Action[0] + 1) % 2 # вычислить номер другой ноги
            self.Legs[n_].S -= 1 # изменить состояние другой ноги в противополжную строну

            if Action[0] == 0: # если это нулевая нога, то изменяем положение
                self.X += 1 # считаем, что степпер ушел правее
                R = 10 # устанавливаем положительное подкрепление 
        # сохраним в истории состояние
        self.History.append([self.X, self.Legs[0].H, self.Legs[0].S, self.Legs[1].H, self.Legs[1].S])
        return R # возвращаем подкрепление

    # исполнить последовательность команд
    def GoPath(self, Path):
        for p in Path:
            self.Go(p)

    # вернуть текущее состояние
    def GetState(self):
        # состояние = только положения ног
        return [self.Legs[0].H, self.Legs[0].S, self.Legs[1].H, self.Legs[1].S]

'''
Stepper = TStepper() # создать степпера

Path = [] # последовательность команд для степпера
Path.append([0, 0])
Path.append([0, 3])
Path.append([0, 1])
Path.append([1, 0])
Path.append([1, 3])
Path.append([1, 1])

Stepper.GoPath(Path) # выполняем заданную последовательность команд

print(Stepper.X) # печатаем пройденное расстояние

'''
