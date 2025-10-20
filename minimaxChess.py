import chess
import random
import datetime
import math

def getEval(captured_piece:chess.Piece|None) -> int:

    if (captured_piece == None):
        return 0
    else:
        if captured_piece.piece_type == chess.PAWN:
            return 1
        elif captured_piece.piece_type == chess.KNIGHT:
            return 3
        elif captured_piece.piece_type == chess.BISHOP:
            return 3
        elif captured_piece.piece_type == chess.ROOK:
            return 5
        elif captured_piece.piece_type == chess.QUEEN:
            return 9
        else:
            return 0


def main () -> None:

    print("="*33)
    print(f"\tWelcome to Chess!")
    print("="*33)
    print(f"Time: {datetime.datetime.now()}")

    botColor = input("Computer player? (w=white/b=black): ")
    startingFEN = input("Starting FEN position? (hit ENTER for standard starting postion): ")
    board = None
    if (startingFEN == ""):
        board = chess.Board()
    else:
        board = chess.Board(startingFEN)
    
    botName = ""
    playerName = "" 
    
    if (botColor == "w"):
       botColor = chess.WHITE
       botName = "Bot (as white)"
       playerName = "Black"
    elif (botColor == "b"):
        botColor = chess.BLACK
        botName = "Bot (as black)"
        playerName = "White"

    print("Printing Initial Board......")
    print(board)
    print("-----------------")
    while not board.is_game_over() :
        # if its the bots turn 
        if (board.turn == botColor):
            moveList = list(board.legal_moves)
            randIndex = random.randint(0,len(moveList)-1)

            botMove = moveList[randIndex]
            best_score = -math.inf
            best_move = None
            for move in moveList:
                baseBoard = chess.BaseBoard(board.board_fen())
                move_piece = baseBoard.piece_at(move.to_square)
                print(move_piece)
                player_move_score = getEval(move_piece)
                
                board.push(move) 
                moveList_opp = list(board.legal_moves)
                
                for opp_move in moveList_opp:
                    baseBoard = chess.BaseBoard(board.board_fen())
                    move_piece = baseBoard.piece_at(opp_move.to_square)
                    print(move_piece)
                    opp_move_score = getEval(move_piece)

                    score = player_move_score - opp_move_score
                    board.pop()

                    if score > best_score:
                        best_score = score
                        best_move = move


                    
            print(f"{botName}: {botMove}")

            board.push(botMove)
            print(f"New FEN position: {board.fen()}")
        else:
            moveList = list(board.legal_moves)

            playerInput = input(f"{playerName}: ")
            
            playerMove = None

            try:
                playerMove = chess.Move.from_uci(playerInput)
            except:
                print("Make sure your input is in UCI format!")
                playerInput = input(f"{playerName}: ")

            if playerMove not in moveList:
                print("That move is not legal! Try again?")
            else:
                board.push(playerMove)
                print(f"New FEN position: {board.fen()}")
        print(board)

        f = open("gameFen.txt", "w")
        f.write(f"Last Fen: {board.fen()}")

    print("-----------------")
    print(f"Game Result: {board.result()}")
    print(board)

    board.reset()


if __name__ == "__main__":
    main()

