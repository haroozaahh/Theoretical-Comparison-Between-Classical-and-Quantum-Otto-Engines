# Quantum Otto Cycle Simulator


a Streamlit app comparing the efficiency of a two-level quantum Otto engine with an ideal gas classical Otto engine. the quantum simulation uses QuTiP to model two magnetic-field strokes and two thermalization strokes.

A Streamlit app comparing a two-level quantum Otto engine with a finite-time ideal-gas classical Otto engine. The quantum simulation uses QuTiP to model two magnetic-field strokes and two thermalization strokes. Both engines use the same hot and cold bath temperatures.


## Run locally

from the project directory, install the dependencies and start Streamlit:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

open the local URL printed by Streamlit. A virtual environment is recommended if you want to keep these dependencies separate from your other Python projects.

## Using the app


set a target efficiency and adjust the two engines independently in the sidebar. the quantum engine has bath temperatures, magnetic fields, stroke times, and transverse coupling. the classical engine has hot and cold temperatures, a compression ratio, and a heat capacity ratio. click **Run comparison** to see each engine's efficiency and its difference from the target in percentage points.

efficiency is work output divided by heat absorbed from the hot bath. the quantum result comes from a repeated cycle with finite stroke times. the classical result assumes an ideal gas with reversible adiabatic strokes. if an engine does not absorb heat and produce positive work, the app reports that it is not operating as an engine.

Set a target efficiency and adjust the shared bath temperatures and engine parameters in the sidebar. The quantum engine has magnetic fields, stroke times, and transverse coupling. The classical engine has a compression ratio, finite work-stroke time, thermalisation time, and heat capacity ratio. Click **Run comparison** to see each engine's efficiency and its difference from the target in percentage points.

Efficiency is work output divided by heat absorbed from the hot bath. The quantum result comes from a repeated cycle with finite stroke times and transverse coupling. The classical result is a finite-time ideal-gas Otto model with incomplete work strokes and thermalisation. Its work strokes approach, but do not instantly reach, the ideal adiabatic endpoints. The app shows efficiency and power versus a shared total cycle time. Power is reported in relative/model units because the quantum and classical energy scales are not directly matched. A region where quantum efficiency is higher is described only as a quantum advantage within the assumptions of these finite-time models. If an engine does not absorb heat and produce positive work, the app reports that it is not operating as an engine.
>>>>>>> a8ddb82 (df)
