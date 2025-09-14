import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Pump & Solar Dashboard", layout="wide")

st.title("🚰 Smart Pump & Solar Monitoring Dashboard")

# ---------------- Sidebar Inputs ---------------- #
st.sidebar.header("🔧 Control Panel")

# Water level input
water_level = st.sidebar.slider("Water Level (%)", 0, 100, 50)

# Pump inputs
flow = st.sidebar.number_input("Flow Rate (m³/s)", 0.01, 1.0, 0.2, step=0.01)
head = st.sidebar.number_input("Head (m)", 1, 100, 30)
efficiency = st.sidebar.slider("Pump Efficiency (%)", 10, 90, 70)

# Solar inputs
solar_irradiance = st.sidebar.slider("Solar Irradiance (W/m²)", 0, 1200, 800)
panel_area = st.sidebar.number_input("PV Panel Area (m²)", 1, 50, 10)
panel_eff = st.sidebar.slider("PV Efficiency (%)", 5, 25, 15)

# Diesel / OPEX costs
diesel_cost = st.sidebar.number_input("Diesel Cost per kWh (₹)", 10, 30, 18)
solar_opex = st.sidebar.number_input("Solar OPEX per kWh (₹)", 0, 5, 1)

# ---------------- Calculations ---------------- #
pump_power = (flow * head * 9.81) / (efficiency / 100)  # kW
solar_power = (solar_irradiance * panel_area * (panel_eff / 100)) / 1000  # kW
diesel_equivalent = solar_power
co2_saved = diesel_equivalent * 0.27  # kg CO₂ saved
cost_saving = (diesel_cost - solar_opex) * solar_power

# ---------------- TOP SECTION ---------------- #
st.subheader("💧 Water Tank & Pump Status")

col1, col2 = st.columns([2, 1])

with col1:
    st.progress(water_level / 100)  # gauge-like progress bar
    st.write(f"Tank Level: **{water_level}%**")

with col2:
    if water_level < 30:
        st.error("🚫 Pump OFF (Low Water Level)")
    else:
        st.success("✅ Pump ON (Sufficient Water)")

# ---------------- MIDDLE SECTION ---------------- #
st.subheader("📊 Solar vs Pump Performance")

time = np.arange(0, 24, 1)
solar_profile = (np.maximum(0, np.sin((time - 6) / 12 * np.pi))) * solar_power
pump_profile = np.random.normal(pump_power, 0.2, len(time))

fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(time - 0.2, solar_profile, width=0.4, label="Solar PV Generation (kW)", color="orange")
ax.bar(time + 0.2, pump_profile, width=0.4, label="Pump Power Output (kW)", color="blue")

ax.set_xlabel("Hour of Day")
ax.set_ylabel("Power (kW)")
ax.legend()
st.pyplot(fig)

# ---------------- BOTTOM SECTION ---------------- #
st.subheader("🌱 Sustainability & Cost Impact")

col3, col4 = st.columns(2)

with col3:
    st.metric("🌍 Carbon Emissions Avoided", f"{co2_saved:.2f} kg CO₂/hr")
    st.caption("Eco-friendly: CO₂ reduced compared to diesel pump.")

with col4:
    st.metric("💰 OPEX Savings", f"₹{cost_saving:.2f} per hour")
    st.caption("Cost advantage of Solar vs Diesel OPEX model.")

# ---------------- Footer ---------------- #
st.caption("Prototype Simulation – Solar Dewatering under OPEX Model")
