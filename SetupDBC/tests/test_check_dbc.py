from __future__ import annotations

import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parents[1]
CHECKER = SKILL_DIR / "check_dbc.py"
EXAMPLE = SKILL_DIR / "example"
Mutation = Callable[[Path], None]


def copied_project(tmp_path: Path) -> Path:
    project = tmp_path / "project"
    _ = shutil.copytree(EXAMPLE, project)
    return project


def run_checker(project: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(CHECKER),
            "--root",
            str(project),
            "--dbc",
            str(project / "DBC"),
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text
    _ = path.write_text(text.replace(old, new, 1), encoding="utf-8")


def exceed_max_nodes(project: Path) -> None:
    concepts = project / "DBC/CONCEPTS.md"
    declarations = "\n".join(
        f'Extra{number}["Extra {number}"]' for number in range(1, 9)
    )
    replace_once(
        concepts,
        'ControllerInterface["Controller interface"] -->|target and mode request| Control["Control"]\n',
        'ControllerInterface["Controller interface"] -->|target and mode request| Control["Control"]\n'
        + declarations
        + "\n",
    )
    class_rows = "\n".join(f"class Extra{number} implemented" for number in range(1, 9))
    replace_once(
        concepts,
        "class ControllerInterface,Sensing,Safety implemented\n",
        "class ControllerInterface,Sensing,Safety implemented\n" + class_rows + "\n",
    )
    node_rows = "".join(
        f"| `Extra{number}` | Additional top-level concept. | energy | implemented |\n"
        for number in range(1, 9)
    )
    replace_once(
        concepts,
        "| `Safety` | Prevents unsafe heating conditions. | safety, heating element | implemented |\n",
        "| `Safety` | Prevents unsafe heating conditions. | safety, heating element | implemented |\n"
        + node_rows,
    )


def fall_below_min_nodes(project: Path) -> None:
    replace_once(
        project / "DBC/CONCEPTS.md",
        "| `StopHeating` | Ends heating once the target is reached. | control rule, heating element | planned |\n",
        "",
    )


def add_child_under_rule_node(project: Path) -> None:
    concepts = project / "DBC/CONCEPTS.md"
    child = """
##### L4 rule · Trip hold (`Trip`)
```mermaid
flowchart TD
classDef implemented fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
classDef partial fill:#fff3b0,stroke:#b58900,color:#5c4400
classDef planned stroke-dasharray:6 4
classDef external fill:#eeeeee,stroke:#9e9e9e,stroke-dasharray:1 3,color:#616161
SafeTemperature{"Above safe temperature?"} -->|yes| Release["Release"]
SafeTemperature -->|no| Resume["Resume"]
Release -->|cleared| Resume
class SafeTemperature,Release,Resume implemented
```

| Node | Meaning | Terms | Status |
| --- | --- | --- | --- |
| `SafeTemperature` | Confirms water has returned to a safe range. | temperature, safety | implemented |
| `Release` | Clears the overheat latch. | safety, control rule | implemented |
| `Resume` | Allows the controller to continue. | control rule, safety | implemented |
"""
    with concepts.open("a", encoding="utf-8") as stream:
        _ = stream.write(child)


def skip_level(project: Path) -> None:
    replace_once(
        project / "DBC/CONCEPTS.md",
        "##### L4 rule · Heating decision (`HeatDecision`)",
        "##### L4 rule · Heating decision (`Regulation`)",
    )


def disagree_parent_status(project: Path) -> None:
    concepts = project / "DBC/CONCEPTS.md"
    replace_once(
        concepts,
        "class Regulation partial\n",
        "class Regulation implemented\n",
    )
    replace_once(
        concepts,
        "| `Regulation` | Coordinates sampling and temperature decisions. | control rule, temperature | partial |",
        "| `Regulation` | Coordinates sampling and temperature decisions. | control rule, temperature | implemented |",
    )


def use_undefined_term(project: Path) -> None:
    replace_once(
        project / "DBC/CONCEPTS.md",
        "| `ControllerInterface` | Accepts target and mode requests, exposes state, and provides a stop control. | target, mode | implemented |",
        "| `ControllerInterface` | Accepts target and mode requests, exposes state, and provides a stop control. | unlisted term | implemented |",
    )


def remove_code_row(project: Path) -> None:
    replace_once(
        project / "DBC/CODE.md",
        "| `Command` | `src/kettle.py` `set_target` | Accepts a user temperature. |\n",
        "",
    )


def missing_code_symbol(project: Path) -> None:
    replace_once(
        project / "DBC/CODE.md",
        "`src/kettle.py` `set_target`",
        "`src/kettle.py` `missing_symbol`",
    )


def add_code_line_reference(project: Path) -> None:
    replace_once(
        project / "DBC/CODE.md",
        "`src/kettle.py` `set_target`",
        "`src/kettle.py:12` `set_target`",
    )


def unknown_test_node(project: Path) -> None:
    replace_once(
        project / "DBC/TESTS.md",
        "`ControllerInterface`, `Control`",
        "`ControllerInterface`, `UnknownNode`",
    )


def omit_test_glob_file(project: Path) -> None:
    replace_once(
        project / "DBC/TESTS.md",
        "| `tests/test_kettle.py` | Target, mode and heating behavior | `ControllerInterface`, `Control` |\n",
        "",
    )


def omit_evidence_comments(project: Path) -> None:
    replace_once(
        project / "DBC/SCENARIOS.md",
        "**Comments:** 2026-11-07, `SetupDBC-example`: this scenario illustrates the review format.\n",
        "",
    )


def unlink_subtree(project: Path) -> None:
    replace_once(
        project / "DBC/CONCEPTS.md",
        "The [Heating subtree](concepts/Heating.md) holds its level-two detail and links back here.\n",
        "",
    )


def lower_review_depth(project: Path) -> None:
    with (project / "DBC/dbc.toml").open("a", encoding="utf-8") as stream:
        _ = stream.write("review_depth = 3\n")


def add_unknown_config_key(project: Path) -> None:
    with (project / "DBC/dbc.toml").open("a", encoding="utf-8") as stream:
        _ = stream.write("unexpected_key = true\n")


def remove_node_status_class(project: Path) -> None:
    replace_once(
        project / "DBC/CONCEPTS.md",
        "class Command,State,Shutdown implemented\n",
        "",
    )


def alter_class_definition(project: Path) -> None:
    replace_once(
        project / "DBC/CONCEPTS.md",
        "classDef implemented fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20\n",
        "",
    )


def test_example_dbc_passes_and_reports_summary(tmp_path: Path) -> None:
    project = copied_project(tmp_path)

    result = run_checker(project)

    assert result.returncode == 0, result.stdout + result.stderr
    assert (
        "check_dbc: ok — 31 nodes (L1 5, L2 15, L3 8, L4 3), "
        "13 code rows, 2 test rows, 1 evidence sections"
    ) in result.stdout


@pytest.mark.parametrize(
    ("mutation", "exit_code", "message"),
    [
        (exceed_max_nodes, 1, "L1 diagram owns 13 nodes"),
        (fall_below_min_nodes, 1, "L4 diagram owns 2 nodes"),
        (add_child_under_rule_node, 1, "rule diagrams cannot have child diagrams"),
        (skip_level, 1, "L4 diagram parent Regulation must be owned at L3"),
        (
            disagree_parent_status,
            1,
            "parent/child status disagreement for Regulation: expected 'partial' from child nodes, found parent 'implemented'",
        ),
        (use_undefined_term, 1, "uses unknown term 'unlisted term'"),
        (remove_code_row, 1, "code-mapped node Command has no CODE row"),
        (missing_code_symbol, 1, "CODE symbol 'missing_symbol' is not present"),
        (add_code_line_reference, 1, "is a line-number reference"),
        (
            unknown_test_node,
            1,
            "TESTS Concepts cell references unknown or non-owned node ID UnknownNode",
        ),
        (
            omit_test_glob_file,
            1,
            "test file 'tests/test_kettle.py' has no TESTS citation",
        ),
        (omit_evidence_comments, 1, "line starting '**Comments:**'"),
        (
            unlink_subtree,
            1,
            "CONCEPTS.md does not link to subtree file concepts/Heating.md",
        ),
        (
            remove_node_status_class,
            1,
            "node Command has status 'implemented' but mermaid status classes are no status class",
        ),
        (alter_class_definition, 1, "mermaid classDef must declare exactly once"),
        (add_unknown_config_key, 2, "unknown config key(s): unexpected_key"),
    ],
    ids=[
        "max-nodes",
        "min-nodes",
        "rule-child",
        "level-skip",
        "status-disagreement",
        "undefined-term",
        "missing-code-row",
        "missing-symbol",
        "line-reference",
        "unknown-test-node",
        "uncited-test",
        "missing-comments",
        "subtree-link",
        "missing-node-class",
        "class-definition",
        "unknown-config-key",
    ],
)
def test_seeded_mutation_reports_targeted_problem(
    tmp_path: Path, mutation: Mutation, exit_code: int, message: str
) -> None:
    project = copied_project(tmp_path)
    mutation(project)

    result = run_checker(project)
    output = result.stdout + result.stderr

    assert result.returncode == exit_code, output
    assert message in output


def test_lower_review_depth_prints_a_note_without_failing(tmp_path: Path) -> None:
    project = copied_project(tmp_path)
    lower_review_depth(project)

    result = run_checker(project)

    assert result.returncode == 0, result.stdout + result.stderr
    assert ": note: L4 is deeper than review_depth 3" in result.stdout
    assert "check_dbc: ok —" in result.stdout
