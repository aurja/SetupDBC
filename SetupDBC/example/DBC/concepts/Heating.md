This subtree links back to [CONCEPTS](../CONCEPTS.md).

### L2 · Heating supply (`Heating`)
```mermaid
flowchart LR
classDef implemented fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
classDef partial fill:#fff3b0,stroke:#b58900,color:#5c4400
classDef planned stroke-dasharray:6 4
classDef external fill:#eeeeee,stroke:#9e9e9e,stroke-dasharray:1 3,color:#616161
Element["Heating element"]
Transfer["Heat transfer"]
Water["Water heating"]
Element -->|thermal energy| Transfer
Transfer -->|heat| Water
class Element planned
class Transfer planned
class Water planned
```

| Node | Meaning | Terms | Status |
| --- | --- | --- | --- |
| `Element` | The component that transfers energy to water. | heating element, energy | planned |
| `Transfer` | The path by which the element warms water. | energy, temperature | planned |
| `Water` | The water receiving heat from the element. | temperature, energy | planned |
