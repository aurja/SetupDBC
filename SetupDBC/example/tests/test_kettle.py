from src.kettle import KettleController


def test_target_and_mode_are_available() -> None:
    kettle = KettleController()
    kettle.set_target(85.0)

    assert kettle.target == 85.0
    assert kettle.current_mode() == "boil"


def test_temperature_comparison_controls_heating() -> None:
    kettle = KettleController()

    assert kettle.read_temperature() == 20.0
    assert kettle.compare_target()
    kettle.start_heating()
    assert kettle.heating
    kettle.maintain_heat()
    assert kettle.heating
