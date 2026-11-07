---
name: SetupDBC
description: Set up DBC (Driven by Concepts) in an existing project that has none — concept map with depth set by need, code map, glossary, test and evidence lists, drift checker, and the AGENTS.md rules that keep them current. Use when asked to "set up DBC", "make this a DBC project" or similar.
---

# SetupDBC

DBC (Driven by Concepts) is the Captain's method for leading a project: she
reasons and decides at the level of concepts, drawn as linked diagrams; code,
tests and evidence are mapped to those concepts; a drift check keeps the map
honest. Her edits to a diagram are directives: the orchestrator turns them
into plans and code, then brings the map back in line with what was built.

This skill builds that infrastructure for a project that has none. It does
not change production code. If the project already has a DBC directory, stop
and say so: this skill is for setup only.

Skill files: `check_dbc.py` (the drift checker; its docstring is the one and
only format specification), `example/` (a small repository whose DBC passes
the checker, with a four-level branch, rule diagrams, a yellow `partial`
branch reaching L1 and a subtree file), `tests/` (the checker's own tests).
The example carries no copy of the checker; check it with
`python3 check_dbc.py --root example --dbc example/DBC` from the skill
directory. Read the docstring and skim `example/DBC/` before drafting
anything.

## What you build

The DBC directory is `Planning/DBC/` if the project has `Planning/`, else
`DBC/`. It holds five files that link to each other, plus config and checker:

| File | Holds |
|---|---|
| `CONCEPTS.md` | The concept map: mermaid diagrams, each with a node table (Node, Meaning, Terms, Status). No code, file names or plan names |
| `CODE.md` | Each built concept → files and symbols. Never line numbers |
| `DEFINITIONS.md` | Glossary: every term a node uses, and the project's own sense of generic words, with where each was decided |
| `TESTS.md` | Every test, what it checks, the concept nodes it guards |
| evidence file | Where concepts meet reality, named for the project's kind of evidence: `FIXTURES.md` (inputs with expected facts), `EXERCISES.md` (graded tasks with acceptance), `SCENARIOS.md` (simulation or end-to-end cases), `BENCHMARKS.md`. Sections carry `**Concepts:**` and a `**Comments:**` column or line for dated, signed agent notes |
| `dbc.toml` | Checker config (keys in the docstring) |
| `check_dbc.py` | Copied from this skill unchanged, so the project does not depend on the skill being installed |
| `concepts/<L1NodeId>.md` | Optional: one file per large L1 subtree, once `CONCEPTS.md` passes ~1500 lines |

## Depth discipline

Levels are not capped at three. A level exists only to keep each diagram
readable and each concept pointable; depth is a consequence of breadth, never
a goal.

- **Breadth drives depth.** Every diagram owns 3–12 nodes (`min_nodes`,
  `max_nodes`). A diagram that needs more than 12 gets a new level by grouping
  its nodes. A would-be child with fewer than 3 nodes is not a level: write it
  into the parent node's Meaning.
- **Open a child diagram for node X only when one holds:**
  1. *Structure:* X splits into at least three parts, each with its own
     meaning, terms and code or tests, and the Captain could plausibly want to
     point at one part ("split `FoulCall`"). Structure diagrams use solid
     information-flow arrows labelled with what flows; a dotted arrow means one
     node checks or limits another.
  2. *Rule:* X is a rule with decisions or steps worth seeing. It gets an
     `L<n> rule · …` diagram (`flowchart TD`, decision diamonds, arrows
     labelled with answers). Rule diagrams are terminal.
- **Never open a child when** it mirrors the directory or class tree
  (concepts are not modules), the parts share one code symbol, the parts are
  parameters or constants (they belong in Meaning or DEFINITIONS), or it
  restates the parent's row.
- **Leaf test.** A node whose code is a handful of symbols in one or two files
  is a leaf. Below it is code, and `CODE.md` points there.
- **Skew is expected.** A simple branch may stop at L2 while a complex one
  reaches L5. Small tools usually need three levels; large engines four or
  five. Diagrams deeper than `review_depth` (default 5) get a checker notice:
  fold the level, or tell the Captain why it earns its place.
- **The DBC needs no DBC.** The format lives only in the checker's docstring.
  No index files, per-level files, node registries, meta-diagrams or
  conventions documents. Navigation is headings, parent IDs in headings and,
  for big maps, one subtree file per L1 node. If a reader needs a map to read
  the map, it is too deep: fold levels.

## Procedure

Follow the project's own context files for roles. If they assign an
orchestrator and workers, the orchestrator owns every DBC file and the
checkpoints; workers draft subtrees and return text.

1. **Survey.** Delegate to scouts when files are unknown; read planning
   documents by section. Collect: what the project is for (vision, README,
   plans); architecture and source layout; existing glossaries or terminology
   files; the test inventory (framework, how tests are named and where they
   live); the project's kind of evidence (fixtures, scenarios, exercises,
   benchmarks); plan and milestone naming (for `banned_patterns`).
2. **Checkpoint: L1.** Decide the location, the evidence file and the config.
   Draft L1: 5–12 nodes that together are the whole project, with labelled
   flows, plus one line per planned L2 diagram. Show the Captain the L1
   mermaid diagram, its node table and these choices as a short brief (issue,
   options with trade-offs, recommendation), then wait for her approval. L1 is
   her top-level frame; nothing below is drafted before she accepts it.
3. **Draft the subtrees.** Small projects: draft directly. Large projects:
   one worker per L1 node (or group of small ones), spawned in one batch. Each
   brief holds: the approved L1 table, the node to open, the depth discipline
   and the format contract (`skill://SetupDBC/check_dbc.py` docstring), the
   source paths and tests to map, the existing glossary, an ID prefix for rule
   nodes (e.g. `Fc` for a foul-call rule) to keep IDs unique, and the return
   format: diagrams with node tables, `CODE.md` rows, `TESTS.md` rows for the
   subtree, new terms with meanings. Workers do not write DBC files.
4. **Integrate.** Assemble `CONCEPTS.md` (and `concepts/*.md` if large).
   Statuses: `implemented` for what is built; `partial` only for what the
   current submilestone (or milestone) is working on; `planned` only for
   concepts a current plan commits to; no aspirational nodes. Write
   `DEFINITIONS.md`, migrating any existing glossary into it (the
   old file gets a one-line pointer, or is retired with the Captain's
   agreement); `CODE.md`; `TESTS.md` with every test; the evidence file with
   every fixture, scenario or exercise family. In big projects one evidence
   section per family is enough; list individual cases only where the project
   already does.
5. **Check.** Copy `check_dbc.py` into the DBC directory unchanged and write
   `dbc.toml`. Run `python3 <dbc-dir>/check_dbc.py` and fix the DBC files
   until it exits 0. Never weaken the checker to pass; a rule that looks wrong
   for this project goes to the Captain.
6. **Rules into context.** Add the DBC section below to the project's agent
   context file (`.omp/AGENTS.md`, `AGENTS.md` or `CLAUDE.md`, whichever the
   project uses), adapted to its roles, paths and evidence file. Point any
   existing glossary references in the context file at `DEFINITIONS.md`.
7. **Deliver.** Commit the DBC directory and the context-file change as one
   planning-only commit (push if the project's rules say so). Report: the L1
   diagram, the list of diagrams per level, the checker summary line, open
   questions marked **Open:** in `DEFINITIONS.md`, and any concepts you could
   not place.

## Writing rules

- **Meaning:** one or two plain sentences saying what the concept is, not how
  the code does it. **Terms:** the defined words the meaning relies on.
- **Node IDs:** CamelCase, stable. Renaming one changes its meaning: every
  reference in every DBC file moves in the same commit.
- **Changed meaning:** rewrite in place with the date and the old meaning
  ("from 2026-10-25; before, …"), so old receipts stay readable.
- **External nodes:** show a node owned elsewhere for context only, with
  Meaning "See <diagram title>" and empty Terms.
- **Status colors:** every diagram declares these four lines verbatim, and
  every node carries exactly one status class (`class A,B implemented`):
  ```
  classDef implemented fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
  classDef partial fill:#fff3b0,stroke:#b58900,color:#5c4400
  classDef planned stroke-dasharray:6 4
  classDef external fill:#eeeeee,stroke:#9e9e9e,stroke-dasharray:1 3,color:#616161
  ```
  Green: built. Yellow: in the current submilestone (or milestone), whether
  or not any of it is built yet. No color, dashed: not started. Grey, dotted:
  owned by another diagram. A parent takes the highest status among its
  children (planned < implemented < partial), so the current work shows
  yellow all the way up to L1. Text colors are set so the nodes stay readable
  in dark themes.
- `CONCEPTS.md` opens with a short "How to read the diagrams" section
  (levels, arrows, statuses, node IDs, the checker command). The other files
  open with one paragraph linking the other four.

## Context-file section

Adapt names, paths and roles; keep the rules.

```markdown
## DBC (Driven by Concepts)

`<dbc-dir>/` is the Captain's main tool for leading the project: she reasons
and decides in its concepts and terms. Keep it current without exception.

- `CONCEPTS.md` draws the project as mermaid flowcharts: L1 the whole project,
  one L2 diagram per L1 node, deeper levels only where the depth discipline
  allows (a structure node with at least three pointable parts, or a rule with
  steps). Each diagram has a node table (ID, meaning, terms, status) and owns
  3–12 nodes. No code, file names or plan names. The Captain's edits to it are
  directives: turn them into a plan or contract change; never revert them.
- `CODE.md` maps every built concept to files and symbols, never line numbers.
  `DEFINITIONS.md` is the glossary. `TESTS.md` lists every test with the nodes
  it guards. `<EVIDENCE>.md` lists every <fixture/scenario/exercise> family with
  its concept nodes and a Comments column.
- The format rules are the ones `<dbc-dir>/check_dbc.py` enforces; its
  docstring lists them. The DBC gets no meta-documents of its own.
- Statuses track the plan: `implemented` (green) is built, `partial`
  (yellow) is in the current submilestone, `planned` (uncolored) is not
  started. When a submilestone's contract is frozen, mark the nodes it will
  build or change `partial` in the same commit. The orchestrator owns all DBC
  files. After every implementation batch: add or split nodes for concepts
  the batch made real (respecting the depth discipline); fix `CODE.md` rows;
  give every new test and evidence entry its node IDs; run
  `python3 <dbc-dir>/check_dbc.py` and fix the DBC files (never the checker's
  rules) until it passes. When the submilestone closes, flip its `partial`
  nodes to `implemented`, or back to `planned` if they were deferred. A rule
  that looks wrong goes to the Captain.
- Any commit that introduces, renames, redefines or retires a term updates
  `DEFINITIONS.md` in the same commit; any commit that adds, changes or drops
  a test or evidence entry updates `TESTS.md` or `<EVIDENCE>.md`; any commit
  that changes what a node means or where it lives updates `CONCEPTS.md` or
  `CODE.md`. No term reaches the Captain in a message, plan or receipt before
  it is defined there.
- Node IDs are stable; renaming one is a change of meaning. A changed meaning
  is rewritten in place with the date and the old meaning. Open questions are
  marked **Open:** in the definition's row.
- Workers do not edit DBC files. They report concept impact (nodes built,
  code that fits no node, new terms) in their return message. The one
  exception: any agent that finds a problem with an evidence entry adds a
  dated, signed note to its Comments.
- Decisions put to the Captain use DBC terms. Read DBC files by section.
```

## Done when

- `python3 <dbc-dir>/check_dbc.py` exits 0 and prints its summary line.
- Every test and evidence family is listed; every implemented code-mapped
  node has a `CODE.md` row; every term on a node is defined.
- The Captain has approved L1, the context file carries the DBC section, and
  the setup is committed.
