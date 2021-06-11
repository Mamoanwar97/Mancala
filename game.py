import pickle
import numpy as np
from board import Board

class Game():
    def __init__(self, stealing=False, difficulty=0, game_mode=5):
        self.game = Board()
        self.is_stealing_mode = stealing # True for stealing 
        self.difficulties = [2, 5, 7, 10]
        self.difficulty = self.difficulties[difficulty]
        self.next_turn = 0
        self.game_mode = game_mode
    def save(self, save_path='./last_play.pickle'):
        data = {}
        data['game'] = self.game
        data['stealing'] = self.is_stealing_mode
        data['difficulty'] = self.difficulty
        data['next_turn'] = self.next_turn
        data['game_mode'] = self.game_mode
        with open(save_path, 'wb') as outfile:
            pickle.dump(data, outfile)

    def load(self, load_path='./last_play.pickle'):
        with open(load_path, 'rb') as handle:
            data =  pickle.load(handle)
            self.game = data['game']
            self.is_stealing_mode = data['stealing']
            self.difficulty = data['difficulty']
            self.next_turn = data['next_turn']
            self.game_mode = data['game_mode']
            
    def get_status(self):
        print("*****************************************  Computer score :  {} *****************************************\n".format(self.game.scores[0]))
        print("*****************************************  Player 1 score :  {} *****************************************\n".format(self.game.scores[1]))
        print(f"Board State \n{self.game.board}\n")

    def choose_bucket(self, player_no, bucket_no):
        game = self.game.board
        if np.sum(game[1]) == 0 or np.sum(game[0]) == 0:
            self.game.scores[player_no] += np.sum(game[player_no])
            self.game.scores[player_no ^ 1] += np.sum(game[player_no ^ 1])
            game =np.array([[0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0]])
            self.next_turn = 2
            return 0
        if player_no == 0:
            game = np.flip(game, (0, 1))
        if (game[1][bucket_no] == 0):
            self.next_turn = player_no
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Empty bucket has been selected play again XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            return 0
        rocks = game[1][bucket_no]
        game[1][bucket_no] = 0
        current = 1
        flag = 1
        self.next_turn = player_no ^ 1
        while rocks > 0:
            bucket_no = abs((bucket_no % 6) + (- 5) * (current ^ 1))
            score_bucket_distance = abs(bucket_no - 6 * current) +(current ^ 1)
            if bucket_no == 5 and current == 1:
                self.game.scores[player_no] = self.game.scores[player_no] + 1
                if rocks == 1:
                        self.next_turn = player_no
                if not rocks == 1: 
                    current = current ^ 1            
                rocks -= 1
                bucket_no = 0
            elif rocks > score_bucket_distance:
                self.game.scores[player_no] = self.game.scores[player_no] + current 
                if current == 0:
                    game[current][bucket_no - score_bucket_distance + (flag ^ 1) :bucket_no + (flag ^ 1) ] = game[current][bucket_no - score_bucket_distance + (flag ^ 1) :bucket_no + (flag ^ 1) ]  + 1
                else:
                    game[current][bucket_no +  (flag) :bucket_no + score_bucket_distance+ (flag) ] = game[current][bucket_no +  (flag) :bucket_no + score_bucket_distance+ (flag) ] + 1
                rocks = rocks - min(score_bucket_distance, 6)
                current = current ^ 1
                bucket_no = 0
            else:
                if rocks == score_bucket_distance and current:
                    self.next_turn = player_no
                if current == 0:
                    if self.is_stealing_mode and (game[0][min(bucket_no - rocks + 1, 5) ] == 0):
                        game[current][min(bucket_no - rocks + 1, 5) ] = -1
                        self.game.scores[player_no] = self.game.scores[player_no] + game[1][min(bucket_no - rocks + 1, 5) ] + 1
                        game[1][min(bucket_no - rocks + 1, 5) ] = 0
                    game[current][bucket_no - rocks + (flag ^ 1) :bucket_no + (flag ^ 1) ] = game[current][bucket_no - rocks + (flag ^ 1) :bucket_no + (flag ^ 1) ]  + 1
                else:
                    if self.is_stealing_mode and (game[1][min(bucket_no + rocks - (1 ^ flag), 5)] == 0):
                        game[current][min(bucket_no + rocks - (1 ^ flag), 5)] = -1
                        self.game.scores[player_no] = self.game.scores[player_no] + game[0][min(bucket_no + rocks - (1 ^ flag), 5)] + 1
                        game[0][min(bucket_no + rocks - (1 ^ flag), 5)] = 0
                    game[current][bucket_no+ (flag) :min(bucket_no + rocks + (flag), 6) ] = game[current][bucket_no+ (flag) :min(bucket_no + rocks + (flag), 6) ] + 1
                rocks = 0
            flag = 0
            
        if player_no == 0:
            game = np.flip(game, (0, 1))

        self.game.board = game
        
        self.save()
        if np.sum(game[1]) == 0 or np.sum(game[0]) == 0:
            self.game.scores[player_no] += np.sum(game[player_no])
            self.game.scores[player_no ^ 1] += np.sum(game[player_no ^ 1])
            game =np.array([[0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0]])
            self.next_turn = 2
            return 0

