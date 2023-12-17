from typing import List
import os


class AlmanacData:
    def __init__(self):
        self.seeds = []
        self.seed_to_soil = {}
        self.soil_to_fertilizer = {}
        self.fertilizer_to_water = {}
        self.water_to_light = {}
        self.light_to_temperature = {}
        self.temperature_to_humidity = {}
        self.humidity_to_location = {}

    def load_data(self, data: list):
        current_map = None
        for line in data:
            if line.startswith("seeds:"):
                self.seeds = list(map(int, line.split(":")[1].strip().split()))
            elif line.endswith("map:"):
                current_map = self._get_map_by_name(line.split(":")[0])
                assert current_map is not None
            elif line and current_map is not None:
                dest_start, src_start, length = map(int, line.split())
                for i in range(length):
                    current_map[src_start + i] = dest_start + i

    def _get_map_by_name(self, name: str):
        return {
            "seed-to-soil map": self.seed_to_soil,
            "soil-to-fertilizer map": self.soil_to_fertilizer,
            "fertilizer-to-water map": self.fertilizer_to_water,
            "water-to-light map": self.water_to_light,
            "light-to-temperature map": self.light_to_temperature,
            "temperature-to-humidity map": self.temperature_to_humidity,
            "humidity-to-location map": self.humidity_to_location,
        }.get(name, None)

    def get_location_for_seed(self, seed: int) -> int:
        soil = self.map_number(seed, self.seed_to_soil)
        fertilizer = self.map_number(soil, self.soil_to_fertilizer)
        water = self.map_number(fertilizer, self.fertilizer_to_water)
        light = self.map_number(water, self.water_to_light)
        temperature = self.map_number(light, self.light_to_temperature)
        humidity = self.map_number(temperature, self.temperature_to_humidity)
        location = self.map_number(humidity, self.humidity_to_location)
        return location

    def map_number(self, number: int, mapping: dict) -> int:
        # If the number is in the mapping, return the mapped number
        # Otherwise, return the number itself
        return mapping.get(number, number)


def get_lowest_location_number(data: list) -> int:
    almanac = AlmanacData()
    almanac.load_data(data)

    seed_locations = []
    for seed in almanac.seeds:
        location = almanac.get_location_for_seed(seed)
        seed_locations.append(location)

    return min(seed_locations)

    # Implementation of processing seeds to find the lowest location number
    # ...


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
