import pygame
import random
import sys
from itertools import combinations

WIDTH = 800
ROWS = 8

RED = pygame.image.load('red.png')
GREEN = pygame.image.load('gray.png')

REDKING = pygame.image.load('redKing.png')
GREENKING = pygame.image.load('grayKing.png')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (235, 168, 52)
BLUE = (76, 252, 241)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('Checkers')

priorMoves = []


class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = BLACK
        self.piece = None

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / ROWS, WIDTH / ROWS))
        if self.piece:
            WIN.blit(self.piece.image, (self.x, self.y))


def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def make_grid(rows, width):
    grid = []
    gap = width // rows
    count = 0
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j, i, gap)
            if abs(i - j) % 2 == 0:
                node.colour = WHITE
            if (abs(i + j) % 2 == 0) and (i < 3):
                node.piece = Piece('R')
            elif (abs(i + j) % 2 == 0) and i > 4:
                node.piece = Piece('G')
            count += 1
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // ROWS
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))


class Piece:
    def __init__(self, team):
        self.team = team
        self.image = RED if self.team == 'R' else GREEN
        self.type = None

    def draw(self, x, y):
        WIN.blit(self.image, (x, y))


def getNode(grid, rows, width):
    gap = width // rows
    RowX, RowY = pygame.mouse.get_pos()
    Row = RowX // gap
    Col = RowY // gap
    return (Col, Row)


def resetColours(grid, node):
    positions = generatePotentialMoves(node, grid)[0]
    positions.append(node)

    for colouredNodes in positions:
        nodeX, nodeY = colouredNodes
        grid[nodeX][nodeY].colour = WHITE if abs(nodeX - nodeY) % 2 == 0 else BLACK


def can_click(clicked_node, grid, currmove):
    our_node = grid[clicked_node[0]][clicked_node[1]]
    positions = []
    for i in range(len(grid)):
        for j in range(len(grid)):
            cur_node = grid[i][j]
            if cur_node.piece and cur_node.piece.team == currmove:
                moves, is_beating = generatePotentialMoves((cur_node.col, cur_node.row), grid)
                positions.append((cur_node, is_beating, moves))
    is_beating_stuff = False
    for i in positions:
        if our_node == i[0] and len(i[2]) == 0:
            return False
        if our_node == i[0] and i[1] == 1:
            return True
        elif our_node != i[0] and i[1] == 1:
            is_beating_stuff = True
    return not is_beating_stuff


def HighlightpotentialMoves(piecePosition, grid):
    positions = generatePotentialMoves(piecePosition, grid)[0]
    for position in positions:
        Column, Row = position
        grid[Column][Row].colour = BLUE


def opposite(team):
    return "R" if team == "G" else "G"


def generatePotentialMoves(nodePosition, grid):
    checker = lambda x, y: x + y >= 0 and x + y < 8
    normal_positions = []
    beating_positions = []
    column, row = nodePosition
    if grid[column][row].piece:
        normal_vectors = [[1, -1], [1, 1]] if grid[column][row].piece.team == "R" else [[-1, -1], [-1, 1]]
        beating_vectors = [[1, -1], [1, 1], [-1, 1], [-1, -1]]
        if grid[column][row].piece.type == 'KING':
            normal_vectors = [[1, -1], [1, 1], [-1, -1], [-1, 1]]
            beating_vectors = [[1, -1], [1, 1], [-1, 1], [-1, -1]]
        for vector in normal_vectors:
            columnVector, rowVector = vector
            if checker(columnVector, column) and checker(rowVector, row):
                # grid[(column+columnVector)][(row+rowVector)].colour=ORANGE
                if not grid[(column + columnVector)][(row + rowVector)].piece:
                    normal_positions.append((column + columnVector, row + rowVector))
        for vector in beating_vectors:
            columnVector, rowVector = vector
            if checker(columnVector, column) and checker(rowVector, row):
                if grid[column + columnVector][row + rowVector].piece and \
                        grid[column + columnVector][row + rowVector].piece.team == opposite(
                    grid[column][row].piece.team):
                    if checker((2 * columnVector), column) and checker((2 * rowVector), row) \
                            and not grid[(2 * columnVector) + column][(2 * rowVector) + row].piece:
                        beating_positions.append((2 * columnVector + column, 2 * rowVector + row))
    if len(beating_positions) != 0:
        return beating_positions, 1
    return beating_positions + normal_positions, 0


"""
Error with locating opssible moves row col error
"""


def highlight(ClickedNode, Grid, OldHighlight):
    Column, Row = ClickedNode
    Grid[Column][Row].colour = ORANGE
    if OldHighlight:
        resetColours(Grid, OldHighlight)
    HighlightpotentialMoves(ClickedNode, Grid)
    return (Column, Row)


def is_end_of_game(grid):
    red_count = 0
    gray_count = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            cm = grid[i][j]
            if cm.piece:
                if cm.piece.team == 'R':
                    red_count += 1
                if cm.piece.team == 'G':
                    gray_count += 1
    return not (red_count != 0 and gray_count != 0), red_count, gray_count


def move(grid, piecePosition, newPosition):
    resetColours(grid, piecePosition)
    newColumn, newRow = newPosition
    oldColumn, oldRow = piecePosition

    piece = grid[oldColumn][oldRow].piece
    grid[newColumn][newRow].piece = piece
    grid[oldColumn][oldRow].piece = None

    if newColumn == 7 and grid[newColumn][newRow].piece.team == 'R':
        grid[newColumn][newRow].piece.type = 'KING'
        grid[newColumn][newRow].piece.image = REDKING
    if newColumn == 0 and grid[newColumn][newRow].piece.team == 'G':
        grid[newColumn][newRow].piece.type = 'KING'
        grid[newColumn][newRow].piece.image = GREENKING
    if abs(newColumn - oldColumn) == 2 or abs(newRow - oldRow) == 2:
        grid[int((newColumn + oldColumn) / 2)][int((newRow + oldRow) / 2)].piece = None
        if generatePotentialMoves(newPosition, grid)[1] == 1:
            return grid[newColumn][newRow].piece.team
        else:
            return opposite(grid[newColumn][newRow].piece.team)
    return opposite(grid[newColumn][newRow].piece.team)


def checkers(WIDTH, ROWS, curmove):
    grid = make_grid(ROWS, WIDTH)
    highlightedPiece = None
    currMove = curmove

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('EXIT SUCCESSFUL')
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                clickedNode = getNode(grid, ROWS, WIDTH)
                ClickedPositionColumn, ClickedPositionRow = clickedNode
                if grid[ClickedPositionColumn][ClickedPositionRow].colour == BLUE:
                    if highlightedPiece:
                        pieceColumn, pieceRow = highlightedPiece
                    if currMove == grid[pieceColumn][pieceRow].piece.team:
                        resetColours(grid, highlightedPiece)
                        currMove = move(grid, highlightedPiece, clickedNode)
                elif highlightedPiece == clickedNode:
                    pass
                else:
                    if grid[ClickedPositionColumn][ClickedPositionRow].piece:
                        if currMove == grid[ClickedPositionColumn][ClickedPositionRow].piece.team:
                            if can_click(clickedNode, grid, currMove):
                                highlightedPiece = highlight((ClickedPositionColumn, ClickedPositionRow), grid,
                                                             highlightedPiece)
        end, red_count, gray_count = is_end_of_game(grid)
        if end:
            import gameover_screen
            if red_count == 0:
                gameover_screen.gameover_menu('G')
            else:
                gameover_screen.gameover_menu('R')
        update_display(WIN, grid, ROWS, WIDTH)


if __name__ == "__main__":
    checkers(WIDTH, ROWS)
