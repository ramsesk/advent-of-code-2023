from typing import List
import os


def readlines_from_file(file_path: str) -> List[str]:
    assert os.path.exists(file_path)

    lines = []
    with open(file_path) as f:
        lines = f.readlines()

    assert len(lines) > 0

    return lines


def calculate_scratchcard(card: str) -> int:
    points = 0

    game_number, numbers_string = card.split(":")
    winning_numbers_str, players_numbers_str = numbers_string.split("|")
    # Convert the strings to sets of integers
    winning_numbers = set(map(int, winning_numbers_str.split()))
    players_numbers = set(map(int, players_numbers_str.split()))

    # Find the intersection (matches) between the two sets
    matches = winning_numbers.intersection(players_numbers)

    if len(matches) == 1:
        points = 1

    if len(matches) > 1:
        points = 2 ** (len(matches) - 1)

    return points


def calculate_scratchcards(cards: List[str]) -> int:
    total_points = 0
    for card in cards:
        total_points += calculate_scratchcard(card)

    return total_points


def test_example_data():
    example_data = [
        "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
        "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
        "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
        "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
        "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
        "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
    ]

    result = calculate_scratchcards(example_data)

    assert result == 13


if __name__ == "__main__":
    test_example_data()

    py_file_path = os.path.dirname(__file__)
    puzzle_doc_path = os.path.join(py_file_path, "puzzle_input.txt")

    puzzle_lines = readlines_from_file(puzzle_doc_path)

    result = calculate_scratchcards(puzzle_lines)
    print(result)
