# Small, offline examples

These fixtures are maintained demonstration inputs, not the official test suite.
The tomb periods reproduce the small example in the task statement; the ranking
and hiking inputs are synthetic. Download the full competition inputs from the
[official material page](https://bwinf.de/bundeswettbewerb/43/).

| File | What it exercises | Expected result |
|---|---|---|
| `schwierigkeiten.txt` | An omitted task inside an exam ranking | `A C D E` |
| `schwierigkeiten-cycle.txt` | Conflicting selected-task rankings | `NO GOOD ORDERING POSSIBLE` |
| `wandern.txt` | Three separate clusters of preferred distances | Routes `3, 7, 11`; all 6 members covered |
| `grabmal.txt` | Waiting between periodically blocked sections | Entry times `5, 8, 12`; arrival after 12 minutes |

Run commands from the repository root. Other optimal route choices or valid
rankings can exist; the fixtures above describe this implementation's tie-breaks.
