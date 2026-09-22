# Quantum Otto Cycle Simulator

A Streamlit app comparing the efficiency of a two-level quantum Otto engine with an ideal gas classical Otto engine. The quantum simulation uses QuTiP to model two magnetic-field strokes and two thermalization strokes.

## Run locally

From the project directory, install the dependencies and start Streamlit:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed by Streamlit. A virtual environment is recommended if you want to keep these dependencies separate from your other Python projects.

## Using the app

Set a target efficiency and adjust the two engines independently in the sidebar. The quantum engine has bath temperatures, magnetic fields, stroke times, and transverse coupling. The classical engine has hot and cold temperatures, a compression ratio, and a heat capacity ratio. Click **Run comparison** to see each engine's efficiency and its difference from the target in percentage points.

Efficiency is work output divided by heat absorbed from the hot bath. The quantum result comes from a repeated cycle with finite stroke times. The classical result assumes an ideal gas with reversible adiabatic strokes. If an engine does not absorb heat and produce positive work, the app reports that it is not operating as an engine.
