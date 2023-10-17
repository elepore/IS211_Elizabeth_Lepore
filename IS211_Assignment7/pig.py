
import argparse

parser = argparse.ArgumentParser(description='Play the Pig game with a configurable number of players.')
parser.add_argument('--numPlayers', type=int, default=2, help='Number of players in the game. Default is 2.')
args = parser.parse_args()

import random

class Die:
    def __init__(self):
        self.seed = 0
        random.seed(self.seed)
    
    def roll(self):
        return random.randint(1, 6)

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn_total = 0
    
    def add_to_score(self, points):
        self.score += points
    
    def reset_turn_total(self):
        self.turn_total = 0

class Game:
    
    def __init__(self, num_players=2, mode='auto'):
        self.players = [Player(f"Player {i + 1}") for i in range(num_players)]
        self.current_player_index = 0
        self.die = Die()
        self.mode = mode

    @property
    def current_player(self):
        return self.players[self.current_player_index]
    
    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    def reset_game(self):
        for player in self.players:
            player.score = 0
        self.current_player_index = 0

    
    def player_decision(self):
        if self.mode == 'auto':
            if self.current_player.turn_total < 20 and (self.current_player.score + self.current_player.turn_total) < 100:
                return 'r'
            else:
                return 'h'
        elif self.mode == 'manual':
            while True:
                decision = input(f"{self.current_player.name}, would you like to (r)oll or (h)old? ").lower()
                if decision in ['r', 'h']:
                    return decision
                else:
                    print("Invalid input. Please enter 'r' for roll or 'h' for hold.")

    def play_turn(self):
        self.current_player.reset_turn_total()
        
        while True:
            roll = self.die.roll()
            
            if roll == 1:
                print(f"{self.current_player.name} rolled a 1. No points added. Turn over.")
                self.switch_player()
                return
            else:
                self.current_player.turn_total += roll
                print(f"{self.current_player.name} rolled a {roll}. Turn total: {self.current_player.turn_total}. Game score: {self.current_player.score}.")
                
                decision = self.player_decision()
                if decision == 'h':
                    self.current_player.add_to_score(self.current_player.turn_total)
                    print(f"{self.current_player.name} adds {self.current_player.turn_total} to their score. New score: {self.current_player.score}.")
                    self.switch_player()
                    return
    
    def play(self):
        while all(player.score < 100 for player in self.players):
            self.play_turn()
        
        winner = max(self.players, key=lambda x: x.score)
        print(f"{winner.name} wins with a score of {winner.score}!")
        self.reset_game()

if __name__ == "__main__":
    game = Game(num_players=args.numPlayers, mode='manual')
    num_games = int(input("How many games would you like to play? "))

    for _ in range(num_games):
        print("\nStarting a new game...\n")
        game.play()
