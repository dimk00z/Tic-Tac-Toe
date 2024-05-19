"""Simple tic-tac-toe game."""

import random
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import Literal


class CellIsNotEmptyError(Exception):
    "Cell is not empty."


PLAYERS_VALUES = ("X", "O")


@dataclass
class Board:
    "Simple tic-tac-toe board."

    _board: list[list[str]] = field(init=False)

    def __post_init__(self):
        self._board = [[" " for _ in range(3)] for _ in range(3)]

    def is_full(self) -> bool:
        "Check if the board is full."
        return all(
            (
                all(
                    (spot != " " for spot in row),
                )
                for row in self._board
            ),
        )

    def is_cell_empty(self, row, col) -> bool:
        "Check if the cell is empty."
        check_result = self._board[row][col] == " "
        if not check_result:
            print("Эта клетка уже занята.")
        return check_result

    def get_empty_spots(self) -> list[tuple[int, int]]:
        "Get all empty spots on the board."
        return [(i, j) for i in range(3) for j in range(3) if self._board[i][j] == " "]

    def __str__(self) -> str:
        return "\n".join(
            [
                "\n".join(
                    (
                        " | ".join(row),
                        "-" * 5,
                    )
                )
                for row in self._board
            ],
        )

    def set_cell_value(self, row, col, value) -> tuple[int, int]:
        "Set the value of a cell."
        if not self.is_cell_empty(row, col):
            raise CellIsNotEmptyError("Эта клетка уже занята.")
        self._board[row][col] = value
        return row, col

    def check_winner(self, player_value: str):
        "Check if the player has won the game."
        for i in range(3):
            if all((spot == player_value for spot in self._board[i])):
                return True
            if all((self._board[j][i] == player_value for j in range(3))):
                return True
        if (
            self._board[0][0] == player_value
            and self._board[1][1] == player_value
            and self._board[2][2] == player_value
        ):
            return True
        if (
            self._board[0][2] == player_value
            and self._board[1][1] == player_value
            and self._board[2][0] == player_value
        ):
            return True
        return False


@dataclass(slots=True, frozen=True)
class BasePlayer(metaclass=ABCMeta):
    """Abstract base class for players."""

    value: str

    @abstractmethod
    def move(self, board: Board) -> tuple[int, int]:
        "Move the player."
        raise NotImplementedError("Необходимо переопределить метод move()")


class Player(BasePlayer):
    "Simple player class."

    def move(self, board: Board) -> tuple[int, int]:
        "Get user move."
        message = "Введите координаты вашего хода (строка и столбец через пробел, от 0 до 2): "
        while True:
            try:
                row, col = map(
                    int,
                    input(message).split(),
                )
            except (ValueError, IndexError):
                print("Некорректный ввод. Пожалуйста, введите два числа от 0 до 2.")
            if not board.is_cell_empty(row, col):
                continue
            return row, col


class CPUPlayer(BasePlayer):
    "Simple CPU player class."

    def move(self, board: Board) -> tuple[int, int]:
        "Get CPU move."
        empty_spots = board.get_empty_spots()
        row, col = random.choice(empty_spots)
        print(f"Компьютер делает ход: {row} {col}")

        return row, col


def get_shuffled_players() -> list[Literal["X", "O"]]:
    "Get shuffled players."
    players = list(PLAYERS_VALUES)
    random.shuffle(players)
    return players


def main():
    "Main function."
    shuffled_values = get_shuffled_players()
    random.shuffle(shuffled_values)

    human_player: Player = Player(value=shuffled_values[0])
    cpu_player: CPUPlayer = CPUPlayer(value=shuffled_values[1])

    current_player = human_player if human_player.value == "X" else cpu_player

    print(f"Первый ход делает: {current_player}")

    board = Board()
    print(board)

    while True:
        row, col = current_player.move(board)
        board.set_cell_value(row, col, current_player.value)
        print(board)

        if board.check_winner(current_player.value):
            print(f"Игрок {current_player} выиграл!")
            break

        if board.is_full():
            print("Ничья!")
            break

        current_player = (
            human_player if isinstance(current_player, CPUPlayer) else cpu_player
        )


if __name__ == "__main__":
    main()
