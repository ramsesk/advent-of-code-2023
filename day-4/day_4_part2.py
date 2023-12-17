from typing import List
import os


def readlines_from_file(file_path: str) -> List[str]:
    assert os.path.exists(file_path)

    lines = []
    with open(file_path) as f:
        lines = f.readlines()

    assert len(lines) > 0

    return lines


def calculate_scratchcard_matches(card_numbers: str) -> int:
    winning_numbers_str, players_numbers_str = card_numbers.split("|")
    # Convert the strings to sets of integers
    winning_numbers = set(map(int, winning_numbers_str.split()))
    players_numbers = set(map(int, players_numbers_str.split()))

    # Find the intersection (matches) between the two sets
    matches = winning_numbers.intersection(players_numbers)

    return len(matches)


# def calculate_scratchcards_copies(cards: List[str]) -> int:
#     total_points = 0

#     # gamenumber , matches
#     matches_per_card = {}

#     for card in cards:
#         game_number_string, numbers_string = card.split(":")
#         game_number = int(game_number_string.split()[1])
#         matches = calculate_scratchcard_matches(numbers_string)
#         matches_per_card[game_number] = matches

#     # if a card has 5 matches, it will add one extra card for the next 5 cards in the list
#     # never going outside of the list (matches outside of the list are ignored)
#     copies_per_card = {(game_number, 1) for game_number, matches in matches_per_card}
#     for game_number, matches in matches_per_card.items:
#         pass

#     return total_points


def calculate_scratchcards_copies(cards: List[str]) -> int:
    # gamenumber, matches
    matches_per_card = {}

    # Populate matches_per_card with the number of matches for each card
    for card in cards:
        game_number_string, numbers_string = card.split(":")
        # split()[0] necessary because game_number_string = "Game 12"
        game_number = int(game_number_string.split()[1])
        matches = calculate_scratchcard_matches(numbers_string)
        matches_per_card[game_number] = matches

    # Initialize copies_per_card with 1 copy for each card
    copies_per_card = {game_number: 1 for game_number in matches_per_card}

    # Add extra copies for the matches
    for game_number, matches in matches_per_card.items():
        current_card_copies = copies_per_card[game_number]
        for next_card in range(game_number + 1, game_number + matches + 1):
            if next_card in copies_per_card:
                copies_per_card[next_card] += current_card_copies

    # Sum the total copies
    total_copies = sum(copies_per_card.values())

    return total_copies


def test_example_data():
    example_data = [
        "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
        "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
        "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
        "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
        "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
        "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
    ]

    result = calculate_scratchcards_copies(example_data)

    assert result == 30


if __name__ == "__main__":
    test_example_data()

    py_file_path = os.path.dirname(__file__)
    puzzle_doc_path = os.path.join(py_file_path, "puzzle_input.txt")

    puzzle_lines = readlines_from_file(puzzle_doc_path)

    result = calculate_scratchcards_copies(puzzle_lines)
    print(result)
