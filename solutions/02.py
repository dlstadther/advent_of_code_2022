from pathlib import Path

filepath = Path(__file__).resolve()
filename_no_ext = filepath.name.split('.')[0]
filedir = filepath.parent
input_file = filedir / f"../inputs/{filename_no_ext}.txt"


class Choice:
    def __init__(self, value):
        self.value = value
        self._wins_against = None
        self._loses_against = None

    @property
    def wins_against(self):
        return self._wins_against

    @property
    def loses_against(self):
        return self._loses_against

    @wins_against.setter
    def wins_against(self, choice):
        self._wins_against = choice

    @loses_against.setter
    def loses_against(self, choice):
        self._loses_against = choice


class RockPaperScissors:
    def __init__(self):
        rock = Choice(value=1)
        paper = Choice(value=2)
        scissors = Choice(value=3)

        rock.wins_against = scissors
        rock.loses_against = paper
        paper.wins_against = rock
        paper.loses_against = scissors
        scissors.wins_against = paper
        scissors.loses_against = rock

        self.round_1_key = {"A": rock, "B": paper, "C": scissors,
                            "X": rock, "Y": paper, "Z": scissors}
        self.round_2_key = {"A": rock, "B": paper, "C": scissors,
                            "X": "lose", "Y": "draw", "Z": "win"}

        self.score = 0

    def score_round(self, player_1_choice: Choice, player_2_choice: Choice):
        did_draw = player_1_choice == player_2_choice
        did_win = player_2_choice.wins_against == player_1_choice
        result_pts = 0
        if did_win:
            result_pts = 6
        elif did_draw:
            result_pts = 3
        choice_pts = player_2_choice.value
        round_score = result_pts + choice_pts
        self.score += round_score

    @staticmethod
    def pick_choice(player_1_choice: Choice, round_result: str) -> Choice:
        if round_result == "win":
            player_2_choice = player_1_choice.loses_against
        elif round_result == "lose":
            player_2_choice = player_1_choice.wins_against
        elif round_result == "draw":
            player_2_choice = player_1_choice
        else:
            raise ValueError(f"Unexpected round_result value; received '{round_result}'")
        return player_2_choice

    def play_round_1(self, player_1_input: str, player_2_input: str) -> None:
        player_1_choice: Choice = self.round_1_key[player_1_input]
        player_2_choice: Choice = self.round_1_key[player_2_input]
        self.score_round(player_1_choice=player_1_choice, player_2_choice=player_2_choice)

    def play_round_2(self, player_1_input: str, player_2_input: str) -> None:
        player_1_choice: Choice = self.round_2_key[player_1_input]
        round_result: str = self.round_2_key[player_2_input]
        player_2_choice: Choice = self.pick_choice(player_1_choice=player_1_choice, round_result=round_result)
        self.score_round(player_1_choice=player_1_choice, player_2_choice=player_2_choice)


if __name__ == "__main__":
    game_1 = RockPaperScissors()
    game_2 = RockPaperScissors()
    with open(input_file, "r") as infile:
        for line in infile:
            line = line.strip()
            if line is None:
                continue
            input_elf, input_me = line.split()
            game_1.play_round_1(player_1_input=input_elf, player_2_input=input_me)
            game_2.play_round_2(player_1_input=input_elf, player_2_input=input_me)
    print(game_1.score)  # 13446 - correct
    print(game_2.score)  # 13509 - correct
