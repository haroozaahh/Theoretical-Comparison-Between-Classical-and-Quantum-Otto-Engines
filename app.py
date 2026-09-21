# File: /qotto-streamlit-app/qotto-streamlit-app/app.py

import streamlit as st
import numpy as np
import qutip as qt
import matplotlib.pyplot as plt

# --- Physics Helper Functions ---

sz = qt.sigmaz()
sx = qt.sigmax()

def get_hamiltonian(B, g):
    """Returns the static Hamiltonian for a given field B and coupling g."""
    return 0.5 * B * sz + 0.5 * g * sx

def get_thermal_state(H, T):
    """Calculates the thermal density matrix for Hamiltonian H at temperature T."""
    if T <= 0:
        return H.eigenstates()[1][0] * H.eigenstates()[1][0].dag()
    rho = (-H / T).expm()
    return rho / rho.tr()

def get_collapse_ops(H, T, gamma):
    """
    Derives the Lindblad jump operators in the instantaneous energy eigenbasis.
    """
    evals, ekets = H.eigenstates()
    delta_E = evals[1] - evals[0]
    
    # Avoid division by zero for T=0
    n_th = 1.0 / (np.exp(delta_E / T) - 1.0) if T > 0 else 0.0
    
    # Transition operators in energy eigenbasis
    sm_eig = ekets[0] * ekets[1].dag() 
    sp_eig = ekets[1] * ekets[0].dag() 
    
    C_down = np.sqrt(gamma * (n_th + 1)) * sm_eig
    C_up = np.sqrt(gamma * n_th) * sp_eig
    return [C_down, C_up]

# Time-dependent coefficients for the adiabatic strokes
def B_exp_coeff(t, args):
    return args['B_H'] + (args['B_C'] - args['B_H']) * (t / args['tau_adi'])

def B_comp_coeff(t, args):
    return args['B_C'] + (args['B_H'] - args['B_C']) * (t / args['tau_adi'])

# --- Streamlit UI Setup ---

st.set_page_config(page_title="Quantum Otto Cycle", layout="wide")
st.title("The Quantum Otto Cycle Simulator")
st.markdown("Interactive simulation of a quantum engine using a two-level system as the working fluid.")

with st.sidebar:
    st.header("Engine Parameters")
    T_H = st.slider("Hot Bath Temp ($T_H$)", 2.0, 15.0, 10.0, 0.5)
    T_C = st.slider("Cold Bath Temp ($T_C$)", 0.1, 2.0, 0.5, 0.1)
    B_H = st.slider("Max Mag Field Gap ($B_H$)", 2.0, 10.0, 5.0, 0.5)
    B_C = st.slider("Min Mag Field Gap ($B_C$)", 0.5, 3.0, 1.0, 0.1)
    
    st.header("Stroke Timings")
    tau_adi = st.slider("Adiabatic Stroke Time ($\\tau_{adi}$)", 0.5, 20.0, 5.0, 0.5)
    tau_iso = st.slider("Isochoric Stroke Time ($\\tau_{iso}$)", 1.0, 20.0, 10.0, 1.0)
    
    st.header("Quantum Friction")
    g = st.slider("Transverse Coupling ($g$)", 0.1, 2.0, 0.5, 0.1, 
                  help="Off-diagonal coupling that causes Landau-Zener non-adiabatic transitions.")
    gamma = 1.0 # Thermalization coupling rate

# --- Simulation Logic ---

if st.button("Run Simulation", type="primary"):
    with st.spinner("Solving Master Equations..."):
        
        # 1. Setup Static Hamiltonians and Initial State
        H_hot = get_hamiltonian(B_H, g)
        H_cold = get_hamiltonian(B_C, g)
        
        rho_initial = get_thermal_state(H_hot, T_H)
        
        # Time arrays
        tlist_adi = np.linspace(0, tau_adi, 50)
        tlist_iso = np.linspace(0, tau_iso, 50)
        args_cycle = {'B_H': B_H, 'B_C': B_C, 'tau_adi': tau_adi}
        
        # Stroke 1: Adiabatic Expansion
        H_exp = [[0.5 * sz, B_exp_coeff], [0.5 * g * sx, '1']]
        result_exp = qt.mesolve(H_exp, rho_initial, tlist_adi, args=args_cycle)
        rho_after_exp = result_exp.states[-1]
        
        # Stroke 2: Cold Isochoric Thermalization
        c_ops_cold = get_collapse_ops(H_cold, T_C, gamma)
        result_cold_iso = qt.mesolve(H_cold, rho_after_exp, tlist_iso, c_ops=c_ops_cold)
        rho_after_cold = result_cold_iso.states[-1]
        
        # Stroke 3: Adiabatic Compression
        H_comp = [[0.5 * sz, B_comp_coeff], [0.5 * g * sx, '1']]
        result_comp = qt.mesolve(H_comp, rho_after_cold, tlist_adi, args=args_cycle)
        rho_after_comp = result_comp.states[-1]
        
        # Stroke 4: Hot Isochoric Thermalization
        c_ops_hot = get_collapse_ops(H_hot, T_H, gamma)
        result_hot_iso = qt.mesolve(H_hot, rho_after_comp, tlist_iso, c_ops=c_ops_hot)
        rho_after_hot = result_hot_iso.states[-1]