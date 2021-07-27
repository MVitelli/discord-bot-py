import sys
from PIL import Image, ImageDraw, ImageFont

MARCO = 4
PIECE_SIZE = 76
BOARD_SIZE = (570, 570)

class fourInARowMatch:
    # ----------------------------------------------------
    def checkWinner(self, player = None):
        if player == None:
            player = self.playerTurn
        board = self.boardList
        if 0 not in board[5]:
            self.winner = 3
            return 3
        for i in range(3):
            for j in range(4):
                if board[i][j] == player and  board[i][j+1] == player and  board[i][j+2] == player and  board[i][j+3] == player:
                    self.winner = player
                    return player
                if board[i][j] == player and  board[i+1][j] == player and  board[i+2][j] == player and  board[i+3][j] == player:
                    self.winner = player
                    return player
                if board[i][j] == player and  board[i+1][j+1] == player and  board[i+2][j+2] == player and  board[i+3][j+3] == player:
                    self.winner = player
                    return player
                if board[i][j+3] == player and  board[i+1][j+2] == player and  board[i+2][j+1] == player and  board[i+3][j] == player:
                    self.winner = player
                    return player
        return 0

    # ----------------------------------------------------
    def boardUpdate(self):
        board = self.boardList
        def coorX(i):
            i-=1
            return (i * PIECE_SIZE + MARCO + 30)
        def coorSlot(i, j):
            return (j * PIECE_SIZE + MARCO + (PIECE_SIZE / 2), i * PIECE_SIZE + 84 + (PIECE_SIZE / 2))
        def coorSlotWidth(i, j, ancho):
            return (coorSlot(i, j), ancho)

        with Image.open("4inrowboard.png") as boardImage:
            fnt = ImageFont.truetype("arial.ttf", 30)
            k= 25
            draw = ImageDraw.Draw(boardImage)
            i=5
            for fila in board:
                j=0
                for slot in fila:
                    draw.regular_polygon(coorSlotWidth(i, j, 30), n_sides=30, rotation=0, fill="#000000", outline=None)
                    if slot == 1:
                        draw.regular_polygon(coorSlotWidth(i, j, k), n_sides=28, rotation=0, fill="#ff0000", outline=None)
                    elif slot == 2:
                        draw.regular_polygon(coorSlotWidth(i, j, k), n_sides=28, rotation=0, fill="#00ff00", outline=None)
                    else:
                        draw.regular_polygon(coorSlotWidth(i, j, k), n_sides=28, rotation=0, fill="#ffffff", outline=None)
                    j+=1
                i-=1
            for i in range(1, 8):
                draw.multiline_text((coorX(i), 30), str(i), font=fnt, fill=(0, 0, 0))
            for i in range(1, 7):
                draw.line((i * PIECE_SIZE + MARCO, 20, i * PIECE_SIZE + MARCO, 530), fill=128, width=3)
            draw.line((MARCO, 84, 540 - MARCO, 84), fill=128, width=3)

            # write to stdout
            boardImage.save("img/4inrow.png")
            # boardImage.show()

    # ----------------------------------------------------
    def changePlayer(self):
        if self.playerTurn == 1:
            self.playerTurn = 2
        else:
            self.playerTurn = 1

    # ----------------------------------------------------
    def addPiece(self, move):

        try:
            move = int(move)
        except:
            return False
        if (move < 1 or move > 7) or self.boardList[5][move-1] != 0:
            return False
        for col in range(6):
            if self.boardList[col][move-1] == 0:
                self.boardList[col][move-1] = self.playerTurn
                return True

    # ----------------------------------------------------
    def showWinner(self):
        if self.winner == 3:
            print("empate")
        else:
            print("ganador jugador", self.winner)

    def getMatchInProg(self):
        return self.matchInProg

    def newMatchInProg(self):
        self.matchInProg = True
    
    def getCurrentPlayer(self):
        return self.playerTurn

    def __init__(self):
        self.boardList = [[0 for i in range(7)] for i in range(6)]
        self.playerTurn = 1
        self.winner = 0
        self.boardUpdate()
        self.matchInProg = False

# -----------------------------------------------------
# -----------------------------------------------------
# -----------------------------------------------------
if __name__ == '__main__':
    print("I'm a module")
    match = fourInARowMatch()
    while not match.winner:
        match.boardUpdate()
        if not match.addPiece(input("ingrese su jugada: ")):
            print('Ingrese un casillero válido')
            continue
    match.boardUpdate()
    match.showWinner()
