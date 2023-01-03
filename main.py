from turtle import speed
import pygame, random

import stepper as st
import rl

random.seed() # инициализировать ГСЧ

Width = 1400 # размеры окна игры
Height = 600
Color_BG = (232, 252, 249) # фон
Color_N1 = (255, 0, 0)
Color_N2 = (0, 0, 255)
Color_NN = (0, 0, 0)
Color_G = (255, 140, 0)

FPS = 10 # количество кадров в секунду
clock = pygame.time.Clock() # создаем часы

pygame.init() # запустить движок
win = pygame.display.set_mode((Width, Height)) # создаем окно

X = Width / 8
Y = Height / 2

L = 100 # ширина степпера
L2 = L / 2 # половина ширины
H = 40 # высота степпера
H2 = H / 2 # половина высоты
GH = 20 # толщина дорожки

# рисуем состояние степпера Hist
def DrawHist(Hist):
    Xs = X + Hist[0] * (L2) # положение нулевой ноги 1 = половина ширины степпера

    # рисуем нулевую ногу
    # определяем вертикальное положение
    if Hist[1] == 0:
        Ys = Y
    else:
        Ys = Y - H2 # половина высоты степпера 

    Leg0 = [(Xs - L2, Ys), (Xs + L2, Ys)] # опорные точки нулевой ноги
    pygame.draw.lines(win, Color_N1, False, [(Xs - L2, Ys + H), Leg0[0], Leg0[1], (Xs + L2, Ys + H)], 3)

    # рисуем первую ногу
    Sh = 0 # сдвиг первой ноги относительно нулевой ноги
    if Hist[2] == 1: 
        Sh = -1 # если нулевая нога вперед, то сдвиг первой ноги -1
    if Hist[2] == -1: 
        Sh = 1 # если нулевая нога назад, то сдвиг первой ноги 1
    if Hist[4] == 1:
        Sh = 1 # если первая нога вперед, то сдвиг первой ноги 1
    if Hist[4] == -1:
        Sh = -1 # если первая нога назад, то сдвиг первой ноги -1

    Sh *= L2 # масштабируем сдвиг

    # определяем вертикальное положение
    if Hist[3] == 0:
        Ys = Y
    else:
        Ys = Y - H2 # половина высоты степпера 

    Leg1 = [(Xs - L2 + Sh, Ys), (Xs + L2 + Sh, Ys)] # опорные точки первой ноги
    pygame.draw.lines(win, Color_N2, False, [(Xs - L2 + Sh, Ys + H), Leg1[0], Leg1[1], (Xs + L2 + Sh, Ys + H)], 3)

    # рисуем спинку
    pygame.draw.lines(win, Color_NN, False, [Leg0[0], Leg1[0]], 3)
    pygame.draw.lines(win, Color_NN, False, [Leg0[1], Leg1[1]], 3)

# запускаем обучение 
for l in range(rl.L):
    rl.Run(0.1)

Stepper = rl.Run(0) # запускаем обученного степпера

print(Stepper.X) # печатаем пройденное расстояние

# мультипликация 
for c in Stepper.History:
    win.fill(Color_BG) # рисуем фон
    pygame.draw.line(win, Color_G, (0, Y + H + GH/2), (Width, Y + H + GH/2), GH) # рисуем дорожку

    DrawHist(c) # рисуем состояние степпера

    pygame.display.flip() # обновляем экран
    clock.tick(FPS) # задержка по времени

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # если произошло событие QUIT
            pygame.quit() # закрываем pygame
            Running = False # выходим из цикла

# запускаем пустой цикл pygame, чтобы сохранить изображение
Running = True
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # если произошло событие QUIT
            pygame.quit() # закрываем pygame
            Running = False # выходим из цикла

