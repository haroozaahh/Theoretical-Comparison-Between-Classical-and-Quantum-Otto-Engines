# Quantum Otto Cycle Simulator

<<<<<<< HEAD

a Streamlit app comparing the efficiency of a two-level quantum Otto engine with an ideal gas classical Otto engine. the quantum simulation uses QuTiP to model two magnetic-field strokes and two thermalization strokes.

=======
A Streamlit app comparing a two-level quantum Otto engine with a finite-time ideal-gas classical Otto engine. The quantum simulation uses QuTiP to model two magnetic-field strokes and two thermalization strokes. Both engines use the same hot and cold bath temperatures.
>>>>>>> 2016bda (Update Otto engine)

## Run locally

From the project directory, install the dependencies and start Streamlit:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed by Streamlit. A virtual environment is recommended if you want to keep these dependencies separate from your other Python projects.

## Using the app

<<<<<<< HEAD

set a target efficiency and shared hot and cold bath temperatures, then adjust each engine’s remaining parameters independently. the quantum engine has magnetic fields, stroke times, and transverse coupling, while the classical engine has a compression ratio, work-stroke time, thermalisation time, and heat capacity ratio. click run comparison to compare their efficiencies.

efficiency is work output divided by heat absorbed from the hot bath. the quantum result comes from a repeated finite-time cycle. the classical result uses a finite-time ideal-gas otto model with incomplete work strokes and incomplete thermalisation.

a quantum advantage can be seen from this application. it can be seen that from the first graph, the quantum otto engine reaches a larger efficiency than the classical otto engine under the chosen simulation parameters. the second graph also shows that as the cycle time increases, the quantum engine becomes more efficient before gradually approaching a maximum value. throughout the simulated range, its efficiency remains above that of the classical engine. this demonstrates a theoretical quantum advantage within the assumptions of this model, rather than proving that quantum otto engines are universally more efficient than classical engines.
=======
Set a target efficiency and adjust the shared bath temperatures and engine parameters in the sidebar. The quantum engine has magnetic fields, stroke times, and transverse coupling. The classical engine has a compression ratio, finite work-stroke time, thermalisation time, and heat capacity ratio. Click **Run comparison** to see each engine's efficiency and its difference from the target in percentage points.

Efficiency is work output divided by heat absorbed from the hot bath. The quantum result comes from a repeated cycle with finite stroke times and transverse coupling. The classical result is a finite-time ideal-gas Otto model with incomplete work strokes and thermalisation. Its work strokes approach, but do not instantly reach, the ideal adiabatic endpoints. The app shows efficiency and power versus a shared total cycle time. Power is reported in relative/model units because the quantum and classical energy scales are not directly matched. A region where quantum efficiency is higher is described only as a quantum advantage within the assumptions of these finite-time models. If an engine does not absorb heat and produce positive work, the app reports that it is not operating as an engine.
>>>>>>> 2016bda (Update Otto engine)
