from __future__ import annotations
from enum import Enum
from typing import List, Union, Dict
from queue import Queue

class BaseModule:
    module_type: str = "base"
    
    def __init__(self, name: str, destinations: Union[List[str], List['BaseModule']]) -> None:
        self.destinations: Union[List[str], List['BaseModule']] = destinations
        self.module_name: str = name

    def __str__(self) -> str:
        destination_names = [dest.module_name if isinstance(dest, BaseModule) else dest for dest in self.destinations]
        return f"Module(name={self.module_name}, type={self.module_type}, destinations={destination_names})"

    def handle_pulse(self, pulse: PulseEvent) -> List[PulseEvent]:
        return []



class BroadcasterModule(BaseModule):
    module_type: str = "broadcaster"

    def handle_pulse(self, pulse: PulseEvent) -> List[PulseEvent]:
        new_pulses  = []
        for dest in self.destinations:
            new_pulses .append(PulseEvent(source=self, destination=dest, pulse_type=pulse.pulse_type))
        
        return new_pulses
    
class FlipflopState(Enum):
    OFF = 0
    ON = 1

class FlipflopModule(BaseModule):
    module_type: str = "flipflop"

    def __init__(self, name: str, destinations: Union[List[str], List[BaseModule]]) -> None:
        super().__init__(name, destinations)
        self.state: FlipflopState = FlipflopState.OFF

    def handle_pulse(self, pulse: PulseEvent) -> List[PulseEvent]:
        new_pulses = []
        if pulse.pulse_type == PulseType.LOW:
            # Flip state and generate new pulses
            self.state = FlipflopState.ON if self.state == FlipflopState.OFF else FlipflopState.OFF
            new_pulse_type = PulseType.LOW if self.state == FlipflopState.OFF else PulseType.HIGH
            for dest in self.destinations:
                new_pulses.append(PulseEvent(source=self, destination=dest, pulse_type=new_pulse_type))
        return new_pulses

class ConjunctionState(Enum):
    LOW_PULSE_REMEMBER = 1
    HIGH_PULSE_REMEMBER = 2

class ConjunctionModule(BaseModule):
    module_type: str = "conjunction"

    def __init__(self, name: str, destinations: Union[List[str], List[BaseModule]]) -> None:
        super().__init__(name, destinations)
        self.states: Dict[str, PulseType] = {}
    
    def handle_pulse(self, pulse: PulseEvent) -> List[PulseEvent]:
        new_pulses = []
        self.states[pulse.source.module_name] = pulse.pulse_type

        if all(state == PulseType.HIGH for state in self.states.values()):
            new_pulse_type = PulseType.LOW
        else:
            new_pulse_type = PulseType.HIGH

        for dest in self.destinations:
            new_pulses.append(PulseEvent(source=self, destination=dest, pulse_type=new_pulse_type))

        return new_pulses


class ButtonModule(BaseModule):
    module_type = "button"

    def __init__(self):
        super().__init__("button", [])

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
        self.create_default_modules_for_undefined_destinations()
        self.setup_all_destinations()
        self.add_button_module()

    def parse_config_data(self, config_data: List[str]) -> None:
        for line in config_data:
            module = ModuleFactory.create_module(line)
            self.modules[module.module_name] = module

    def initialize_conjunction_inputs(self):
        for module in self.modules.values():
            for dest in module.destinations:
                if isinstance(dest, ConjunctionModule):
                    # Initialize the state for this input module in the ConjunctionModule
                    dest.states[module.module_name] = PulseType.LOW

    def create_default_modules_for_undefined_destinations(self):
        all_destinations = set()
        for module in self.modules.values():
            if isinstance(module.destinations, list):
                all_destinations.update(dest for dest in module.destinations if isinstance(dest, str))

        for dest_name in all_destinations:
            if dest_name not in self.modules:
                self.modules[dest_name] = BaseModule(dest_name, [])

    def setup_all_destinations(self) -> None:
        for module in self.modules.values():
            module.destinations = [self.modules[dest_name] if isinstance(dest_name, str) else dest_name for dest_name in module.destinations]

        self.initialize_conjunction_inputs()

    
    def add_button_module(self):
        broadcaster = self.modules.get("broadcaster")
        if broadcaster:
            button = ButtonModule()
            button.destinations = [broadcaster]
            self.modules[button.module_name] = button

    def __str__(self) -> str:
        return "\n".join(str(module) for module in self.modules.values())

class PulseType(Enum):
    LOW = 'low'
    HIGH = 'high'

class PulseEvent:
    def __init__(self, source: BaseModule, destination: BaseModule, pulse_type: PulseType):
        self.source = source
        self.destination = destination
        self.pulse_type = pulse_type

    def __str__(self) -> str:
        return f"{self.source.module_name} -{self.pulse_type.value}-> {self.destination.module_name}"

class PulseManager:
    def __init__(self, module_config: ModuleConfiguration):
        self.module_config = module_config
        self.queue = Queue()
        self.low_pulse_count = 0
        self.high_pulse_count = 0

        self.pulse_log: List[PulseEvent] = []

    def push_button(self):
        # Simulate pushing the button by sending a low pulse to the broadcaster
        broadcaster = self.module_config.modules.get("broadcaster")
        button = self.module_config.modules.get("button")
        assert broadcaster
        assert button
        self.queue.put(PulseEvent(source=button, destination=broadcaster, pulse_type=PulseType.LOW))

    def process_pulses(self):
        while not self.queue.empty():
            pulse_event = self.queue.get()
            self.pulse_log.append(pulse_event)
            
            if pulse_event.pulse_type == PulseType.LOW:
                self.low_pulse_count += 1
            elif pulse_event.pulse_type == PulseType.HIGH:
                self.high_pulse_count += 1
            else:
                assert 0
            
            new_pulses = pulse_event.destination.handle_pulse(pulse_event)
            for pulse in new_pulses:
                self.queue.put(pulse)

    def run_simulation(self, n: int):
        for _ in range(n):
            self.push_button()
            self.process_pulses()

    def get_formatted_pulse_log(self) -> str:
        return "\n".join(str(pulse_event) for pulse_event in self.pulse_log)


def test_example_data() -> None:
    example_data = [
        "broadcaster -> a, b, c",
        "%a -> b",
        "%b -> c",
        "%c -> inv",
        "&inv -> a",
    ]

    module_config = ModuleConfiguration(example_data)
    print("\nExample Module Configuration 1")
    print(module_config)

    pulse_manager = PulseManager(module_config)
    pulse_manager.run_simulation(1)
    print("\nPulse log of one button push:")
    print(pulse_manager.get_formatted_pulse_log())
    pulse_manager.run_simulation(999)

    pulse_product = pulse_manager.low_pulse_count * pulse_manager.high_pulse_count

    assert pulse_product == 32000000

def test_example_data2() -> None:
    example_data2 = [
        "broadcaster -> a",
        "%a -> inv, con",
        "&inv -> b",
        "%b -> con",
        "&con -> output",
    ]

    module_config = ModuleConfiguration(example_data2)
    print("\nExample Module Configuration 2")
    print(module_config)

    pulse_manager = PulseManager(module_config)
    pulse_manager.run_simulation(1)
    print("Pulse log of one button push:")
    print(pulse_manager.get_formatted_pulse_log())
    pulse_manager.run_simulation(999)

    pulse_product = pulse_manager.low_pulse_count * pulse_manager.high_pulse_count
    assert pulse_product == 11687500

if __name__ == "__main__":
    test_example_data()

    test_example_data2()