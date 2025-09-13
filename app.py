import streamlit as st import numpy as np import matplotlib.pyplot as plt

Title

st.title("☀️ Solar-Powered Dewatering Prototype") st.write("A simple simulation of solar PV powered pumping system under OPEX model")

Inputs

solar_irradiance = st.slider("Solar Irradiance (kW/m²)", 0.0, 1.2, 0.8, 0.1) duty_cycle = st.slider("Pump Duty Cycle (%)", 0, 100, 70, 5) water_inflow = st.number_input("Water Inflow Rate (Liters/sec)", 0.0, 50.0, 10.0, 1.0)

Constants & Calculations

panel_efficiency = 0.18  # 18% efficiency panel_area = 10  # m² small prototype panel area pv_power = solar_irradiance * panel_area * panel_efficiency  # kW

pump_efficiency = 0.75 pump_power = (pv_power * duty_cycle / 100) * pump_efficiency

water_pumped = (water_inflow * duty_cycle/100) * 3600 / 1000  # m³/hr

diesel_equiv = pump_power * 0.27  # liters diesel saved (approx) co2_reduction = diesel_equiv * 2.68  # kg CO2 saved

Outputs

st.subheader("Simulation Results") st.metric("PV Power Generated", f"{pv_power:.2f} kW") st.metric("Pump Power Utilized", f"{pump_power:.2f} kW") st.metric("Water Pumped", f"{water_pumped:.2f} m³/hr") st.metric("CO₂ Emission Reduction", f"{co2_reduction:.2f} kg/hr")

Status Panel

st.subheader("System Status") if pv_power > 0.2: st.success("✅ Pump Operating on Solar Power") else: st.warning("⚠️ Low Solar Power – Switching to Grid/Diesel Backup")

Graph

hours = np.arange(0, 24, 1) solar_profile = np.maximum(0, np.sin((hours-6)/12 * np.pi)) * solar_irradiance pump_output = solar_profile * panel_area * panel_efficiency * duty_cycle/100 * pump_efficiency

fig, ax = plt.subplots() ax.plot(hours, solar_profile, label="Solar Irradiance (kW/m²)") ax.plot(hours, pump_output, label="Pump Power Output (kW)") ax.set_xlabel("Time of Day (hrs)") ax.set_ylabel("Power / Output") ax.legend() st.pyplot(fig)

Footer

st.caption("Prototype Simulation – Solar Dewatering under OPEX Model")
