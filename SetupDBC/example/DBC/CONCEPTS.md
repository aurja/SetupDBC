# Concepts

The electric-kettle concept map links to [CODE](CODE.md), [DEFINITIONS](DEFINITIONS.md), [TESTS](TESTS.md), and [SCENARIOS](SCENARIOS.md).

## How to read the diagrams
L1 frames the whole controller; deeper levels open parts or rules that deserve separate decisions. Structure diagrams use solid labelled arrows for what flows and dotted labelled arrows for checks or limits. Rule diagrams are terminal flowcharts: diamonds ask decisions and arrows carry answers. Status colors mean implemented (built), partial (in the current work unit), planned (not started), and external (owned elsewhere). Node IDs are stable references; run `python3 DBC/check_dbc.py` to check this map.

## L1 · Electric kettle controller
```mermaid
flowchart LR
classDef implemented fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
classDef partial fill:#fff3b0,stroke:#b58900,color:#5c4400
classDef planned stroke-dasharray:6 4
classDef external fill:#eeeeee,stroke:#9e9e9e,stroke-dasharray:1 3,color:#616161
ControllerInterface["Controller interface"] -->|target and mode request| Control["Control"]
Sensing["Sensing"] -->|water temperature sample| Control
Control -->|heat request| Heating["Heating"]
Safety["Safety"] -.->|limits| Control
Safety -.->|cuts off| Heating
class ControllerInterface,Sensing,Safety implemented
class Control partial
class Heating planned
```

| Node | Meaning | Terms | Status |
| --- | --- | --- | --- |
| `ControllerInterface` | Accepts target and mode requests, exposes state, and provides a stop control. | target, mode | implemented |
| `Sensing` | Provides the controller's measured water temperature. | measurement, temperature | implemented |
| `Control` | Chooses whether the element starts, holds, or stops. | control rule, target | partial |
| `Heating` | Transfers energy from the element into the water. | heating element, energy | planned |
| `Safety` | Prevents unsafe heating conditions. | safety, heating element | implemented |

The [Heating subtree](concepts/Heating.md) holds its level-two detail and links back here.

### L2 · Controller interface (`ControllerInterface`)
```mermaid
flowchart LR
classDef implemented fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
classDef partial fill:#fff3b0,stroke:#b58900,color:#5c4400
classDef planned stroke-dasharray:6 4
classDef external fill:#eeeeee,stroke:#9e9e9e,stroke-dasharray:1 3,color:#616161
Command["User command"] -->|target request| State["Operating state"]
CurrentReading["Current reading"] -->|temperature display| State
Command -->|stop request| Shutdown["Shutdown"]
class Command,State,Shutdown implemented
class CurrentReading external
```

| Node | Meaning | Terms | Status |
| --- | --- | --- | --- |
| `Command` | Accepts a user request for a temperature. | target, measurement | implemented |
| `State` | Exposes the active operating mode. | mode, state | implemented |
| `Shutdown` | Ends heating when the controller stops. | power, safety | implemented |
| `CurrentReading` | See Temperature sensing. |  | external |

### L2 · Temperature sensing (`Sensing`)
```mermaid
flowchart LR
classDef implemented fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
classDef partial fill:#fff3b0,stroke:#b58900,color:#5c4400
classDef planned stroke-dasharray:6 4
classDef external fill:#eeeeee,stroke:#9e9e9e,stroke-dasharray:1 3,color:#616161
Probe["Probe"] -->|raw sample| Filter["Filter"]
Filter -->|filtered temperature| CurrentReading["Current reading"]
class Probe,Filter,CurrentReading implemented
```

| Node | Meaning | Terms | Status |
| --- | --- | --- | --- |
| `Probe` | Observes the water's current temperature. | measurement, temperature | implemented |
| `Filter` | Provides a stable reading to control. | measurement, temperature | implemented |
| `CurrentReading` | Supplies the value used to choose heating actions. | temperature, measurement | implemented |

### L2 · Temperature control (`Control`)
```mermaid
flowchart LR
classDef implemented fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
classDef partial fill:#fff3b0,stroke:#b58900,color:#5c4400
classDef planned stroke-dasharray:6 4
classDef external fill:#eeeeee,stroke:#9e9e9e,stroke-dasharray:1 3,color:#616161
Target["Target"] -->|requested threshold| Regulation["Regulation"]
Regulation -->|chosen heating mode| Mode["Mode"]
class Regulation partial
class Target implemented
class Mode planned
```

| Node | Meaning | Terms | Status |
| --- | --- | --- | --- |
| `Regulation` | Coordinates sampling and temperature decisions. | control rule, temperature | partial |
| `Target` | Holds the desired water temperature. | target, temperature | implemented |
| `Mode` | Selects a future controller operating mode. | mode, control rule | planned |

#### L3 · Regulation (`Regulation`)
```mermaid
flowchart LR
classDef implemented fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
classDef partial fill:#fff3b0,stroke:#b58900,color:#5c4400
classDef planned stroke-dasharray:6 4
classDef external fill:#eeeeee,stroke:#9e9e9e,stroke-dasharray:1 3,color:#616161
SampleInput["Sample input"] -->|measured temperature| CompareTarget["Compare with target"]
TargetInput["Target input"] -->|requested threshold| CompareTarget
CompareTarget -->|comparison result| HeatDecision["Heating decision"]
class SampleInput,TargetInput implemented
class CompareTarget,HeatDecision partial
```

| Node | Meaning | Terms | Status |
| --- | --- | --- | --- |
| `SampleInput` | Supplies the current temperature to regulation. | measurement, temperature | implemented |
| `TargetInput` | Supplies the requested temperature for comparison. | target, temperature | implemented |
| `CompareTarget` | Compares the sample with the requested temperature. | control rule, target | partial |
| `HeatDecision` | Chooses whether to start, hold, or stop heating. | control rule, heating element | partial |

##### L4 rule · Heating decision (`HeatDecision`)
```mermaid
flowchart TD
classDef implemented fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
classDef partial fill:#fff3b0,stroke:#b58900,color:#5c4400
classDef planned stroke-dasharray:6 4
classDef external fill:#eeeeee,stroke:#9e9e9e,stroke-dasharray:1 3,color:#616161
BelowTarget{"Water below target?"} -->|yes| MaintainHeat["Maintain heat"]
BelowTarget -->|no| StopHeating["Stop heating"]
MaintainHeat -->|target reached| StopHeating
class BelowTarget,MaintainHeat partial
class StopHeating planned
```

| Node | Meaning | Terms | Status |
| --- | --- | --- | --- |
| `BelowTarget` | Decides whether the sample is below the requested temperature. | control rule, target | partial |
| `MaintainHeat` | Continues heating while the target is unmet. | control rule, temperature | partial |
| `StopHeating` | Ends heating once the target is reached. | control rule, heating element | planned |

### L2 · Safety interlocks (`Safety`)
```mermaid
flowchart LR
classDef implemented fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
classDef partial fill:#fff3b0,stroke:#b58900,color:#5c4400
classDef planned stroke-dasharray:6 4
classDef external fill:#eeeeee,stroke:#9e9e9e,stroke-dasharray:1 3,color:#616161
EmptyGuard["Empty guard"] -.->|blocks an empty vessel| Interlock["Combined interlock"]
OverheatGuard["Overheat guard"] -.->|blocks excess heat| Interlock
class EmptyGuard,OverheatGuard,Interlock implemented
```

| Node | Meaning | Terms | Status |
| --- | --- | --- | --- |
| `EmptyGuard` | Rejects a heating request when the vessel is empty. | safety, heating element | implemented |
| `OverheatGuard` | Stops heating when temperature exceeds the safe range. | safety, temperature | implemented |
| `Interlock` | Allows heating only while safety conditions hold. | safety, control rule | implemented |

#### L3 rule · Overheat response (`OverheatGuard`)
```mermaid
flowchart TD
classDef implemented fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
classDef partial fill:#fff3b0,stroke:#b58900,color:#5c4400
classDef planned stroke-dasharray:6 4
classDef external fill:#eeeeee,stroke:#9e9e9e,stroke-dasharray:1 3,color:#616161
SafeTemperature{"Above safe temperature?"} -->|yes| Trip["Trip heating"]
Trip -->|condition persists| Hold["Hold off"]
SafeTemperature -->|no| Reset["Reset interlock"]
class SafeTemperature,Trip implemented
class Hold,Reset planned
```

| Node | Meaning | Terms | Status |
| --- | --- | --- | --- |
| `SafeTemperature` | Determines whether water is above the safe temperature limit. | safety, temperature | implemented |
| `Trip` | Stops the element when an overheat threshold is crossed. | safety, heating element | implemented |
| `Hold` | Keeps the element off while the condition persists. | safety, control rule | planned |
| `Reset` | Re-enables control after a safe temperature returns. | safety, temperature | planned |
