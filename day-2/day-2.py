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
    # 12 red cubes, 13 green cubes, and 14 blue cubes
    REDS = 12
    GREENS = 13
    BLUES = 14 

    # Variables to track the total number of each color required by the game
    total_reds = 0
    total_greens = 0
    total_blues = 0

    # Split the string into parts and iterate over them
    parts = game.split()
    for i, part in enumerate(parts):
        if part.isdigit() and i + 1 < len(parts):
            # Convert the number and check the next part for the color
            number = int(part)
            color = parts[i + 1].lower()

            if 'red' in color:
                total_reds += number
            elif 'green' in color:
                total_greens += number
            elif 'blue' in color:
                total_blues += number

    # Check if the game is possible with the available cubes
    return total_reds <= REDS and total_greens <= GREENS and total_blues <= BLUES


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