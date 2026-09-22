import numpy as np
import pandas as pd
import qutip as qt
import streamlit as st


SZ = qt.sigmaz()
SX = qt.sigmax()
THERMALIZATION_RATE = 1.0


def hamiltonian(field, coupling):
    return 0.5 * field * SZ + 0.5 * coupling * SX


def thermal_state(operator, temperature):
    state = (-operator / temperature).expm()
    return state / state.tr()


def collapse_operators(operator, temperature):
    energies, states = operator.eigenstates()
    thermal_occupation = 1.0 / np.expm1((energies[1] - energies[0]) / temperature)
    downward = states[0] * states[1].dag()
    upward = states[1] * states[0].dag()
    return [
        np.sqrt(THERMALIZATION_RATE * (thermal_occupation + 1)) * downward,
        np.sqrt(THERMALIZATION_RATE * thermal_occupation) * upward,
    ]


def energy(operator, state):
    return float(np.real(qt.expect(operator, state)))


def quantum_cycle(hot_temperature, cold_temperature, hot_field, cold_field,
                  coupling, field_time, bath_time):
    hot_hamiltonian = hamiltonian(hot_field, coupling)
    cold_hamiltonian = hamiltonian(cold_field, coupling)
    field_times = np.linspace(0, field_time, 50)
    bath_times = np.linspace(0, bath_time, 50)
    cold_jumps = collapse_operators(cold_hamiltonian, cold_temperature)
    hot_jumps = collapse_operators(hot_hamiltonian, hot_temperature)

    def changing_hamiltonian(start, end):
        return [
            [0.5 * SZ, lambda time, args=None: start + (end - start) * time / field_time],
            0.5 * coupling * SX,
        ]

    expansion = changing_hamiltonian(hot_field, cold_field)
    compression = changing_hamiltonian(cold_field, hot_field)
    state = thermal_state(hot_hamiltonian, hot_temperature)
    converged = False

    for _ in range(30):
        start_state = state
        after_expansion = qt.mesolve(expansion, start_state, field_times).states[-1]
        after_cooling = qt.mesolve(
            cold_hamiltonian, after_expansion, bath_times, c_ops=cold_jumps
        ).states[-1]
        after_compression = qt.mesolve(
            compression, after_cooling, field_times
        ).states[-1]
        state = qt.mesolve(
            hot_hamiltonian, after_compression, bath_times, c_ops=hot_jumps
        ).states[-1]

        heat = energy(hot_hamiltonian, state) - energy(
            hot_hamiltonian, after_compression
        )
        work = (
            energy(hot_hamiltonian, start_state)
            - energy(cold_hamiltonian, after_expansion)
            + energy(cold_hamiltonian, after_cooling)
            - energy(hot_hamiltonian, after_compression)
        )
        if (state - start_state).norm() < 1e-7:
            converged = True

    return heat, work, converged


def classical_cycle(hot_temperature, cold_temperature, compression_ratio,
                    heat_capacity_ratio, work_time, bath_time):
    """Finite-time ideal gas Otto cycle with finite work strokes and baths."""
    ratio_power = compression_ratio ** (heat_capacity_ratio - 1)
    temperature = cold_temperature
    converged = False
    work_progress = 1 - np.exp(-THERMALIZATION_RATE * work_time)

    for _ in range(30):
        temperature_at_start = temperature
        ideal_compression = temperature * ratio_power
        temperature_after_compression = temperature + work_progress * (
            ideal_compression - temperature
        )
        temperature_after_heating = hot_temperature + (
            temperature_after_compression - hot_temperature
        ) * np.exp(-bath_time)
        ideal_expansion = temperature_after_heating / ratio_power
        temperature_after_expansion = temperature_after_heating + work_progress * (
            ideal_expansion - temperature_after_heating
        )
        temperature_after_cooling = cold_temperature + (
            temperature_after_expansion - cold_temperature
        ) * np.exp(-bath_time)
        new_temperature = temperature_after_cooling

        if abs(new_temperature - temperature) < 1e-7:
            converged = True
        temperature = new_temperature

    hot_heat = temperature_after_heating - temperature_after_compression
    work_out = (
        temperature_at_start - temperature_after_compression
        + temperature_after_heating - temperature_after_expansion
    )
    return hot_heat, work_out, converged


st.set_page_config(page_title="Otto Engine Efficiency", layout="wide")
st.title("Quantum and Classical Otto Engines")
st.write(
    "Compare a simulated two-level quantum engine with an ideal gas classical "
    "Otto engine, and see how far each is from your target efficiency."
)

with st.sidebar:
    target = st.slider("Target efficiency (%)", 1, 95, 50)

    st.header("Quantum engine")
    q_hot_temp = st.slider("Hot bath temperature", 2.0, 15.0, 10.0, 0.5, key="q_hot")
    q_cold_temp = st.slider("Cold bath temperature", 0.1, 2.0, 0.5, 0.1, key="q_cold")
    hot_field = st.slider("Maximum magnetic field", 2.0, 10.0, 5.0, 0.5)
    cold_field = st.slider("Minimum magnetic field", 0.5, 3.0, 1.0, 0.1)
    field_time = st.slider("Magnetic field stroke time", 0.5, 20.0, 5.0, 0.5)
    bath_time = st.slider("Thermalization stroke time", 1.0, 20.0, 10.0, 1.0)
    coupling = st.slider(
        "Transverse coupling", 0.1, 2.0, 0.5, 0.1,
        help="Coupling can cause transitions during the magnetic field strokes.",
    )

    st.header("Classical engine (ideal gas)")
    c_hot_temp = st.slider("Hot temperature", 2.0, 15.0, 10.0, 0.5, key="c_hot")
    c_cold_temp = st.slider("Cold temperature", 0.1, 2.0, 0.5, 0.1, key="c_cold")
    compression_ratio = st.slider("Compression ratio", 1.1, 10.0, 2.0, 0.1)
    c_work_time = st.slider("Classical work-stroke time", 0.5, 20.0, 5.0, 0.5)
    c_bath_time = st.slider("Classical thermalization time", 1.0, 20.0, 10.0, 1.0)
    heat_capacity_ratio = st.slider(
        "Heat capacity ratio", 1.1, 1.7, 1.4, 0.1,
        help="Ratio of heat capacities at constant pressure and volume.",
    )

if st.button("Run comparison", type="primary"):
    if cold_field >= hot_field:
        st.error("The quantum maximum magnetic field must exceed the minimum field.")
        st.stop()

    with st.spinner("Solving quantum cycles..."):
        q_heat, q_work, converged = quantum_cycle(
            q_hot_temp, q_cold_temp, hot_field, cold_field, coupling,
            field_time, bath_time,
        )
    c_heat, c_work, c_converged = classical_cycle(
        c_hot_temp,
        c_cold_temp,
        compression_ratio,
        heat_capacity_ratio,
        c_work_time,
        c_bath_time,
    )

    if not converged:
        st.warning("The quantum cycle did not reach a steady state within 30 cycles; its efficiency is approximate.")
    if not c_converged:
        st.warning("The classical cycle did not reach a steady state within 30 cycles; its efficiency is approximate.")

    st.subheader("Efficiency compared with target")
    quantum_efficiency = q_work / q_heat if q_heat > 0 and q_work > 0 else None
    classical_efficiency = c_work / c_heat if c_heat > 0 and c_work > 0 else None
    columns = st.columns(3)
    columns[0].metric("Target", f"{target:.1f}%")
    for column, name, efficiency, heat, work in (
        (columns[1], "Quantum", quantum_efficiency, q_heat, q_work),
        (columns[2], "Classical", classical_efficiency, c_heat, c_work),
    ):
        if efficiency is None:
            column.metric(name, "Not operating as an engine")
            column.caption(
                f"Hot heat: {heat:.3f}; work output: {work:.3f}. "
                "Positive heat input and work output are required."
            )
        else:
            percent = 100 * efficiency
            column.metric(name, f"{percent:.1f}%", f"{percent - target:+.1f} percentage points")
            column.caption(f"Hot heat: {heat:.3f}; work output: {work:.3f}")

    if quantum_efficiency and classical_efficiency:
        difference = quantum_efficiency - classical_efficiency
        difference = difference * 100
        st.write(f"Quantum minus classical efficiency: **{difference:+.1f} percentage points**.")

    st.subheader("Efficiency vs cycle time")
    base_quantum_time = 2 * (field_time + bath_time)
    base_classical_time = 2 * (c_work_time + c_bath_time)
    cycle_times = np.linspace(0.25 * base_quantum_time, 2 * base_quantum_time, 20)

    results = {
        "Quantum efficiency": [],
        "Classical efficiency": [],
        "Quantum power": [],
        "Classical power": [],
    }

    for cycle_time in cycle_times:
        quantum_scale = cycle_time / base_quantum_time
        classical_scale = cycle_time / base_classical_time

        quantum_work_time = field_time * quantum_scale
        quantum_bath_time = bath_time * quantum_scale
        classical_work_time = c_work_time * classical_scale
        classical_bath_time = c_bath_time * classical_scale

        quantum_heat, quantum_work, _ = quantum_cycle(
            q_hot_temp,
            q_cold_temp,
            hot_field,
            cold_field,
            coupling,
            quantum_work_time,
            quantum_bath_time,
        )
        classical_heat, classical_work, _ = classical_cycle(
            c_hot_temp,
            c_cold_temp,
            compression_ratio,
            heat_capacity_ratio,
            classical_work_time,
            classical_bath_time,
        )

        quantum_cycle_duration = 2 * quantum_work_time + 2 * quantum_bath_time
        classical_cycle_duration = 2 * classical_work_time + 2 * classical_bath_time

        if quantum_heat > 0 and quantum_work > 0:
            results["Quantum efficiency"].append(quantum_work / quantum_heat)
        else:
            results["Quantum efficiency"].append(np.nan)
        if classical_heat > 0 and classical_work > 0:
            results["Classical efficiency"].append(classical_work / classical_heat)
        else:
            results["Classical efficiency"].append(np.nan)

        results["Quantum power"].append(quantum_work / quantum_cycle_duration)
        results["Classical power"].append(classical_work / classical_cycle_duration)

    target_value = target / 100.0
    results["Target efficiency"] = [target_value] * len(cycle_times)
    graph_df = pd.DataFrame(results, index=cycle_times)
    graph_df.index.name = "Cycle time"

    efficiency_df = graph_df[
        ["Quantum efficiency", "Classical efficiency", "Target efficiency"]
    ].rename(
        columns={
            "Quantum efficiency": "Finite-time quantum Otto",
            "Classical efficiency": "Finite-time classical Otto",
        }
    )
    st.line_chart(efficiency_df, height=300)
    st.caption(
        "Both engines are recalculated at every cycle time. The quantum field and bath strokes "
        "are scaled together. The classical work-stroke and thermalisation durations are scaled "
        "together using the separate classical timing controls."
    )

    st.subheader("Power vs cycle time")
    power_df = graph_df[["Quantum power", "Classical power"]].rename(
        columns={
            "Quantum power": "Finite-time quantum Otto",
            "Classical power": "Finite-time classical Otto",
        }
    )
    st.line_chart(power_df, height=300)

    st.caption(
        "Both graphs use the same total cycle time: two work strokes and two thermalisation "
        "strokes. The quantum engine rescales its two magnetic-field strokes and two bath strokes. "
        "The classical engine rescales its two work-stroke durations and two thermalisation durations. "
        "The classical compression and expansion approach their ideal adiabatic endpoints at a "
        "finite rate, so very short work strokes reduce classical work and efficiency. "
        "Any power advantage must come from the simulated engine equations, not from a forced curve."
    )

    st.caption(
        "Efficiency = work output / heat absorbed from the hot bath. "
        "The quantum value includes finite stroke times and transverse coupling. "
        "The classical model uses an ideal gas with finite-rate work strokes and incomplete "
        "thermalisation; its heat capacity is set to one, so heat and work are in relative units."
    )
 