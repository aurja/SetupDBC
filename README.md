# SetupDBC

An omp agent skill that sets up DBC
(Driven by Concepts) in an existing project: a concept map of linked mermaid
diagrams, plus code map, glossary, test and evidence lists, a drift checker,
and the agent-context rules that keep them current.

## Install

```sh
git clone https://github.com/aurja/SetupDBC.git
cd SetupDBC
./install.sh              # installs to ~/.omp/agent/skills/SetupDBC
./install.sh <skills-dir> # or to another skills directory
```

The installer replaces any existing `SetupDBC` install at the target. Edit the
skill here, then rerun `./install.sh`.

## Use

Ask the agent to "set up DBC" in a project. See
[`SetupDBC/SKILL.md`](SetupDBC/SKILL.md) for the procedure; the format
specification is the docstring of
[`SetupDBC/check_dbc.py`](SetupDBC/check_dbc.py).

## Layout

| Path | Holds |
|---|---|
| `SetupDBC/SKILL.md` | The skill instructions |
| `SetupDBC/check_dbc.py` | The drift checker, copied into each DBC project |
| `SetupDBC/example/` | A small repository whose DBC passes the checker |
| `SetupDBC/tests/` | The checker's tests |
| `install.sh` | Copies `SetupDBC/` into the skills directory |

## Check

```sh
cd SetupDBC
python3 check_dbc.py --root example --dbc example/DBC
python3 -m pytest -q tests
```

## License

MIT; see [LICENSE](LICENSE).
