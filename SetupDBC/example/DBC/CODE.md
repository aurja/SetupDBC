Code links to [CONCEPTS](CONCEPTS.md), [DEFINITIONS](DEFINITIONS.md), [TESTS](TESTS.md), and [SCENARIOS](SCENARIOS.md).

| Node | Code | Notes |
| --- | --- | --- |
| `Command` | `src/kettle.py` `set_target` | Accepts a user temperature. |
| `State` | `src/kettle.py` `current_mode` | Exposes the operating mode. |
| `Shutdown` | `src/kettle.py` `stop_heating` | Turns the element off. |
| `Probe` | `src/kettle.py` `read_temperature` | Reads the sample. |
| `Filter` | `src/kettle.py` `filtered_temperature` | Provides the conditioned reading. |
| `CurrentReading` | `src/kettle.py` `read_temperature` | Supplies the current sample. |
| `Target` | `src/kettle.py` `set_target` | Stores the requested threshold. |
| `TargetInput` | `src/kettle.py` `set_target` | Supplies the requested comparison threshold. |
| `EmptyGuard` | `src/kettle.py` `reject_empty` | Stops heating when empty. |
| `Interlock` | `src/kettle.py` `safety_enabled` | Combines safety conditions. |
| `OverheatGuard` | `src/kettle.py` `overheat_trip` | Stops heating above the safe threshold. |
| `SampleInput` | `src/kettle.py` `read_temperature` | Reads the value used by control. |
| `CompareTarget` | `src/kettle.py` `compare_target` | Current work unit's comparison behavior. |
