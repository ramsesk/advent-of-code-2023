from typing import List
import os

example_data = {
    "1abc2": 12,
    "pqr3stu8vwx": 38,
    "a1b2c3d4e5f": 15,
    "treb7uchet": 77
}

def test_example_data():
    total_calibration_value = calibrate_text(example_data.keys())

    assert total_calibration_value == 142

def calibrate_line(line: str):
    first_integer = None
    last_integer = None

    for char in line:
        if char.isdigit():
            if first_integer is None:
                first_integer = char
            
            last_integer = char

    
    # Combine the integers if both are found
    if first_integer is not None and last_integer is not None:
        return int(f"{first_integer}{last_integer}")
    else:
        return 0  # Return 0 if no integers are found in the string


    return 0

def calibrate_text(calibration_lines: List[str]):
    total_calibration_value = 0
    for line in calibration_lines:
        calibration_value = calibrate_line(line)
        total_calibration_value += calibration_value

    return total_calibration_value

if __name__ == "__main__":
    test_example_data()

    py_file_path = os.path.dirname(__file__)
    calibration_doc_path = os.path.join(py_file_path, "calibrationdoc.txt")

    assert(os.path.exists(calibration_doc_path))

    calibration_lines = []
    with open(calibration_doc_path) as f:
        calibration_lines = f.readlines()
    
    assert len(calibration_lines) > 0

    calibration_value = calibrate_text(calibration_lines)

    print(calibration_value)
