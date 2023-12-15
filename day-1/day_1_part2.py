
from typing import List
import os

example_data = [
    "two1nine",
    "eightwothree",
    "abcone2threexyz",
    "xtwone3four",
    "4nineeightseven2",
    "zoneight234",
    "7pqrstsixteen"
]

def calibrate_line_part2(line: str):
    def text_to_number(text):
        mapping = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9
        }
        return mapping.get(text.lower())

    def find_number_from_index(s, index):
        current_text = ""
        for char in s[index:]:
            current_text += char
            number = text_to_number(current_text)
            if number is not None:
                return number
        return None
    
    first_integer = None
    last_integer = None

    for i in range(len(line)):
        if line[i].isalpha():
            number = find_number_from_index(line, i)
            if number is not None:
                if first_integer is None:
                    first_integer = number
                last_integer = number
        elif line[i].isdigit():
            if first_integer is None:
                first_integer = int(line[i])
            last_integer = int(line[i])

    # Combine the integers if both are found
    if first_integer is not None and last_integer is not None:
        return int(f"{first_integer}{last_integer}")
    else:
        return 0  # Return 0 if no integers are found in the string


def calibrate_text(calibration_lines: List[str]):
    total_calibration_value = 0
    for line in calibration_lines:
        calibration_value = calibrate_line_part2(line)
        total_calibration_value += calibration_value

    return total_calibration_value

def test_example_data_part2():
    calibration_value = calibrate_text(example_data)
    assert calibration_value == 281



if __name__ == "__main__":
    test_example_data_part2()

    py_file_path = os.path.dirname(__file__)
    calibration_doc_path = os.path.join(py_file_path, "calibrationdoc.txt")

    assert(os.path.exists(calibration_doc_path))

    calibration_lines = []
    with open(calibration_doc_path) as f:
        calibration_lines = f.readlines()
    
    assert len(calibration_lines) > 0

    calibration_value = calibrate_text(calibration_lines)

    print(calibration_value)