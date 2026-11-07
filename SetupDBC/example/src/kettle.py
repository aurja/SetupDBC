class KettleController:
    def __init__(self) -> None:
        self.target = 100.0
        self.mode = "boil"
        self.temperature = 20.0
        self.empty = False
        self.heating = False

    def set_target(self, target: float) -> None:
        self.target = target

    def current_mode(self) -> str:
        return self.mode

    def stop_heating(self) -> None:
        self.heating = False

    def read_temperature(self) -> float:
        return self.temperature

    def filtered_temperature(self) -> float:
        return self.read_temperature()

    def compare_target(self) -> bool:
        return self.filtered_temperature() < self.target

    def start_heating(self) -> None:
        self.heating = True

    def maintain_heat(self) -> None:
        self.heating = self.temperature < self.target

    def reject_empty(self) -> bool:
        if self.empty:
            self.stop_heating()
        return not self.empty

    def overheat_trip(self) -> bool:
        if self.temperature > self.target + 5:
            self.stop_heating()
            return True
        return False

    def safety_enabled(self) -> bool:
        return not self.empty and self.temperature <= self.target + 5
