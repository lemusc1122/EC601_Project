# Quantum Circuit Builder

A desktop learning prototype for exploring quantum gates, example circuits, local simulations, and a BB84 plus one-time-pad teaching demonstration. The interface currently supports English, Spanish, and Arabic.

## Run the prototype

From macOS or Linux, in the repository root:

```bash
./install_dependencies.bash
source .venv/bin/activate
python prototype.py
```

See [gettingStarted.md](gettingStarted.md) for setup notes and the optional IBM Quantum hardware example.

## Repository contents

- `prototype.py` — desktop application and local demonstrations.
- `firstQiskitScript.py` — optional Bell-state job submitted to IBM Quantum hardware.
- `install_dependencies.bash` — creates `.venv` and installs dependencies for the local prototype.
- `Feedback/` — feedback submitted in the application is saved here as local Markdown issues.
- `docs/` — project documentation and references.
- `SPRINT1.md`, `TEAM.md`, and `brainstormingPart*.md` — project planning and notes.
