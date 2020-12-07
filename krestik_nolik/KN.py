import pygame 
import sys #чтобы выйти из Python
from pygame.locals import * # для многих фишек pygame
import time # для метода time.sleep()

#Инициализация глобальных переменных
XO = 'x'
win = None
draw = False
width = 400
height = 400
white = (255, 255, 255)
line_color = (10,10,10)

#делаем доску
BRD = [[None]*3,[None]*3,[None]*3]

#инициализируем окно
pygame.init()
fps = 60
CLOCK = pygame.time.Clock()#создаем обьект который поможет отслеживать время
screen = pygame.display.set_mode((width, height+100),0,32)#резервируем 100 пиксельное пр-во для отображения статуса игры
pygame.display.set_caption("Krestiki-Noliki")# название в верхней части 

#загружаем картинки
opening = pygame.image.load('KN_opening.png')
x_img = pygame.image.load('x.png')
o_img = pygame.image.load('o.png')

#делаем все под один размер крч
x_img = pygame.transform.scale(x_img, (80,80))
o_img = pygame.transform.scale(o_img, (80,80))
opening = pygame.transform.scale(opening, (width, height+100))

# функция запускает игру
def game_opening():
    screen.blit(opening,(0,0))
    #обновляет изображение
    pygame.display.update()
    time.sleep(1)
    screen.fill(white)

    # рисуем вертикальные палочки
    pygame.draw.line(screen,line_color,(width/3,0),(width/3, height),7)
    pygame.draw.line(screen,line_color,(width/3*2,0),(width/3*2, height),7)
    # рисуем горизонтальные палочки
    pygame.draw.line(screen,line_color,(0,height/3),(width, height/3),7)
    pygame.draw.line(screen,line_color,(0,height/3*2),(width, height/3*2),7)
    draw_status()

# черный прямоугольник внизу отображающий статус игры
def draw_status():

    global draw

    if win is None:
        message = XO.upper() + "   ход"
    else:
        message = "Игрок "+ win.upper() +", Победа! Вместо обеда!"
    if draw:
        message = 'Ничья Другалек!'

    font = pygame.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))

    # копируем сообщение на доску
    screen.fill ((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width/2, 500-50))
    screen.blit(text, text_rect)
    pygame.display.update()

#функция которая проверяет выйгрыш    
def check_win():

    global BRD, win, draw

    # чекаем выйгрышные строки
    for row in range (0,3):
        if ((BRD [row][0] == BRD[row][1] == BRD[row][2]) and(BRD [row][0] is not None)):
            # строка выйграла
            win = BRD[row][0]
            #рисуем линию выйгрыша
            pygame.draw.line(screen, (250,0,0), (0, (row + 1)*height/3 -height/6),\
                              (width, (row + 1)*height/3 - height/6 ), 4)
            break

    # чекаем выйгрышные столбцы
    for col in range (0, 3):
        if (BRD[0][col] == BRD[1][col] == BRD[2][col]) and (BRD[0][col] is not None):
            # столбец выйграл
            win = BRD[0][col]
            pygame.draw.line (screen, (250,0,0),((col + 1)* width/3 - width/6, 0),\
                          ((col + 1)* width/3 - width/6, height), 4)
            break

    # чекаем победу по диагонали
    if (BRD[0][0] == BRD[1][1] == BRD[2][2]) and (BRD[0][0] is not None):
        # \
        win = BRD[0][0]
        pygame.draw.line (screen, (250,70,70), (50, 50), (350, 350), 4)

    if (BRD[0][2] == BRD[1][1] == BRD[2][0]) and (BRD[0][2] is not None):
        # /
        win = BRD[0][2]
        pygame.draw.line (screen, (250,70,70), (350, 50), (50, 350), 4)

    if(all([all(row) for row in BRD]) and win is None ):
        draw = True

    draw_status()

#функция рисует X и O там где щелкает мышка 
def drawXO(row,col):
    global BRD,XO

    if row==1:
        posx = 30
    if row==2:
        posx = width/3 + 30
    if row==3:
        posx = width/3*2 + 30

    if col==1:
        posy = 30
    if col==2:
        posy = height/3 + 30
    if col==3:
        posy = height/3*2 + 30

    BRD[row-1][col-1] = XO
    if(XO == 'x'):
        screen.blit(x_img,(posy,posx))
        XO= 'o'
    else:
        screen.blit(o_img,(posy,posx))
        XO= 'x'

    pygame.display.update()

#функция запускается от клика берет координаты и если место не занято рисует там X или O   
def userClick():
    #берет координаты клика мышью
    x,y = pygame.mouse.get_pos()

    #получает столбец клика мыши
    if(x<width/3):
        col = 1
    elif (x<width/3*2):
        col = 2
    elif(x<width):
        col = 3
    else:
        col = None

    #получает строку клика мыши
    if(y<height/3):
        row = 1
    elif (y<height/3*2):
        row = 2
    elif(y<height):
        row = 3
    else:
        row = None

    if(row and col and BRD[row-1][col-1] is None):
        global XO

        #рисует X или O на экране
        drawXO(row,col)
        check_win()

#перезапускает игру и сбрасывает переменные        
def reset_game():
    global BRD, win,XO, draw

    time.sleep(3)
    XO = 'x'
    draw = False
    game_opening()
    win=None
    BRD = [[None]*3,[None]*3,[None]*3]

#чтобы начать игру мы вызываем эту функцию
game_opening()

#запускаем бесконечный цикл
while(True):

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type is MOUSEBUTTONDOWN:
            #запускаем функцию нажатия мышки
            userClick()
            #если есть победитель или ничья вызываем перезапуск
            if(win or draw):
                reset_game()

    pygame.display.update()

    CLOCK.tick(fps)
