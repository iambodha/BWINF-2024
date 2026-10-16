# BWINF 2024 · Algorithms and problem solving

Python implementations and original write-ups for **Tasks 2, 3, and 5** of the
43rd Bundeswettbewerb Informatik, Round 1 (2024/25). The projects explore three
different ideas: ordering constraints with graphs, choosing routes by interval
coverage, and navigating a corridor of periodically moving obstacles.

**[Run the examples](#try-it-locally)** · **[Algorithm notes](docs/ALGORITHMS.md)** ·
**[Original English report](Task5-English.pdf)** ·
**[Competition tasks](https://bwinf.de/bundeswettbewerb/43/)**

## The three problems

| Task | Problem | Approach in this repository | Source and write-up |
|---|---|---|---|
| **2 · Schwierigkeiten** | Put selected exam tasks in a consistent difficulty order, or detect a conflict. | Project each exam's ranking onto the selection; apply deterministic topological sorting. | [Python](Aufgabe2.py) · [German report](Aufgabe2.tex) |
| **3 · Wandertag** | Offer route lengths that satisfy as many members' preferred distance intervals as possible. | Rank interval endpoints by individual coverage, then search triples using cached membership masks. | [Python](Aufgabe3.py) · [German report](Aufgabe3.tex) |
| **5 · Das ägyptische Grabmal** | Find a way through sections that alternate between blocked and open. | Move forward when possible; backtrack to retry earlier sections in a later opening window. | [Python](Aufgabe5.py) · [English report](Task5-English.pdf) · [TeX](Aufgabe5.tex) |

Wandertag's default **60-candidate search is a heuristic**. It can miss the global
optimum. `--candidate-limit 0` searches all endpoints and is suitable for small
inputs; its combination count grows cubically. The tomb solver retains the
original search strategy and is checked against an independent reference on
small instances. This repository does not claim a complete correctness proof or
full official-suite validation. See the [algorithm notes](docs/ALGORITHMS.md).

## Try it locally

**Python 3.10 or newer.** The command-line solvers and tests use only the standard
library. Run these commands from the repository root:

```bash
git clone https://github.com/iambodha/BWINF-2024.git
cd BWINF-2024

python3 Aufgabe2.py examples/schwierigkeiten.txt
python3 Aufgabe3.py examples/wandern.txt
python3 Aufgabe5.py examples/grabmal.txt
```

On Windows, use `py` in place of `python3` if that is your Python launcher.
The included examples run offline. Nothing is downloaded at import time, and
no graphical window opens during a normal run.

### Example results

```text
Task 2
A C D E

Task 3
Route lengths: 3, 7, 11
Members covered: 6/6
Route 3: members 1, 2
Route 7: members 3, 4
Route 11: members 5, 6

Task 5
Section entry times: 5, 8, 12
Arrival time: 12 minutes
Warte 5 Minuten, laufe in den Abschnitt 1, Warte 3 Minuten,
laufe in den Abschnitt 2, Warte 4 Minuten, laufe zum Grabmal
```

Member IDs are 1-based input rows. A member accepting more than one route is
counted once in the total. See [all example fixtures](examples/README.md),
including a ranking with a cycle.

## Run your own input

Pass a local path to any solver. An explicit HTTP(S) URL is also supported, with
a 20-second network timeout. The [official material page](https://bwinf.de/bundeswettbewerb/43/)
contains the competition datasets; they are not bundled here.

```bash
python3 Aufgabe2.py path/to/schwierigkeiten0.txt path/to/schwierigkeiten1.txt
python3 Aufgabe3.py path/to/wandern.txt --candidate-limit 0
python3 Aufgabe5.py path/to/grabmal.txt --max-steps 1000000
```

| Task | Input format |
|---|---|
| 2 | Header `n m k`; `n` exam rankings such as `A < B < C`; one line containing the `k` selected task names. |
| 3 | Member count; one `minimum maximum` integer interval per member, inclusive at both ends. |
| 5 | Section count; one positive integer period per section (whitespace-separated). |

Use `--help` on any script for its options. Invalid input and missing files return
a nonzero exit code with an error message. A tomb search hitting its work limit
is reported as an interrupted search, not as proof that a route is impossible.

### Optional Wandertag plot

Only plotting needs an additional package. Use a virtual environment:

```bash
python3 -m venv .venv
# macOS / Linux; on Windows use .venv\Scripts\activate
source .venv/bin/activate
python -m pip install -r requirements-plot.txt
python Aufgabe3.py examples/wandern.txt --plot wandertag.png
```

The plot shows each member's acceptable interval and the chosen route lengths.
It is saved to a file rather than opening a window.

## Validation

```bash
python3 -m unittest discover -s tests -v
```

The offline suite checks command-line examples, cycle detection, omitted tasks
inside rankings, inclusive coverage, small candidate pools, and search limits.
It also compares exhaustive hiking searches with brute force on 50 seeded
inputs, and the tomb search with time-based reachability on 117 small period
sequences. These checks test behavior independently of the implementation.

[GitHub Actions](https://github.com/iambodha/BWINF-2024/actions/workflows/tests.yml)
runs the standard-library suite on Python 3.10, 3.12, and 3.13. Optional plotting
has a separate smoke check. The configured matrix is distinct from the Python
version used for any local test run.

## Project history and documentation

The original 2024 TeX reports, [task sheet](Aufgaben.pdf), and
[English Task 5 PDF](Task5-English.pdf) remain in place, with their original
team/author labels. They describe the competition-era implementations; the
[current algorithm guide](docs/ALGORITHMS.md) records maintenance changes,
complexity, and limitations. Task 4 (Krocket) has no implementation in this repo.

The maintenance pass adds explicit inputs, offline fixtures, importable solvers,
and tests. It also fixes lost ranking constraints across omitted tasks and makes
Wandertag's existing candidate cap visible. Git history retains the original code.

## License

Repository code is provided under the existing [Apache License 2.0](LICENSE).
The competition statement and task material originate from
[BWINF](https://bwinf.de/bundeswettbewerb/43/).
