# Python Visual Debugger

An educational step-by-step Python debugger with variable inspection.

## Phase 1 features

- Paste or edit Python code
- Line numbers
- "Trace Program" to run the tracer
- Next / Previous / Restart navigation
- Current line highlighting
- Live variable panel with change detection
- Restricted execution environment (whitelisted imports, no `eval`/`exec`/`open`)

## Install

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## How to use

1. The code panel is pre-loaded with an RREF example.
2. Click **Trace Program**.
3. Use **Next Step** / **Previous** to walk through execution.
4. Watch the variable panel to see values change.

## Architecture

- `engine/` — execution tracing and safety
- `ui/` — PySide6 widgets
- `examples/` — sample programs

The tracing engine is fully separated from the UI. The UI only
receives `Snapshot` objects and renders them.

## Roadmap

- **Phase 2:** loop and condition visualization, function call stack view, step explanations
- **Phase 3:** matrix detection and matrix viewer
- **Phase 4:** Linear Algebra mode (row operations, pivots, RREF)
- **Phase 5:** animation, more algorithms, plugin architecture
