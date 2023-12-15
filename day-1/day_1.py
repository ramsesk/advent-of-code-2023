from typing import List

example_data = {
    "1abc2": 12,
    "pqr3stu8vwx": 38,
    "a1b2c3d4e5f": 15,
    "treb7uchet": 77
}

def test_example_data():
    total_calibration_value = calibrate_text(example_data.keys)

    assert total_calibration_value == 142

def calibrate_line(line: str):
    return 0

def calibrate_text(calibration_lines: List[str]):
    total_calibration_value = 0
    for line in calibration_lines:
        calibration_value = calibrate_line(line)
        total_calibration_value += calibration_value

    return calibration_value

if __name__ == "__main__":
    test_example_data()