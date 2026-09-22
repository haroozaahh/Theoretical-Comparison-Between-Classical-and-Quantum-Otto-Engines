# Quantum Otto Cycle Simulator


a Streamlit app comparing the efficiency of a two-level quantum Otto engine with an ideal gas classical Otto engine. the quantum simulation uses QuTiP to model two magnetic-field strokes and two thermalization strokes.


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

a quantum advantage can be seen from this application. it can be seen that from the first graph, the quantum otto engine reaches a larger efficiency than the classical otto engine under the chosen simulation parameters. the second graph also shows that as the cycle time increases, the quantum engine becomes more efficient before gradually approaching a maximum value. throughout the simulated range, its efficiency remains above that of the classical engine. this demonstrates a theoretical quantum advantage within the assumptions of this model, rather than proving that quantum otto engines are universally more efficient than classical engines.
