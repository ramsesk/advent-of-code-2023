import os
from typing import List

def readlines_from_file(file_path: str) -> List[str]:
    assert(os.path.exists(file_path))

    lines = []
    with open(file_path) as f:
        lines = f.readlines()
    
    assert len(lines) > 0

    return lines

def sum_of_all_gear_ratios(engine_diagram: List[str]) -> int:
    GEAR_SYMBOL = '*'
    total_sum = 0

    # Helper function to find start and end indices of a number in a row
    def find_number_indices(row, start_index):
        end_index = start_index
        while end_index < len(row) and row[end_index].isdigit():
            end_index += 1
        return start_index, end_index - 1

    # Helper function to find start and end indices of a number in a row
    def find_complete_number(row, index):
        # Find the start of the number
        start_index = index
        while start_index > 0 and row[start_index - 1].isdigit():
            start_index -= 1

        # Find the end of the number
        end_index = index
        while end_index < len(row) - 1 and row[end_index + 1].isdigit():
            end_index += 1

        # Return the complete number
        return int(row[start_index:end_index + 1])
    
    # Function to find all adjacent numbers to a particular index
    def find_adjacent_numbers(row_index, col_index):
        adjacent_numbers = []
        processed_indices = set()
        for x in range(row_index - 1, row_index + 2):
            for y in range(col_index - 1, col_index + 2):
                if 0 <= x < len(engine_diagram) and 0 <= y < len(engine_diagram[x]) and (x, y) not in processed_indices:
                    char = engine_diagram[x][y]
                    if char.isdigit():
                        number = find_complete_number(engine_diagram[x], y)
                        start_index, end_index = find_number_indices(engine_diagram[x], y)
                        adjacent_numbers.append(number)
                        
                        # Add all indices of this number to processed_indices to avoid re-processing
                        for i in range(start_index, end_index + 1):
                            processed_indices.add((x, i))
        return adjacent_numbers

    # Loop through each character in the grid
    for i, row in enumerate(engine_diagram):
        for j, char in enumerate(row):
            if char == GEAR_SYMBOL:
                adjacent_numbers = find_adjacent_numbers(i, j)
                # Check if there are exactly two numbers adjacent to '*'
                if len(adjacent_numbers) == 2:
                    total_sum += adjacent_numbers[0] * adjacent_numbers[1]
                else:
                    pass

    return total_sum


def test_example_date():
    example_data = [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ]

    result = sum_of_all_gear_ratios(example_data)

    assert result == 467835


if __name__ == "__main__":
    test_example_date()
    
    py_file_path = os.path.dirname(__file__)
    puzzle_doc_path = os.path.join(py_file_path, "puzzle_input.txt")

    puzzle_lines = readlines_from_file(puzzle_doc_path)

    result = sum_of_all_gear_ratios(puzzle_lines)
    print(result)