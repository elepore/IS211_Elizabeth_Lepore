import argparse
import random
import time

parser = argparse.ArgumentParser(description='Play the Pig game with various configurations.')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--players', type=str, nargs='+', choices=['human', 'computer'], help='List of players in order. E.g., --players human computer human.')
group.add_argument('--player1', type=str, choices=['human', 'computer'], help='Type for Player 1 (either "human" or "computer").')
parser.add_argument('--player2', type=str, choices=['human', 'computer'], help='Type for Player 2 (either "human" or "computer"). Only used if --player1 is specified.')
parser.add_argument('--timed', action='store_true', help='Activate the timed version of the game.')
args = parser.parse_args()

if args.player1 and args.player2:
    players_list = [args.player1, args.player2]
elif args.players:
    players_list = args.players
else:
    raise ValueError("Either --players or both --player1 and --player2 must be provided.")

# Example Use:

# python pig.py
# Description: Default two humans.

# python pig.py --players human computer human
# Description: Two humans one computer

# python pig.py --player1 human --player2 computer
# Description: One human one computer

# python pig.py --players human computer computer --timed
# Description: Timed game, one human two computers

# python pig.py --player1 human --player2 computer --timed
# Description: Timed game, one human one computer


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

class ComputerPlayer(Player):
    def decision(self):
        threshold = min(25, 100 - self.score)
        if self.turn_total < threshold:
            return 'r'
        else:
            return 'h'

class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return Player(name)
        elif player_type == "computer":
            return ComputerPlayer(name)

class Game:
    def __init__(self, players_list):
        self.players = [PlayerFactory.create_player(player_type, f"Player {i+1}") for i, player_type in enumerate(players_list)]
        self.current_player_index = 0
        self.die = Die()

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
        if isinstance(self.current_player, ComputerPlayer):
            return self.current_player.decision()
        else:
            while True:
                decision = input(f"{self.current_player.name}, would you like to (r)oll or (h)old? ").lower()
                if decision in ['r', 'h']:
                    return decision

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

class TimedGameProxy:
    def __init__(self, players_list):
        self.game = Game(players_list)
        self.start_time = None

    def play_turn(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= 60:
            winner = max(self.game.players, key=lambda x: x.score)
            print(f"Time's up! {winner.name} wins with a score of {winner.score}!")
            self.game.reset_game()
            return True
        return self.game.play_turn()

    def play(self):
        self.start_time = time.time()
        while all(player.score < 100 for player in self.game.players):
            game_ended = self.play_turn()
            if game_ended:
                break
        else:
            winner = max(self.game.players, key=lambda x: x.score)
            print(f"{winner.name} wins with a score of {winner.score}!")
            self.game.reset_game()

if __name__ == "__main__":
    if args.timed:
        game = TimedGameProxy(players_list=players_list)
    else:
        game = Game(players_list=players_list)
    
    num_games = int(input("How many games would you like to play? "))
    for _ in range(num_games):
        game.play()