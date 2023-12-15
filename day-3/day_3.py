import os
from typing import List

def readlines_from_file(file_path: str) -> List[str]:
    assert(os.path.exists(file_path))

    lines = []
    with open(file_path) as f:
        lines = f.readlines()
    
    assert len(lines) > 0

    return lines

def sum_of_all_engine_parts(engine_diagram: List[str]) -> int:
    SPECIAL_SYMBOLS = {'*', '#', '+', '$', '&', '/', '@', '-', '%', '=', '+'}
    total_sum = 0

    # Helper function to find start and end indices of a number in a row
    def find_number_indices(row, start_index):
        end_index = start_index
        while end_index < len(row) and row[end_index].isdigit():
            end_index += 1
        return start_index, end_index - 1
    
    # Function to get adjacent indices for a range (start_index, end_index) in a row
    def get_adjacent_indices(row_index, start_index, end_index):
        adjacent_indices = []
        for i in range(start_index, end_index + 1):
            for x in range(row_index - 1, row_index + 2):
                for y in range(i - 1, i + 2):
                    if 0 <= x < len(engine_diagram) and 0 <= y < len(engine_diagram[row_index]) and not (x == row_index and y == i):
                        adjacent_indices.append((x, y))
        return adjacent_indices

    # Loop through each character in the grid
    for i, row in enumerate(engine_diagram):
        j = 0
        while j < len(row):
            if row[j].isdigit():
                # Identify the complete number
                start_index, end_index = find_number_indices(row, j)
                number = int(row[start_index:end_index + 1])
                # Generate indices for all adjacent cells of the number
                adjacent_indices = get_adjacent_indices(i, start_index, end_index)
                # Check for special symbols in adjacent cells
                if any(engine_diagram[x][y] in SPECIAL_SYMBOLS for x, y in adjacent_indices):
                    total_sum += number
                else:
                    message = f"Number is not part of the total_sum: {number}"

                # Skip to the end of the current number
                j = end_index + 1
            else:
                j += 1

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

    result = sum_of_all_engine_parts(example_data)

    assert result == 4361


if __name__ == "__main__":
    test_example_date()
    
    py_file_path = os.path.dirname(__file__)
    puzzle_doc_path = os.path.join(py_file_path, "puzzle_input.txt")

    puzzle_lines = readlines_from_file(puzzle_doc_path)

    result = sum_of_all_engine_parts(puzzle_lines)
    print(result)