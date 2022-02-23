from mimetypes import init, inited
import pygame
import math
import random

BOARD_SIZE = 3 #exponent of 2
TILE_WIDTH = 20
WIDTH = TILE_WIDTH*2**BOARD_SIZE
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

CLOSED = (255, 0, 0)
OPEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
BLANK = (255, 255, 255)
BARRIER = (0, 0, 0)
PATH = (255, 255, 0)# (128, 0, 128)
START = (255, 165 ,0)
SEPARATOR = (128, 128, 128)
END = (64, 224, 208)


HEADS = (255, 0, 0)
TAILS = (0, 200, 0)
CHOSEN = (255, 255, 0)


class Tile:
    def __init__(self, row, col, width, bit) -> None:
        self.row, self.col = row, col
        self.x = row*width
        self.y = col*width
        self.bit = bit
        self.width = width
        self.radius = width//2
        self.center = (row*width+self.radius,col*width+self.radius)
        self.chosen = False
        self.reset_color()

    def draw(self, win):
        pygame.draw.rect(win,BLANK,(self.x,self.y,self.width, self.width))
        pygame.draw.circle(win,self.color,self.center,self.radius)
    
    def invert(self):
        self.bit = 1-self.bit
        self.reset_color()
    def choose(self):
        self.chosen = True
        self.color = CHOSEN
    def unchoose(self):
        self.chosen = False
        self.reset_color()
    def reset_color(self):
        self.color = HEADS if self.bit else TAILS

def make_grid(rows, width):
    gap = width//rows
    grid = [[Tile(i,j,gap,int(random.random()>0.5)) for j in range(rows)] for i in range(rows)]
    return grid

def draw_gridlines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        line_row_start = (0,i*gap)
        line_row_end = (width,i*gap)
        pygame.draw.line(win,SEPARATOR,line_row_start,line_row_end)
        line_col_start = (i*gap,0)
        line_col_end = (i*gap,width)
        pygame.draw.line(win,SEPARATOR,line_col_start,line_col_end)

def draw_grid(win, grid, rows, width):
    win.fill(BLANK)

    for row in grid:
        for node in row:
            node.draw(win)
    draw_gridlines(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    
    y, x = pos
    
    row = y // gap
    col = x // gap

    return row, col

def main_loop(win, width):
    ROWS = 2**BOARD_SIZE
    grid = make_grid(ROWS, width)

    start = None
    end = None

    state = None

    run = True
    started = False
    PLAYER1 = 1
    PLAYER2 = 2
    ADVERSARY = 4

    turn = ADVERSARY
    inverted_coin = None
    chosen_coin = None
    paused = False
    while run:
        draw_grid(win, grid,ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                run = False
                break

            if pygame.mouse.get_pressed()[0]: # flip coin
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                tile = grid[row][col]
                
                if turn & ADVERSARY:
                    tile.invert()
                elif turn & PLAYER1:
                    if inverted_coin is None:
                        tile.invert()
                        inverted_coin = tile
                    elif inverted_coin == tile:
                        tile.invert()
                        inverted_coin = None
                    else:
                        pass
                elif turn & PLAYER2:
                    if chosen_coin and tile == chosen_coin:
                        #WIN
                        pass
                    else:
                        #LOSE
                        pass
            elif pygame.mouse.get_pressed()[1]: #change player
                if turn & ADVERSARY:
                    turn = PLAYER1
                    chosen_coin.reset_color()
                elif turn & PLAYER1:
                    turn = PLAYER2
                else: # turn & PLAYER2
                    turn = ADVERSARY
                    if not chosen_coin is None:
                        chosen_coin.choose()
                

            elif pygame.mouse.get_pressed()[2]: #right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                tile = grid[row][col]

                if turn & ADVERSARY:
                    if chosen_coin is None:
                        tile.choose()
                        chosen_coin = tile
                    elif chosen_coin == tile:
                        tile.unchoose()
                        chosen_coin = None
                    else:
                        pass

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_c:
            #         start = None
            #         end = None
            #         state = None
            #         grid = make_grid(ROWS, width)
            #     elif event.key == pygame.K_r:
            #         grid = gen_maze_grid(ROWS, width)
            #         start = grid[0][0]
            #         start.make_start()
            #         end = grid[ROWS-1][ROWS-2]
            #         end.make_end()
            #         state = None
            #     elif event.key == pygame.K_s:
            #         import tkinter as tk
            #         from tkinter import simpledialog
            #         tk.Tk().wm_withdraw() #to hide the main window
            #         ROWS = simpledialog.askinteger("resize","enter new size")
            #         grid = make_grid(ROWS, width)
            #         start = None
            #         end = None
            #         state = None
            #         run = True
            #         started = False
            #         paused = False
            #         continue
            #     if start and end \
            #         and event.key == pygame.K_SPACE and not started:
            #         for row in grid:
            #             for node in row:
            #                 node.update_neighbors(grid)
            #         state = astar_alg(lambda: draw_grid(win, grid, ROWS, width), grid, start, end)
            #     if event.key == pygame.K_p:
            #         if not (state is True or state is False):
            #             astar_alg(lambda: draw_grid(win, grid, ROWS, width), grid, start, end, state)
    pygame.quit()



main_loop(WIN, WIDTH)