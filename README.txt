
<div align="center">

  <h1>⚡ EV Battery Performance Simulation</h1>

  <h3>Understanding Electric Vehicle Battery Charging, Discharging & State of Charge</h3>

  <p>
    A Python-based simulation that demonstrates how an electric vehicle's
    battery performs during charging and driving.
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" alt="Python">
    <img src="https://img.shields.io/badge/NumPy-Used-orange?logo=numpy" alt="NumPy">
    <img src="https://img.shields.io/badge/Matplotlib-Visualization-green" alt="Matplotlib">
    <img src="https://img.shields.io/badge/Project-Completed-success" alt="Completed">
  </p>

</div>

---

## 📌 About the Project

**EV Battery Performance Simulation** is a Python-based project developed to understand and demonstrate the performance of an Electric Vehicle (EV) battery.

The project simulates battery charging and discharging conditions and calculates important battery parameters such as:

- Initial State of Charge (SOC)
- SOC after charging
- Energy consumed during driving
- Remaining battery energy
- Final State of Charge
- Estimated remaining driving range

The simulation helps explain how battery energy changes when an electric vehicle is charged and driven over a particular distance.

## 🎯 Project Objectives

- Understand the working principle of EV batteries.
- Simulate battery charging and discharging.
- Calculate the State of Charge (SOC).
- Estimate energy consumption during driving.
- Calculate the remaining battery capacity.
- Estimate the remaining driving range.
- Apply Python programming to a real-world EV application.

## ⚙️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| NumPy | Numerical calculations |
| Matplotlib | Data visualization |

## 🔋 How the Simulation Works

The simulation follows these steps:

<div align="center">

  <h3>Battery Performance Workflow</h3>

  <p>🔋 Initial Battery State</p>
  <p>⬇️</p>
  <p>⚡ Battery Charging</p>
  <p>⬇️</p>
  <p>📊 Calculate SOC After Charging</p>
  <p>⬇️</p>
  <p>🚗 Simulate Vehicle Driving</p>
  <p>⬇️</p>
  <p>⚡ Calculate Energy Consumption</p>
  <p>⬇️</p>
  <p>🔋 Calculate Remaining Battery Energy</p>
  <p>⬇️</p>
  <p>📍 Estimate Remaining Driving Range</p>

</div>

## 🧮 Mathematical Calculations

The simulation uses the following basic formulas:

**1. Energy Consumed**

Energy Consumed (kWh) = Distance (km) × Energy Consumption Rate (kWh/km)

**2. Remaining Battery Energy**

Remaining Energy = Battery Capacity × (Final SOC / 100)

**3. Final State of Charge**

Final SOC (%) = (Remaining Energy / Battery Capacity) × 100

**4. Estimated Remaining Range**

Remaining Range = Remaining Energy / Energy Consumption Rate

## 📊 Simulation Results

The following table shows the output from the completed simulation.

| Parameter | Simulation Result |
|---|---:|
| Battery Capacity | 60 kWh |
| Initial SOC | 30% |
| SOC After Charging | 51% |
| Driving Distance | 100 km |
| Energy Consumed | 15 kWh |
| Final SOC | 26% |
| Remaining Energy | 15.60 kWh |
| Estimated Remaining Range | 104 km |

### 🔍 Understanding the Results

- The battery initially contains 30% charge.
- After charging, the battery SOC increases to 51%.
- The vehicle travels a distance of 100 km.
- During driving, 15 kWh of energy is consumed.
- After the journey, the battery retains 26% charge.
- The remaining energy is 15.60 kWh.
- Based on the simulated energy consumption rate, the vehicle can travel approximately another 104 km.

## 💡 Key Features

- **Battery Charging Simulation:** Demonstrates an increase in battery SOC.
- **Battery Discharging Simulation:** Calculates energy used during vehicle operation.
- **SOC Calculation:** Tracks the battery's remaining charge percentage.
- **Energy Monitoring:** Calculates consumed and remaining energy.
- **Range Estimation:** Estimates how far the vehicle can travel with its remaining charge.
- **Python-Based Implementation:** Uses simple mathematical calculations and programming concepts.

## 🚀 How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/SRINIVASKALYAN30/EV-Battery-Performance-Simulation.git
```

### 2. Open the Project Folder

```bash
cd EV-Battery-Performance-Simulation
```

### 3. Install Required Libraries

```bash
pip install numpy matplotlib
```

### 4. Run the Python Program

Use the main Python simulation file:

```bash
python main.py
```

If your main Python file has a different name, replace `main.py` with its actual filename.

## 🌍 Real-World Applications

This type of simulation helps understand:

- Electric vehicle battery monitoring.
- Battery charge and discharge behaviour.
- Driving range estimation.
- Energy consumption analysis.
- Basic EV battery performance evaluation.

## ⚠️ Limitations

This is an educational simulation based on simplified mathematical calculations.

Actual EV battery performance may vary depending on:

- Driving speed and acceleration.
- Road conditions and terrain.
- Ambient and battery temperature.
- Battery age and degradation.
- Vehicle weight and driving style.
- Charging and discharging efficiency.

The estimated range is a theoretical value and may differ from the actual range of an electric vehicle.

## 🔮 Future Enhancements

- Develop an interactive battery monitoring dashboard.
- Add real-time SOC visualization.
- Include different battery capacities.
- Simulate different driving conditions.
- Add temperature-dependent battery behaviour.
- Integrate real-world EV battery datasets.

## 👨‍💻 Project Information

**Project Name:** EV Battery Performance Simulation

**Domain:** Electric Vehicles and Battery Technology

**Programming Language:** Python

**Project Type:** Simulation-Based Mini Project

**Status:** Completed

---

<div align="center">

  <h3>⚡ Powering the Future of Electric Mobility ⚡</h3>

  <p>Developed as an academic mini-project to explore EV battery performance using Python.</p>

  <p>
    <a href="https://github.com/SRINIVASKALYAN30">
      GitHub Profile
    </a>
  </p>

  <p><b>Thank you for visiting this repository!</b></p>

</div>
