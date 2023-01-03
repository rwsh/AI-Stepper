import random
import copy
import stepper as st

alpha = 0.1 # скорость обучения
gamma = 0.9 # ценность

N = 67 # количество шагов в партии
L = 1000 # количество циклов обучения

Qsa = {} # значения оценок действий

# создать текстовый ключ для состояние-действие 
def Key(s, a):
    key = "" # ключ - строка
    for i in s:
        key += i.__str__() +" " # преобразуем в строку
    for i in a:
        key += i.__str__() +" " # преобразуем в строку
    return key

# функция оценки действия a в состоянии s
def CalcQsa(s, a):
    key = Key(s, a)
    if key in Qsa:
        return Qsa[key] # если есть значение для действия a, то возвращаем
    else:
        return 0 # если действие a нам не известно, возвращаем 0

# выбрать eps-жадное действие для степпера
def ChoiseEps(Stepper, eps):
    Can = []
    Can0 = Stepper.Actions(0) # возможные действия нулевой ноги
    Can1 = Stepper.Actions(1) # возможные действия первой ноги

    s = Stepper.GetState() # сохраняем текущее состояние

    # объединяем возможные ходы, с указанием номера ноги
    for c in Can0:
        Can.append([0, c])
    for c in Can1:
        Can.append([1, c])

    p = random.random()
    if p < eps:
        # делаем произволный ход
        return copy.deepcopy(random.choice(Can)) # выбираем случайный элемент

    # ищем ход с максимальной оценкой в Qsa
    Max = CalcQsa(s, Can[0]) 
    MaxA = copy.deepcopy(Can[0])
    for a in Can:
        m = CalcQsa(s, a) # для каждого действия вычисляем значение
        if m > Max: # если текущее значение больше
            Max = m # сохраяем его
            MaxA = copy.deepcopy(a)
    
    return MaxA

# Запуск партии
def Run(eps):
    Stepper = st.TStepper() # создаем новый степпер

    S = Stepper.GetState() # сохраняем состояние
    A = ChoiseEps(Stepper, eps) # выбираем действие 

    for n in range(N):
        r = Stepper.Go(A) # реализуем действие и получаем подкрепление
        S_ = Stepper.GetState() # сохраняем состояние
        A_ = ChoiseEps(Stepper, eps) # выбираем действие 
        
        key = Key(S, A) # формируем ключ
        
        # обновляем функцию оценки действия
        Qsa[key] = CalcQsa(S, A) + alpha * (r + gamma * CalcQsa(S_, A_) - CalcQsa(S, A))

        S = copy.deepcopy(S_) # сохраняем полученное состояние
        A = copy.deepcopy(A_) # и выбранное действие
    return Stepper

