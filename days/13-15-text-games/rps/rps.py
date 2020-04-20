from random import randint
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
from csv import DictReader


class Roll:
    def __init__(self, name: str, strong: List[str], weak: List[str]) -> None:
        self.name: str = name
        self.strong: List[str] = strong
        self.weak: List[str] = weak

    def can_defeat(self, roll: 'Roll') -> Optional['Roll']:
        if roll.name in self.strong:
            return roll
        elif roll.name in self.weak:
            return self
        return None


class Player:
    def __init__(self, name: str) -> None:
        self.name = name


def print_header(name: str) -> None:
    print("-----------------------------")
    print("        Rock Paper Scisor")
    print("-----------------------------")
    print("        Player: {}".format(name))
    print()
    print()


def get_players_name() -> str:
    name = input("Please enter your name: ")
    return name


def get_player_roll(rolls: List[Roll]) -> Roll:
    while True:
        roll_name = input("Get roll name: ").strip().lower()
        for roll in rolls:
            if roll_name == roll.name:
                return roll
        print("Roll {} doesn't exist".format(roll_name))
        print("Please pick in the following list:")
        for roll in rolls:
            print("* {}".format(roll.name))


def game_loop(player1: Player, player2: Player, rolls: List[Roll]) -> None:
    max_count = 3
    count = 0
    scores: Dict[Player, int] = defaultdict(int)
    while count < max_count:
        p2_roll = rolls[randint(0, len(rolls)-1)]
        p1_roll = get_player_roll(rolls)

        outcome = p1_roll.can_defeat(p2_roll)

        print("count {}".format(count))
        if outcome is None:
            print("Nobody won, both players played {}".format(p1_roll.name))
            continue

        if outcome is p1_roll:
            won_turn = player1
        else:
            won_turn = player2

        print("{} played {}".format(player1.name, p1_roll.name))
        print("{} played {}".format(player2.name, p2_roll.name))
        print("{} won turn".format(won_turn.name))

        scores[won_turn] += 1
        count += 1
        if float(scores[won_turn]) > (max_count/2.0):
            break

    winner: Tuple[Player, int] = (player1, scores[player1])
    for player, score in scores.items():
        if score > winner[1]:
            winner = (player, score)

    print("WINNER IS: {} with {} points".format(winner[0].name, winner[1]))


def read_rolls() -> List[Roll]:
    rolls = []
    with open('battle-table.csv') as fin:
        reader = DictReader(fin)
        for row in reader:
            rolls.append(read_roll(row))
    return rolls


def read_roll(row: dict) -> Roll:
    name = row['Attacker']
    del row['Attacker']
    del row[name]

    lose = []
    win = []
    for k in row.keys():
        outcome = row[k].strip().lower()
        roll = k.strip().lower()
        if outcome == 'win':
            win.append(roll)
        else:
            lose.append(roll)

    print("{} win: {} lose: {}".format(name, win, lose))
    return Roll(name.strip().lower(), win, lose)


def main() -> None:
    name = get_players_name()
    player1 = Player(name)
    player2 = Player("computer")

    print_header(player1.name)

    rolls = read_rolls()

    game_loop(player1, player2, rolls)


if __name__ == '__main__':
    main()
