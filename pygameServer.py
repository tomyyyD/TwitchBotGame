import socket
import time
import sys
import pygame
import threading

# constants
HEIGHT = 600
WIDTH = 800
BLOCK_SIZE = 20

numPogs = 0
running = True
moveSpeed = 10

posX = WIDTH/2 - BLOCK_SIZE/2
posY = HEIGHT/2 - BLOCK_SIZE/2

obstacles = [
    pygame.Rect((0, 0), (440, BLOCK_SIZE)),
    pygame.Rect((0, 100), (360, BLOCK_SIZE)),
    pygame.Rect((440, 0), (BLOCK_SIZE, 400)),
    pygame.Rect((340, 100), (BLOCK_SIZE, 320)),
    pygame.Rect((340, 400), (120, BLOCK_SIZE)),
    # pygame.Rect((420, 69), (OBSTACLE_SIZE, OBSTACLE_SIZE/2)),
]

finishLine = pygame.Rect((0, 20), (BLOCK_SIZE*4, BLOCK_SIZE*4))

isWin = False

# initializes pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TwitchBot Game!")
font = pygame.font.SysFont('timesnewroman', 30)

# initializes socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 1024))
s.listen(5)


def receiveInput():
    global isWin
    global posX
    global posY
    searching = True
    while searching:
        clt, adr = s.accept()
        msg = clt.recv(1024).decode("utf-8")

        # update player position
        if msg == 'a':
            posX -= moveSpeed
        elif msg == 'd':
            posX += moveSpeed
        elif msg == 'w':
            posY -= moveSpeed
        elif msg == 's':
            posY += moveSpeed

        # screen edges check
        if (posX < 0):
            posX = 0
        elif (posY < 0):
            posY = 0
        elif(posX > WIDTH - BLOCK_SIZE):
            posX = WIDTH - BLOCK_SIZE
        elif (posY > HEIGHT - BLOCK_SIZE):
            posY = HEIGHT - BLOCK_SIZE

        # wall check
        for w in obstacles:
            # print(w.x)
            # print(w.x + w.width)
            # print(f"{posX} > {w.x} and {posX} < {w.x + w.width}, {posY} > {w.y} and {posY} < {w.y + w.height}")
            if(posX + BLOCK_SIZE > w.x and posX < w.x + w.width and posY + BLOCK_SIZE > w.y and posY < w.y + w.height):
                posX = WIDTH/2 - BLOCK_SIZE/2
                posY = HEIGHT/2 - BLOCK_SIZE/2
                isWin = False

        if(posX + BLOCK_SIZE > finishLine.x and posX < finishLine.x + finishLine.width and posY + BLOCK_SIZE > finishLine.y and posY < finishLine.y + finishLine.height):
            #print("you win game Poggers!")
            isWin = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                searching = False
                # thread1.join()


thread1 = threading.Thread(
    group=None, target=receiveInput, name=None, args=(), kwargs={}, daemon=None)
thread1.start()


while running:
    win.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # clt, adr = s.accept()
    # msg = clt.recv(1024).decode("utf-8")
    # print(msg)

    # else:
    #     if msg == 'a':
    #         posX -= 10
    #     elif msg == 'd':
    #         posX += 10
    #     elif msg == 'w':
    #         posY -= 10
    #     elif msg == 's':
    #         posY += 10
    #     else:
    #         text = font.render(f'Pogs: {msg}', True, (255, 100, 100))

    player = pygame.Rect((posX, posY), (BLOCK_SIZE, BLOCK_SIZE))

    pygame.draw.rect(win, (0, 255, 0), finishLine)

    for obstacle in obstacles:
        pygame.draw.rect(win, (255, 0, 0), obstacle)

    if (isWin):
        label = font.render("You have won!", 1, (0, 0, 0))
        win.blit(label, (WIDTH/2 - BLOCK_SIZE/2, HEIGHT/2 - BLOCK_SIZE/2))

    # win.blit(text, (0, 0))
    # win.blit(circle, (posX, posY))

    pygame.draw.rect(win, (0, 0, 0), player)

    pygame.display.update()
