
import time
from game import Game
from ai import AI

def main():
    print("\n------------------------------------------------------\n")
    game_mode = int(input('Choose Your Game Mode:\n 0 - For two player\n 1 - Vs AI, You start First\n 2 - Vs AI, AI start with first\n 3 - Load your last play\nInput is: '))

    if game_mode == 3:        
        game = Game()
        ai = AI(0, game.is_stealing_mode)
        game.load()
    else:
        stealing = bool(int(input("Enter 0 for non-stealing mode or 1 for stealing mood : ")))
        difficulty = int(input("Enter:\n 0 - Easy\n 1 - Medium\n 2 - Hard\n 3 - Very_Hard\nInput is: ")) % 4
        game = Game(stealing, difficulty, game_mode)
        ai = AI(0, game.is_stealing_mode)
        difficulties = ["Easy", "Medium", "Hard", "Very_Hard", "Insanely_Hard"]
        print("\n*****************************************  Difficulty is {:}  *****************************************\n".format(difficulties[difficulty]))

    game.get_status()

    if game.game_mode == 1: 
        print("*******************************************     Player 1  Turn   *****************************************\n")
        move = int(input("Player 1 Choose  bucket to Move : ")) % 6
        game.choose_bucket(1, move)

        while True:
            game.get_status()
            # print("\n----------------------------------------------------------------------------------------------------------\n")
            if game.next_turn == 0:
                print("*******************************************     Computer  Turn   *****************************************\n")
                # move = int(input("Player 2 Choose  bucket to Move : "))% 6
                # game.choose_bucket(0, move)
                t1 = time.time()
                next_move = ai.predict(game.game.copy(), game.difficulty)
                print(f"Action Taken By AI at Depth: {game.difficulty} = {time.time() - t1}s ")
                game.choose_bucket(0, next_move)
            elif game.next_turn == 1:
                print("*******************************************     Player 1  Turn   *****************************************\n")
                move = int(input("Player 1 Choose  bucket to Move : "))% 6
                game.choose_bucket(1, move)
            else:
                print("*******************************    The End congratulations for the winner    *****************************\n")
                game.get_status()
                break
    elif game.game_mode == 2:
        print("*******************************************     Computer  Turn   *****************************************\n")
        t1 = time.time()
        next_move = ai.predict(game.game.copy(), game.difficulty)
        print(f"Action Taken By AI at Depth: {game.difficulty} = {time.time() - t1}s ")
        game.choose_bucket(0, next_move)
        while True:
            game.get_status()
            # print("\n----------------------------------------------------------------------------------------------------------\n")
            if game.next_turn == 0:
                print("*******************************************     Computer  Turn   *****************************************\n")
                # move = int(input("Player 2 Choose  bucket to Move : "))% 6
                # game.choose_bucket(0, move)
                t1 = time.time()
                next_move = ai.predict(game.game.copy(), game.difficulty)
                print(f"Action Taken By AI at Depth: {game.difficulty} = {time.time() - t1}s ")
                game.choose_bucket(0, next_move)
            elif game.next_turn == 1:
                print("*******************************************     Player 1  Turn   *****************************************\n")
                move = int(input("Player 1 Choose  bucket to Move : "))% 6
                game.choose_bucket(1, move)
            else:
                print("*******************************    The End congratulations for the winner    *****************************\n")
                game.get_status()
                break
    elif game.game_mode == 0:
        print("*******************************************     Player 1  Turn   *****************************************\n")
        move = int(input("Player 1 Choose  bucket to Move : ")) % 6
        game.choose_bucket(1, move)
        while True:
            game.get_status()
            # print("\n----------------------------------------------------------------------------------------------------------\n")
            if game.next_turn == 0:
                print("*******************************************     Player 2  Turn   *****************************************\n")
                move = int(input("Player 2 Choose  bucket to Move : ")) % 6
                game.choose_bucket(0, move)
            elif game.next_turn == 1:
                print("*******************************************     Player 1  Turn   *****************************************\n")
                move = int(input("Player 1 Choose  bucket to Move : "))% 6
                game.choose_bucket(1, move)
            else:
                print("*******************************    The End congratulations for the winner    *****************************\n")
                game.get_status()
                break
    else:
        print("*******************************   You entered a wrong key, Try again later    *****************************\n")
if __name__ == "__main__":
    main()
