from typing import List, Tuple, Set
from enum import Enum

class MapTile(Enum):
    PATH = ('.',)
    FOREST = ('#',)
    SLOPE_LEFT = ('<',)
    SLOPE_RIGHT = ('>',)
    SLOPE_DOWN = ('v',)
    SLOPE_UP = ('^',)

    def __init__(self, character) -> None:
        self.character = character

class AdventMap():
    def __init__(self, map_data: List[str]) -> None:
        self.forest_map = self.read_map(map_data)
    

    def read_map(self, map_data: List[str]) -> List[List[MapTile]]:
        tile_map = []
        for row in map_data:
            tile_row = []
            for char in row:
                for tile in MapTile:
                    if char in tile.character:
                        tile_row.append(tile)
                        break
            tile_map.append(tile_row)
        return tile_map

    def print_map(self, path: List[Tuple[int, int]] = None) -> None:
        for x, row in enumerate(self.forest_map):
            row_str = ''
            for y, tile in enumerate(row):
                if path and (x, y) in path:
                    char = 'O' if (x, y) != path[0] else 'S'  # 'S' for start, 'O' for path
                else:
                    char = tile.character
                row_str += char
            print(row_str)
        

class PathFinder:
    def __init__(self, advent_map: AdventMap):
        self.map = advent_map.forest_map
        self.longest_path = []
        self.visited = set()

    def find_longest_path(self) -> List[Tuple[int, int]]:
        start = self.find_start()
        self.dfs(start, [])
        return self.longest_path

    def find_start(self) -> Tuple[int, int]:
        for x, tile in enumerate(self.map[0]):
            if tile == MapTile.PATH:
                return (0, x)
        
        assert 0, "No start found on first row"

    def dfs(self, position: Tuple[int, int], current_path: List[Tuple[int, int]]) -> None:
        x, y = position
        if x < 0 or x >= len(self.map) or y < 0 or y >= len(self.map[0]) or position in self.visited:
            return  # Out of bounds or already visited

        current_path.append(position)
        self.visited.add(position)

        # Check if we've reached the bottom row
        if x == len(self.map) - 1:
            if len(current_path) > len(self.longest_path):
                self.longest_path = list(current_path)
        else:
            # Explore adjacent tiles
            for dx, dy in self.get_possible_moves(x, y):
                self.dfs((x + dx, y + dy), current_path)

        # Backtrack
        current_path.pop()
        self.visited.remove(position)
    
    def get_possible_moves(self, x: int, y: int) -> List[Tuple[int, int]]:
        moves = []
        current_tile = self.map[x][y]

        if current_tile == MapTile.PATH or current_tile == MapTile.FOREST:
            # Can move in any direction
            moves = [(1, 0), (0, 1), (0, -1), (-1, 0)]
        elif current_tile == MapTile.SLOPE_DOWN:
            moves = [(1, 0)]
        elif current_tile == MapTile.SLOPE_UP:
            moves = [(-1, 0)]
        elif current_tile == MapTile.SLOPE_RIGHT:
            moves = [(0, 1)]
        elif current_tile == MapTile.SLOPE_LEFT:
            moves = [(0, -1)]

        # Filter out invalid moves
        valid_moves = []
        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(self.map) and 0 <= new_y < len(self.map[0]):
                valid_moves.append((dx, dy))

        return valid_moves

def test_example_data() -> None:
    example_data = [
        "#.#####################",
        "#.......#########...###",
        "#######.#########.#.###",
        "###.....#.>.>.###.#.###",
        "###v#####.#v#.###.#.###",
        "###.>...#.#.#.....#...#",
        "###v###.#.#.#########.#",
        "###...#.#.#.......#...#",
        "#####.#.#.#######.#.###",
        "#.....#.#.#.......#...#",
        "#.#####.#.#.#########v#",
        "#.#...#...#...###...>.#",
        "#.#.#v#######v###.###v#",
        "#...#.>.#...>.>.#.###.#",
        "#####v#.#.###v#.#.###.#",
        "#.....#...#...#.#.#...#",
        "#.#########.###.#.#.###",
        "#...###...#...#...#.###",
        "###.###.#.###v#####v###",
        "#...#...#.#.>.>.#.>.###",
        "#.###.###.#.###.#.#v###",
        "#.....###...###...#...#",
        "#####################.#",
    ]
    # pathes: (.)
    # forests: (#)
    # steep slopes: (^, >, v, <)
    #   stepping on a slope is one way
    # start = top row single path
    # goal = bottom row single path
    # never step on same tile twice
    # longest possible hike route?

    advent_map = AdventMap(example_data)
    advent_map.print_map()

    path_finder = PathFinder(advent_map)
    longest_path = path_finder.find_longest_path()

    print("\nLongest Path Length:", len(longest_path))
    advent_map.print_map(longest_path)

    assert len(longest_path) == 94


if __name__ == "__main__":
    test_example_data()