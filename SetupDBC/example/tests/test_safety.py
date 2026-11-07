from src.kettle import KettleController


def test_empty_interlock_stops_heating() -> None:
    kettle = KettleController()
    kettle.start_heating()
    kettle.empty = True

    assert not kettle.reject_empty()
    assert not kettle.heating
    assert not kettle.safety_enabled()


def test_overheat_trip_stops_heating() -> None:
    kettle = KettleController()
    kettle.start_heating()
    kettle.temperature = 106.0

    assert kettle.overheat_trip()
    assert not kettle.heating
