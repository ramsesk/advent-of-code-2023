import os
from typing import List

def get_game_id(game: str) -> int:
    # Split the string by spaces and grab the second element (index 1)
    # which should be the number following "Game"
    parts = game.split()
    if len(parts) > 1 and parts[0].lower() == "game":
        # Convert the game number to an integer and return it
        game_number = parts[1].split(":")[0]
        return int(game_number)
    
    else:
        return -1

def game_is_possible(game: str) -> bool:
    REDS = 12
    GREENS = 13
    BLUES = 14

    # Split the game string into sets
    sets = game.split(';')
    
    max_reds, max_greens, max_blues = 0, 0, 0

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
                elif 'green' in color :
                    current_greens += number
                elif 'blue' in color:
                    current_blues += number
                else:
                    pass # something went wrong 

        # Update max counts if current set has more
        max_reds = max(max_reds, current_reds)
        max_greens = max(max_greens, current_greens)
        max_blues = max(max_blues, current_blues)

    # Check if the game is possible with the available cubes
    return max_reds <= REDS and max_greens <= GREENS and max_blues <= BLUES

# Test with a sample game string
print(game_is_possible("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"))  # Test output



def sum_ids_possible_games(game_list: List[str]) -> int:
    result = 0
    for game in game_list:
        if (game_is_possible(game)):
            result += get_game_id(game)

    return result

def test_example_data():
    example_data = [
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
    ]

    result = sum_ids_possible_games(example_data)

    assert result == 8

    

if __name__ == "__main__":
    test_example_data()

    
    py_file_path = os.path.dirname(__file__)
    puzzle_doc_path = os.path.join(py_file_path, "puzzle_input.txt")

    assert(os.path.exists(puzzle_doc_path))

    puzzle_lines = []
    with open(puzzle_doc_path) as f:
        puzzle_lines = f.readlines()
    
    assert len(puzzle_lines) > 0

    result = sum_ids_possible_games(puzzle_lines)

    print(result)