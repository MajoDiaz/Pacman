"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.

"""
#A01701879 María José Díaz Sánchez
#A00829556 Santiago Gonzalez Irigoyen
#Este código es un juego de pacman

from random import choice, randint
from turtle import *
from freegames import floor, vector

state = {'score': 0}#esto marca cuantos puntos se comen
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80)
#con la variable ghost se generan los vectores para los fantasmas
#se cambio también el color de cada fantasma para distingurilos
ghosts = [
    [vector(-180, 160), vector(5, 0), 'right', 'red'],
    [vector(-180, -160), vector(0, 5), 'up', 'orange'],
    [vector(100, 160), vector(0, -5), 'down', 'cyan'],
    [vector(100, -160), vector(-5, 0), 'left', 'pink'],
]
'''En tiles es donde se constuyre básicamente el laberinto,
los 0 son el espacio en negro y los 1 son el camino diseñado.
Si se modifican los 1 y 0 se crea un nuevo tablero'''

'''Se modificaron los valores de tiles para crear un tabero modificado
esto se hizo cambiando algunos valores por 0 o por 1 según convenga para
el diseño del nuevo tablero'''

tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

def square(x, y):
    "Draw square using path at (x, y)."
    '''Esta función usa las coordenadas creadas en la función
    world, para crear el cuadrado de los caminos'''
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()

def offset(point):
    "Return offset of point in tiles."
    '''Esta función tambien ayuda a la funcion move
    creando un idex que es usado en los if de esa función'''
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

def valid(point):
    "Return True if point is valid in tiles."
    '''Esta función ayuda a ver si el punto es valido
    para el pacman, regresa su valor a la función move'''
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

def world():
    "Draw world using path."
    #Con esta función se crea el tablero
    #en este caso el fondo es negro
    #y el camino es azul
    bgcolor('black')
    path.color('white')
    #colors define los colores diferentes para los puntos
    colors = ['cyan', 'red', 'light green', 'orange']

    for index in range(len(tiles)):
        '''Esta funcion checa cuales de la lista son 1 y cuales
        0 para construir el laberinto. Se verifica que sean mayores
        a 0, para despues mandar ese vector [x,y] a la función
        square, la cual va a ir creando los cuadrado de cada posición.
        Si el valor de ese index del tile es 0, este se quedara en negro'''
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                #crea los distintos puntos con colores al azar
                path.dot(2, colors[randint(0,3)])

def move():
    "Move pacman and all ghosts."
    '''La función moce es la que ayuda a mover a todos
    los personajes, checa si topan con un recuadro negro, 
    si hay puntos en donde estan caminando y se apoya de otras
    funciones como valid y offset'''
    
    writer.undo()
    writer.write(state['score'])

    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow2')

    for point, course, history, id in ghosts:
        if valid(point + course):
            point.move(course)
        #Si se encuentra con una pared el fantasma, busca si está
        #a la izquierda, abajo, a la derecha o arriba de pacman
        #y entonces se mueve en dirección suya.
        #Se intercalaron los pares de moviminetos por eje para prevenir
        #que los fantasmas se atoren llendo de lado a lado. Si no se puede
        #ir en estas direcciones 'inteligentes', los fantasmas deciden al
        #azar de las direcciones posibles. De esta forma manejamos
        #posibles errores de lógica. History recuerda cual fue la última
        #dirección del fantasma y trata de evitar repeticiones.
        elif pacman.x > point.x and valid(point + vector(5,0)) and history != 'right':
            course.x = 5
            course.y = 0
            history = 'right'
            #con este print se mandan los cambios de dirección a la terminal
            print(str(id), 'change')
        elif pacman.y > point.y and valid(point + vector(0,5)) and history != 'up':
            course.x = 0
            course.y = 5
            history = 'up'
            print(str(id), 'change')
        elif pacman.x < point.x and valid(point + vector(-5,0)) and history != 'left':
            course.x = -5
            course.y = 0
            history = 'left'
            print(str(id), 'change')
        elif pacman.y < point.y and valid(point + vector(0,-5)) and history != 'down':
            course.x = 0
            course.y = -5
            history = 'down'
            print(str(id), 'change')
        else:
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            '''aqui están las distintas formas 
            en las que se mueven los fantasmas
            si no ven a pacman'''
            plan = choice(options)
            if plan == vector(5,0):
                history = 'right'
            if plan == vector(0,5):
                history = 'up'
            if plan == vector(-5,0):
                history = 'left'
            if plan == vector(0,-5):
                history = 'down'
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, id)

    update()

    for point, course, history, id in ghosts:
        if abs(pacman - point) < 20:
            return

    '''Ontimer pone la velocidad del juego
    entre mayor sea el valor que se le meta
    mas tiempor se tomarán en moverse, entre
    menor sea el valor más rápido se mueven'''

    '''En este caso se cambio el valor de 100
    a 35, para que se movieran más rápido'''
    ontimer(move, 35)

def change(x, y):
    "Change pacman aim if valid."
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

setup(420, 420, 370, 0)#define el espacio del juego
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])#escribe el puntaje en el tablero
listen()
#las siguientes funciones son para mover al pacman
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()
