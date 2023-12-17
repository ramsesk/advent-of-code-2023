from typing import List
import os

class AlmanacData:
    def __init__(self):
        self.seeds = []
        self.seed_to_soil = []
        self.soil_to_fertilizer = []
        self.fertilizer_to_water = []
        self.water_to_light = []
        self.light_to_temperature = []
        self.temperature_to_humidity = []
        self.humidity_to_location = []

    def load_data(self, data: list):
        # TODO: Implement this method to parse 'data' and fill the class attributes

    def map_number(self, number: int, mapping: list) -> int:
        # TODO: Implement this method to map a number using a given mapping

    def get_location_for_seed(self, seed: int) -> int:
        # TODO: Implement this method to process a seed through all stages to find its location



def get_lowest_location_number(almanac: List[str]):


def test_example_data():
    example_data = [
        "seeds: 79 14 55 13",
        "",
        "seed-to-soil map:",
        "50 98 2",
        "52 50 48",
        "",
        "soil-to-fertilizer map:",
        "0 15 37",
        "37 52 2",
        "39 0 15",
        "",
        "fertilizer-to-water map:",
        "49 53 8",
        "0 11 42",
        "42 0 7",
        "57 7 4",
        "",
        "water-to-light map:",
        "88 18 7",
        "18 25 70",
        "",
        "light-to-temperature map:",
        "45 77 23",
        "81 45 19",
        "68 64 13",
        "",
        "temperature-to-humidity map:",
        "0 69 1",
        "1 0 69",
        "",
        "humidity-to-location map:",
        "60 56 37",
        "56 93 4",
    ]

    result = get_lowest_location_number(example_data)

    assert result == 35


if __name__ == "__main__":
    test_example_data()
