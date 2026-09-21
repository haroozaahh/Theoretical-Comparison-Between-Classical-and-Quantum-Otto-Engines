# Quantum Otto Cycle Simulator

A Streamlit app for exploring a quantum Otto cycle with a two-level system as its working fluid. The simulation uses QuTiP to model two magnetic-field strokes and two thermalization strokes.

## Run locally

From the project directory, install the dependencies and start Streamlit:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed by Streamlit. A virtual environment is recommended if you want to keep these dependencies separate from your other Python projects.

## Using the app

Set the hot and cold bath temperatures, maximum and minimum magnetic-field gaps, stroke durations, and transverse coupling in the sidebar. Click **Run Simulation** to solve one cycle. The transverse coupling controls transitions during the magnetic-field strokes.

**Current state:** The app runs the four strokes but does not yet display plots or numerical results after the simulation finishes.
