from game import BLACK, WHITE, Game
from piece import Pawn, Knight, Bishop
from config import COLORS, CHARS
from move import Move


RESULTS = ("Draw", "White won", "Black won")

game = Game()

try:
    while True:
        print("\033[H\033[J", end="")
        print("    a b c d e f g h\n")
        for y in range(7, -1, -1):
            print(y + 1, end="   ")
            for x in range(8):
                piece = game.board[x][y]
                char = CHARS[piece]
                if piece:
                    print(f"{COLORS[piece.side]}{char}\033[0m", end=" ")
                else:
                    print(char, end=" ")
            print(f"  {y + 1}")
        print("\n    a b c d e f g h\n")
        if game.over:
            print(f"{RESULTS[game.result]}\n")
        print(*(notation for move in game.moves for notation in move.notation()))
        match (action := input("> ")):
            case "new":
                game.setup()
            case "exit":
                break
            case "undo":
                game.undo()
            case _:
                game.move(action)

except KeyboardInterrupt:
    print()

