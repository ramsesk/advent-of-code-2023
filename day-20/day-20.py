from enum import Enum

class BaseModule:
    module_type = "base"    
    def __init__(self, name: str, destinations: str) -> None:
        self.destinations = destinations
        self.module_name = name

    def __str__(self) -> str:
        return f"Module(name={self.module_name}, type={self.module_type}, destinations={self.destinations})"

class BroadcasterModule(BaseModule):
    module_type = "broadcaster"
    
class FlipflopState(Enum):
        OFF = 0
        ON = 1

class FlipflopModule(BaseModule):
    module_type = "flipflop"
    def __init__(self, name: str, destinations: list) -> None:
        super().__init__(name, destinations)
        self.state = FlipflopState.OFF

class ConjunctionState(Enum):
    LOW_PULSE_REMEMBER = 1
    HIGH_PULSE_REMEMBER = 2

class ConjunctionModule(BaseModule):
    module_type = "conjunction"
    def __init__(self, name: str, destinations: list) -> None:
        super().__init__(name, destinations)
        # Initialize the state for each destination module
        self.states = {dest: ConjunctionState.LOW_PULSE_REMEMBER for dest in destinations}


class ModuleFactory:
    @staticmethod
    def create_module(config_str: str):
        parts = config_str.split(" -> ")
        name = parts[0]
        destinations = parts[1].split(", ") if len(parts) > 1 else []

        if name.startswith("%"):
            return FlipflopModule(name, destinations)
        elif name.startswith("&"):
            return ConjunctionModule(name, destinations)
        elif name == "broadcaster":
            return BroadcasterModule(name, destinations)
        else:
            return BaseModule(name, destinations)

class ModuleConfiguration:
    def __init__(self, config_data: list):
        self.modules = {}
        self.parse_config_data(config_data)
        self.setup_all_destinations()

    def parse_config_data(self, config_data: list):
        for line in config_data:
            module = ModuleFactory.create_module(line)
            self.modules[module.module_name] = module

    def setup_all_destinations(self):
        for module in self.modules.values():
            destination_list = [self.modules[dest_name] for dest_name in module.destinations if dest_name in self.modules]
            module.destinations = destination_list

    def __str__(self) -> str:
        return "\n".join(str(module) for module in self.modules.values())


def test_example_data():
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