import os
from typing import List, Tuple

def minimum_necessary_balls(game: str) -> Tuple[int, int, int]:
    # Split the game string into sets
    sets = game.split(';')

    # Initialize the minimum requirements to 0
    min_reds, min_greens, min_blues = 0, 0, 0

    for set in sets:
        # Initialize counts for the current set
        current_reds, current_greens, current_blues = 0, 0, 0

        parts = set.split()
        for i, part in enumerate(parts):
            if part.isdigit() and i + 1 < len(parts):
                number = int(part)
                color = parts[i + 1].lower()

                if 'red' in color:
                    current_reds += number
                elif 'green' in color:
                    current_greens += number
                elif 'blue' in color:
                    current_blues += number

        # Update minimum requirements if the current set has more
        min_reds = max(min_reds, current_reds)
        min_greens = max(min_greens, current_greens)
        min_blues = max(min_blues, current_blues)

    return min_reds, min_greens, min_blues


def product_of_minimum_balls(game_list: List[str]) -> int:
    result = 0
    for game in game_list:
        red, green, blue = minimum_necessary_balls(game)
        result += red * green * blue

    return result

def test_example_data():
    example_data = [
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
    ]

    result = product_of_minimum_balls(example_data)

    assert result == 2286

    

if __name__ == "__main__":
    test_example_data()

    
    py_file_path = os.path.dirname(__file__)
    puzzle_doc_path = os.path.join(py_file_path, "puzzle_input.txt")

    assert(os.path.exists(puzzle_doc_path))

    puzzle_lines = []
    with open(puzzle_doc_path) as f:
        puzzle_lines = f.readlines()
    
    assert len(puzzle_lines) > 0

    result = product_of_minimum_balls(puzzle_lines)

    print(result)