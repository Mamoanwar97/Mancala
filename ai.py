import numpy as np
from numpy.lib.function_base import place



class AI():
    def __init__(self, no, stealing=False):
        self.no = no
        self.difficulty = None
        self.is_stealing_mode = stealing

    def __simulate_move(self, bucket_no, player_no, game_state):
        game_state = game_state.copy()
        game = game_state.board
        if np.sum(game[1]) == 0 or np.sum(game[0]) == 0:
            game_state.scores[player_no] += np.sum(game[player_no])
            game_state.scores[player_no ^ 1] += np.sum(game[player_no ^ 1])
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
                game_state.scores[player_no] = game_state.scores[player_no] + 1
                # print(player_no, " ", current, " ",bucket_no, " ",rocks)
                if rocks == 1:
                        self.next_turn = player_no
                if not rocks == 1: 
                    current = current ^ 1            
                rocks -= 1
                bucket_no = 0
            elif rocks > score_bucket_distance:
                game_state.scores[player_no] = game_state.scores[player_no] + current 
                if current == 0:
                    if self.is_stealing_mode and (game[0][min(bucket_no - rocks + 1, 5) ] == 0):
                        game[current][min(bucket_no - rocks + 1, 5) ] = -1
                        game_state.scores[player_no] = game_state.scores[player_no] + game[1][min(bucket_no - rocks + 1, 5) ] + 1
                        game[1][min(bucket_no - rocks + 1, 5) ] = 0
                    game[current][bucket_no - score_bucket_distance + (flag ^ 1) :bucket_no + (flag ^ 1) ] = game[current][bucket_no - score_bucket_distance + (flag ^ 1) :bucket_no + (flag ^ 1) ]  + 1
                else:
                    if self.is_stealing_mode and (game[1][min(bucket_no + rocks - (1 ^ flag), 5)] == 0):
                        game[current][min(bucket_no + rocks - (1 ^ flag), 5)] = -1
                        game_state.scores[player_no] = game_state.scores[player_no] + game[0][min(bucket_no + rocks - (1 ^ flag), 5)] + 1
                        game[0][min(bucket_no + rocks - (1 ^ flag), 5)] = 0
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
                        game_state.scores[player_no] = game_state.scores[player_no] + game[1][min(bucket_no - rocks + 1, 5) ] + 1
                        game[1][min(bucket_no - rocks + 1, 5) ] = 0
                    game[current][bucket_no - rocks + (flag ^ 1) :bucket_no + (flag ^ 1) ] = game[current][bucket_no - rocks + (flag ^ 1) :bucket_no + (flag ^ 1) ]  + 1
                else:
                    if self.is_stealing_mode and (game[1][min(bucket_no + rocks - (1 ^ flag), 5)] == 0):
                        game[current][min(bucket_no + rocks - (1 ^ flag), 5)] = -1
                        game_state.scores[player_no] = game_state.scores[player_no] + game[0][min(bucket_no + rocks - (1 ^ flag), 5)] + 1
                        game[0][min(bucket_no + rocks - (1 ^ flag), 5)] = 0
                    game[current][bucket_no+ (flag) :min(bucket_no + rocks + (flag), 6) ] = game[current][bucket_no+ (flag) :min(bucket_no + rocks + (flag), 6) ] + 1
                rocks = 0
            flag = 0
        if player_no == 0:
            game = np.flip(game, (0, 1))
        if np.sum(game[1]) == 0 or np.sum(game[0]) == 0:
            game_state.scores[player_no] += np.sum(game[player_no])
            game_state.scores[player_no ^ 1] += np.sum(game[player_no ^ 1])
            game =np.array([[0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0]])
        game_state.board = game
        return game_state # Return a new 2D-Array (Game State) after simulating a single move


    def __get_possible_moves(self, board_state, max_player, depth):
        updated_states = []
        player_turn = max_player ^ 1
        # Xnor 
        #-----------------------------------
        #  player |  max_player  | results |
        #    0    |      0       |    1    |        
        #    0    |      1       |    0    |
        #    1    |      0       |    0    |
        #    1    |      1       |    1    |
        #-----------------------------------

        state_ = board_state.board[player_turn]
        # print("---------------------------------------------------------------------")
        # print("PARENT BOARD : ", board_state.board)
        # print("---------------------------------------------------------------------")
        for i in range(6):
            index = abs((i % 6) + (- 5) * (player_turn ^ 1))
            # index = i
            if state_[i] > 0:
                # print("---------------------------------------------------------------------")
                # print("Player turn ", player_turn, ", Next Move ", index, " State ", state_, " item ", state_[index])
                if depth == self.difficulty:
                    board_state.last_played_move = index
                next_move = self.__simulate_move(index, player_turn, board_state)
                # print(next_move.board, ", Last Move : ", next_move.last_played_move, "\n")
                updated_states.append(next_move) # return a new state 
                # print("---------------------------------------------------------------------")
        # ex of the possible returned moves: [[4, 4, 5, 6, 1, 4], [4, 4, 5, 6, 1, 4], [4, 4, 5, 6, 1, 4]]
        return updated_states


    def __get_score_value(self, state, maximizingPlayer):
        mancala1 = (state.scores[maximizingPlayer^self.no] + np.sum(state.board[maximizingPlayer^self.no]))
        mancala2 = (state.scores[maximizingPlayer^self.no^1] + np.sum(state.board[maximizingPlayer^self.no^1]))
        if maximizingPlayer:
            score = mancala1 - mancala2
        else:
            score = mancala2 - mancala1
        # print("IT IS SCORE TIME, Last Move", state.last_played_move, " MODE ", maximizingPlayer, " SCORE  ", score)
        return score
    

    def __is_terminal_state(self, board, max_player):
        if np.sum(board) > 0:
            return False
        else:
            return True


    def __mini_max(self, state, depth, alpha, beta, max_player):
        if depth == 0 or self.__is_terminal_state(state.board, 1):
            return self.__get_score_value(state, max_player), state.last_played_move
    
        state_childs = self.__get_possible_moves(state, max_player, depth)
        
        if max_player:
            max_val = -np.inf
            best_move = -1
            for child in state_childs:
                val, last_played_move =  self.__mini_max(child, depth - 1, alpha, beta, 0)
                if val > max_val:
                    max_val = val
                    best_move = last_played_move    

                alpha = max(val, alpha)   
                if beta <= alpha:
                    break
            return max_val, best_move

        else:
            min_val = np.inf
            best_move = 6
            for child in state_childs:
                val, last_played_move = self.__mini_max(child, depth - 1, alpha, beta, 1)

                if val < min_val:
                    # print("IT IS Compare TIME, Last Move", last_played_move, " MODE MINIMIZing", " BEFORE ", best_val,  " SCORE  ", val)
                    min_val = val
                    best_move = last_played_move

                beta = min(val, beta)
                if beta <= alpha:
                    break
        
            return min_val, best_move


    def predict(self, board, depth):
        self.difficulty = depth
        best_val, final_move = self.__mini_max(board, depth, -np.inf, np.inf, 1)
        # print("best_val ", best_val, " final_move ", final_move)
        return final_move