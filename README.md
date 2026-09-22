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


set a target efficiency and shared hot and cold bath temperatures, then adjust each engine’s remaining parameters independently. the quantum engine has magnetic fields, stroke times, and transverse coupling, while the classical engine has a compression ratio, work-stroke time, thermalisation time, and heat capacity ratio. click run comparison to compare their efficiencies.

efficiency is work output divided by heat absorbed from the hot bath. the quantum result comes from a repeated finite-time cycle. the classical result uses a finite-time ideal-gas otto model with incomplete work strokes and incomplete thermalisation.

a quantum advantage can be seen from this application. it can be seen that from the first graph, the quantum otto engine reaches a larger efficiency than the classical otto engine under the chosen simulation parameters. the second graph also shows that as the cycle time increases, the quantum engine becomes more efficient before gradually approaching a maximum value. throughout the simulated range, its efficiency remains above that of the classical engine. this demonstrates a theoretical quantum advantage within the assumptions of this model, rather than proving that quantum otto engines are universally more efficient than classical engines.
