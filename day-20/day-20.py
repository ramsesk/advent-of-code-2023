from enum import Enum
from typing import List, Union, Dict

class BaseModule:
    module_type: str = "base"
    
    def __init__(self, name: str, destinations: Union[List[str], List['BaseModule']]) -> None:
        self.destinations: Union[List[str], List['BaseModule']] = destinations
        self.module_name: str = name

    def __str__(self) -> str:
        destination_names = [dest.module_name if isinstance(dest, BaseModule) else dest for dest in self.destinations]
        return f"Module(name={self.module_name}, type={self.module_type}, destinations={destination_names})"

class BroadcasterModule(BaseModule):
    module_type: str = "broadcaster"
    
class FlipflopState(Enum):
    OFF = 0
    ON = 1

class FlipflopModule(BaseModule):
    module_type: str = "flipflop"

    def __init__(self, name: str, destinations: Union[List[str], List[BaseModule]]) -> None:
        super().__init__(name, destinations)
        self.state: FlipflopState = FlipflopState.OFF

class ConjunctionState(Enum):
    LOW_PULSE_REMEMBER = 1
    HIGH_PULSE_REMEMBER = 2

class ConjunctionModule(BaseModule):
    module_type: str = "conjunction"

    def __init__(self, name: str, destinations: Union[List[str], List[BaseModule]]) -> None:
        super().__init__(name, destinations)
        self.states: Dict[str, ConjunctionState] = {dest: ConjunctionState.LOW_PULSE_REMEMBER for dest in destinations if isinstance(dest, str)}

class ModuleFactory:
    @staticmethod
    def create_module(config_str: str) -> BaseModule:
        parts = config_str.split(" -> ")
        full_name = parts[0]
        destinations = parts[1].split(", ") if len(parts) > 1 else []

        name = full_name.lstrip("%&")

        if full_name.startswith("%"):
            return FlipflopModule(name, destinations)
        elif full_name.startswith("&"):
            return ConjunctionModule(name, destinations)
        elif full_name == "broadcaster":
            return BroadcasterModule(name, destinations)
        else:
            return BaseModule(name, destinations)

class ModuleConfiguration:
    def __init__(self, config_data: List[str]) -> None:
        self.modules: Dict[str, BaseModule] = {}
        self.parse_config_data(config_data)
        self.setup_all_destinations()

    def parse_config_data(self, config_data: List[str]) -> None:
        for line in config_data:
            module = ModuleFactory.create_module(line)
            self.modules[module.module_name] = module

    def setup_all_destinations(self) -> None:
        for module in self.modules.values():
            if isinstance(module.destinations, list) and module.destinations and isinstance(module.destinations[0], str):
                module.destinations = [self.modules[dest_name] for dest_name in module.destinations if dest_name in self.modules]

    def __str__(self) -> str:
        return "\n".join(str(module) for module in self.modules.values())

def test_example_data() -> None:
    example_data = [
        "broadcaster -> a, b, c",
        "%a -> b",
        "%b -> c",
        "%c -> inv",
        "&inv -> a",
    ]

    module_config = ModuleConfiguration(example_data)
    print(module_config)    

    assert 0

if __name__ == "__main__":
    test_example_data()