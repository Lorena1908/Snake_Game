import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
pygame.font.init()

width = 500
window = pygame.display.set_mode((width, width))
pygame.display.set_caption('Snake')

class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny): # Add the directions to the current position
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        distance = self.w // self.rows # 25
        row = self.pos[0] # x
        column = self.pos[1] # y

        pygame.draw.rect(surface, self.color, (row * distance + 1.8, column * distance + 1.8, distance - 2, distance - 2)) 
        # The (distance - 2) makes the rectangle be drawn inside the white grid lines
        # The 1.8 in (row * distance + 1.8) offsets the cube to be more in the center of the grid lines

        if eyes:
            center = distance // 2
            radius = 3 # Border
            circle_middle1 = (row * distance + center - radius, column * distance + 8)
            circle_middle2 = (row * distance + distance - radius * 2, column * distance + 8)
            pygame.draw.circle(surface, (0,0,0), circle_middle1, radius) # Left eye
            pygame.draw.circle(surface, (0,0,0), circle_middle2, radius) # Right eye
die = False
class Snake(object):
    body = []
    turns = {} # Stores the position of the head when the snake turned
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos) # self.body[0] is the head, so the self.body list is never empty
        self.body.append(self.head)
        self.dirny = 0 # This is the x speed
        self.dirny = 1 # This is the Y speed
        # The dirnx and dirny are different, one is 0 and one is 1 because you can only move on one
        # direction at a time

    def move(self):
        for event in pygame.event.get(): # For every key that is pressed, or anything happens
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed() # Dictionary of keys that get pressed or not (True:1 ; False:0)

            # MOVEMENTS
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos] = [self.dirnx, self.dirny] # Assigns the current position to the head
                    # turns is a dictionary. The line above is the same as
                    # self.turns = {"self.head.pos":"[self.dirnx, self.dirny]"}
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos] = [self.dirnx, self.dirny]

        # Border checking
        for index, cube in enumerate(self.body):
            posi = cube.pos

            # It makes the turning movement
            if posi in self.turns:
                turn = self.turns[posi] # Return the direction of the movement in a list
                cube.move(turn[0], turn[1])
                # This will move each cube to the position of the head
                if index == len(self.body)-1: # Last cube
                    self.turns.pop(posi) # This removes the last turned position to the snake only turn when we click

            # Border checking
            else: # pos[0] -> x , pos[1] -> y
                if cube.dirnx == -1 and cube.pos[0] <= 0:
                    die(self)
                elif cube.dirnx == 1 and cube.pos[0] >= cube.rows-1:
                    die(self)
                elif cube.dirny == 1 and cube.pos[1] >= cube.rows-1:
                    die(self)
                elif cube.dirny == -1 and cube.pos[1] <= 0:
                    die(self)
                else:
                    cube.move(cube.dirnx, cube.dirny)

    def reset(self, pos): # Reset everything
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1] # Last cube
        dx, dy = tail.dirnx, tail.dirny

        # It checks the movement of the snake to add the cube at the end of the tail
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))

        # set the direction of the new cube
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for index, cube in enumerate(self.body):
            if index == 0: # If it is the head it'll draw eyes on it
                cube.draw(surface, True)
            else:
                cube.draw(surface)

def drawGrid(w, rows, surface):
    size_between = w // rows # The // round the number to the smaller integer

    x = 0
    y = 0
    for line in range(rows):
        x = x + size_between
        y = y + size_between

        pygame.draw.line(surface, (255,255,255), (x,0), (x,w)) # The line is gonna be drawn between (0,0) and (x,w)
        pygame.draw.line(surface, (255,255,255), (0,y), (w,y))

def redrawWindow(surface):
    global rows, width, snake_object, snack
    surface.fill((0,0,0))
    snake_object.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, snake):
    positions = snake.body

    while True:
        x = random.randrange(rows) # Random x position for the snack
        y = random.randrange(rows) # Random Y position for the snack
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            # It creates a filtered list from the "positions" list. z is a position in positions
            # It checks if the position of the the cubes from the body are at the same position of...
            # ...the random snack. 0: False, 1: True
            continue # Returns to the begining of the loop
        else:
            break
    return (x,y)

def die(snake):
    run = True

    while run:
        window.fill((0,0,0))
        font = pygame.font.SysFont('comicsans', 60)
        text = font.render('Press Any Key to Play', 1, (255,255,255))
        window.blit(text, (width/2 - text.get_width()/2, width/2 - text.get_height()/2 - 40))
        score = font.render(f'Score: {len(snake.body)}', 1, (255,255,255))
        window.blit(score, (width/2 - score.get_width()/2, width/2 - score.get_height()/2 + 40))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            
            if event.type == pygame.KEYDOWN:
                snake.reset((10,10))
                run = False

                redrawWindow(window)

def main():
    global width, rows, snake_object, snack, window
    rows = 20
    snake_object = Snake((255,0,0), (10,10)) # This creates the snake object at the center of the screen
    snack = Cube(randomSnack(rows, snake_object), color=(0,255,0))

    clock = pygame.time.Clock()

    while True:
        pygame.time.delay(50) # It delays the program in 50 milisseconds so that the program doesn't run too fast
        clock.tick(10) # This make the game run in less than 10 frames per second, otherwise it would be too fast
        snake_object.move()
        if snake_object.head.pos == snack.pos:
            snake_object.addCube()
            snack = Cube(randomSnack(rows, snake_object), color=(0,255,0))
            # I don't need to make the snack disappear because the line above will change the position of the snack

        for cube in range(len(snake_object.body)):
            if snake_object.body[cube].pos in list(map(lambda z:z.pos, snake_object.body[cube+1:])) and die:
                # If the position of the cube x is in a list that contains all of the positions of the cubes after the x one
                # then it means that the snake hit itself
                die(snake_object)
                break

        redrawWindow(window)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        window.fill((0,0,0))
        font = pygame.font.SysFont('comicsans', 60)
        text = font.render('Press Any Key to Play', 1, (255,255,255))
        window.blit(text, (width/2 - text.get_width()/2, width/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            
            if event.type == pygame.KEYDOWN:
                main()

menu_screen()