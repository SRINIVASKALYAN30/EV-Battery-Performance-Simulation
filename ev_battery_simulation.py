
import numpy as np
import matplotlib.pyplot as plt
import os

# Create folders for saving results
os.makedirs("graphs", exist_ok=True)
os.makedirs("results", exist_ok=True)

# EV Battery Specifications
battery_capacity = 60
initial_soc = 30

# Charging specifications
charging_power = 7
charging_time = 2
charging_efficiency = 0.90

# Driving specifications
driving_distance = 100
energy_consumption = 0.15

# Battery charging simulation
time = np.linspace(0, charging_time, 21)

charging_soc = initial_soc + (
    charging_power * charging_efficiency * time
    / battery_capacity * 100
)

charging_soc = np.clip(charging_soc, 0, 100)

# Battery discharging simulation
distance = np.linspace(0, driving_distance, 101)

energy_used = distance * energy_consumption

driving_soc = charging_soc[-1] - (
    energy_used / battery_capacity * 100
)

driving_soc = np.clip(driving_soc, 0, 100)

# Final calculations
charged_soc = charging_soc[-1]
final_soc = driving_soc[-1]

remaining_energy = battery_capacity * final_soc / 100
estimated_range = remaining_energy / energy_consumption

# Display results
print("\n===== EV BATTERY SIMULATION =====")

print(f"Battery Capacity: {battery_capacity} kWh")
print(f"Initial Battery SOC: {initial_soc:.2f}%")
print(f"Charging Power: {charging_power} kW")
print(f"Charging Time: {charging_time} hours")
print(f"SOC After Charging: {charged_soc:.2f}%")

print(f"\nDriving Distance: {driving_distance} km")
print(f"Energy Consumed: {energy_used[-1]:.2f} kWh")
print(f"Final Battery SOC: {final_soc:.2f}%")
print(f"Remaining Energy: {remaining_energy:.2f} kWh")
print(f"Estimated Remaining Range: {estimated_range:.2f} km")

# Charging graph
plt.figure(figsize=(9, 5))
plt.plot(time, charging_soc, marker="o")
plt.title("EV Battery Charging Simulation")
plt.xlabel("Charging Time (Hours)")
plt.ylabel("Battery SOC (%)")
plt.grid(True)
plt.ylim(0, 100)
plt.savefig("graphs/charging_graph.png")
plt.show()

# Discharging graph
plt.figure(figsize=(9, 5))
plt.plot(distance, driving_soc)
plt.title("EV Battery Discharging During Driving")
plt.xlabel("Driving Distance (km)")
plt.ylabel("Battery SOC (%)")
plt.grid(True)
plt.ylim(0, 100)
plt.savefig("graphs/discharging_graph.png")
plt.show()

# Save results
with open("results/simulation_results.txt", "w") as file:
    file.write("EV BATTERY SIMULATION RESULTS\n")
    file.write(f"Battery Capacity: {battery_capacity} kWh\n")
    file.write(f"Initial SOC: {initial_soc:.2f}%\n")
    file.write(f"SOC After Charging: {charged_soc:.2f}%\n")
    file.write(f"Driving Distance: {driving_distance} km\n")
    file.write(f"Energy Consumed: {energy_used[-1]:.2f} kWh\n")
    file.write(f"Final SOC: {final_soc:.2f}%\n")
    file.write(f"Remaining Energy: {remaining_energy:.2f} kWh\n")
    file.write(f"Estimated Remaining Range: {estimated_range:.2f} km\n")

print("\nSimulation completed successfully!")
print("Graphs saved in the graphs folder.")
print("Results saved in the results folder.")
