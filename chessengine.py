import pygame as p
import copy


board = [['', 'wb', ''],
         ['bb', '', 'bknt'],
         ['', '', 'br']]



width = height = 512
dimension = 3
sq_size = width // dimension
images = {}


def loadImages():
    pieces = ['wb', 'bb', 'bknt', 'br']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (sq_size, sq_size))


def drawGameState(screen, board):
    drawBoard(screen)
    drawPieces(screen, board)


def drawBoard(screen):
    colors = [p.Color("#F1D9B8"), p.Color("#B88866")]
    for r in range(dimension):
        for k in range(dimension):
            color = colors[((r + k) % 2)]
            p.draw.rect(screen, color, p.Rect(k * sq_size, r * sq_size, sq_size, sq_size))


def drawPieces(screen, board):
    for r in range(dimension):
        for k in range(dimension):
            piece = board[r][k]
            if piece != '':
                screen.blit(images[piece], p.Rect(k * sq_size, r * sq_size, sq_size, sq_size))


def validRookMove(start_pos, end_pos, board):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if start_row == end_row:
        # Horizontal move
        step = 1 if start_col < end_col else -1
        for col in range(start_col + step, end_col, step):
            if board[start_row][col] != '':
                return False
        return True

    elif start_col == end_col:
        # Vertical move
        step = 1 if start_row < end_row else -1
        for row in range(start_row + step, end_row, step):
            if board[row][start_col] != '':
                return False
        return True

    return False

def validBishopMove(start_pos, end_pos, board):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    if abs(start_row - end_row) != abs(start_col - end_col):
        return False

    if abs(start_row - end_row) > 2 or abs(start_col - end_col) > 2:
        return False


    row_step = 1 if start_row < end_row else -1
    col_step = 1 if start_col < end_col else -1

    row, col = start_row + row_step, start_col + col_step
    while (row, col) != (end_row, end_col):
        if board[row][col] != '':
            return False
        row += row_step
        col += col_step

    return True


def validKnightMove(start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    return (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or \
           (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2)



def movePiece(board, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    piece = board[start_row][start_col]
    target_piece = board[end_row][end_col]

    if start_pos == end_pos:
        print(f"Invalid move: Piece {piece} at {start_pos} to {end_pos}")
        return False

    if piece == 'wb' and validBishopMove(start_pos, end_pos, board) or \
            piece == 'bb' and validBishopMove(start_pos, end_pos, board) or \
            piece == 'bknt' and validKnightMove(start_pos, end_pos) or \
            piece == 'br' and validRookMove(start_pos, end_pos, board):
        if target_piece == '' or target_piece[0] != piece[0]:
            board[end_row][end_col] = piece
            board[start_row][start_col] = ''
            return True

    print(f"Invalid move: Piece {piece} at {start_pos} to {end_pos}")
    return False


def whitePieceLoc(board):
    for r in range(dimension):
        for k in range(dimension):
            if board[r][k] == 'wb':
                return r, k

def blackPieceLoc(board):
    for r in range(dimension):
        for k in range(dimension):
            if board[r][k] != 'wb' and board[r][k] != '':
                return r, k


def stateGenerator(board, color):
    tempboard = copy.deepcopy(board)
    moves=[]
    
    if color == 'white' and whitePieceLoc(board) is not None:
        x, y = whitePieceLoc(board)
        for r in range(dimension):
            for k in range(dimension):
                target = tempboard[r][k]
                if movePiece(tempboard, (x, y), (r, k)):
                    if copy.deepcopy(tempboard) not in moves:
                        moves.append(copy.deepcopy(tempboard))
                    tempboard[x][y] = tempboard[r][k]
                    tempboard[r][k] = target

    elif color == 'black' and blackPieceLoc(board) is not None:
        for r in range(dimension):
            for k in range(dimension):
                if board[r][k] != 'wb' and board[r][k] != '':
                    x, y = r, k
                    for i in range(dimension):
                        for j in range(dimension):
                            target = tempboard[i][j]
                            if movePiece(tempboard, (x, y), (i, j)):
                                if copy.deepcopy(tempboard) not in moves:
                                    moves.append(copy.deepcopy(tempboard))
                                tempboard[x][y] = tempboard[i][j]
                                tempboard[i][j] = target
                                    
    return moves

def save_screenshot(screen, move_number):
    filename = f"screenshots/screenshot_{move_number}.png"
    p.image.save(screen, filename)

def main():
    
    board = [['', 'wb', ''],
            ['bb', '', 'bknt'],
            ['', '', 'br']]


    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()

    loadImages()
    running = True

    # Draw the initial game state
    drawGameState(screen, board)
    p.display.flip()

    move_number = 0

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN and e.button == 1:  # Left mouse button clicked
                if move_number < len(validMoves):
                    # Update the board with the next move
                    board = validMoves[move_number]
                    move_number += 1

                    # Draw the updated game state
                    drawGameState(screen, board)
                    p.display.flip()

                    # Save a screenshot
                    save_screenshot(screen, move_number)

        clock.tick(30)  

    p.quit()
i=0
color='white'
validMoves=[]
lastList=[]
validMoves.append(board)
moveList=stateGenerator(board,color)
validMoves+=moveList
lastList=moveList
moveList=[]
for i in range(2): #The tree depth is 2 and it is adjustable, which means it generates all possible moves for each piece for 2 turns for both colors.
    if(color=='white'):
        color='black'
    else:
        color='white'
    for move in lastList:
        moveList+=stateGenerator(move,color)
    for move in moveList:
        if move not in validMoves:
            validMoves.append(move)
    lastList=copy.deepcopy(moveList)
    moveList.clear()

print(validMoves)
print(len(validMoves))

if __name__ == "__main__":
    main()