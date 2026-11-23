
import matplotlib.pyplot as plt
import numpy as np
import os

# Create output folders
os.makedirs("graphs", exist_ok=True)
os.makedirs("results", exist_ok=True)

# EV battery specifications
battery_capacity = 60
initial_soc = 30
target_soc = 80

# Charging specifications
slow_charger = 7
fast_charger = 50

slow_efficiency = 0.90
fast_efficiency = 0.95

# Calculate required energy
energy_required = (
    battery_capacity * (target_soc - initial_soc) / 100
)

# Calculate charging time
slow_time = energy_required / (
    slow_charger * slow_efficiency
)

fast_time = energy_required / (
    fast_charger * fast_efficiency
)

# Display results
print("\n===== EV CHARGING COMPARISON =====")

print(f"Battery Capacity: {battery_capacity} kWh")
print(f"Initial SOC: {initial_soc}%")
print(f"Target SOC: {target_soc}%")
print(f"Energy Required: {energy_required:.2f} kWh")

print("\nSlow Charging")
print(f"Charger Power: {slow_charger} kW")
print(f"Charging Time: {slow_time:.2f} hours")

print("\nFast Charging")
print(f"Charger Power: {fast_charger} kW")
print(f"Charging Time: {fast_time:.2f} hours")
print(f"Time Saved: {slow_time - fast_time:.2f} hours")

# Charging time comparison graph
plt.figure(figsize=(9, 5))

plt.bar(
    ["Slow Charging (7 kW)", "Fast Charging (50 kW)"],
    [slow_time, fast_time]
)

plt.title("EV Slow vs Fast Charging Time")
plt.ylabel("Charging Time (Hours)")
plt.grid(axis="y")

plt.savefig("graphs/charging_comparison.png")
plt.show()

# Charging progress simulation
time_slow = np.linspace(0, slow_time, 100)
time_fast = np.linspace(0, fast_time, 100)

soc_slow = initial_soc + (
    time_slow / slow_time * (target_soc - initial_soc)
)

soc_fast = initial_soc + (
    time_fast / fast_time * (target_soc - initial_soc)
)

plt.figure(figsize=(9, 5))

plt.plot(time_slow, soc_slow, label="Slow Charging (7 kW)")
plt.plot(time_fast, soc_fast, label="Fast Charging (50 kW)")

plt.title("EV Battery Charging Progress")
plt.xlabel("Time (Hours)")
plt.ylabel("Battery SOC (%)")
plt.legend()
plt.grid(True)

plt.savefig("graphs/charging_progress.png")
plt.show()

# Save results
with open("results/charging_comparison.txt", "w") as file:
    file.write("EV CHARGING COMPARISON RESULTS\n")
    file.write(f"Battery Capacity: {battery_capacity} kWh\n")
    file.write(f"Initial SOC: {initial_soc}%\n")
    file.write(f"Target SOC: {target_soc}%\n")
    file.write(f"Energy Required: {energy_required:.2f} kWh\n")
    file.write(f"Slow Charging Time: {slow_time:.2f} hours\n")
    file.write(f"Fast Charging Time: {fast_time:.2f} hours\n")
    file.write(f"Time Saved: {slow_time - fast_time:.2f} hours\n")

print("\nCharging comparison completed successfully!")
