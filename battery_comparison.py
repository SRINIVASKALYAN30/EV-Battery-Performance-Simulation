
import matplotlib.pyplot as plt
import numpy as np

# Battery capacities
battery_capacities = [30, 60, 90]

# Common simulation values
initial_soc = 100
driving_distance = 100
energy_consumption = 0.15

remaining_soc = []

print("\n===== EV BATTERY COMPARISON =====")

for capacity in battery_capacities:

    energy_used = driving_distance * energy_consumption

    final_energy = capacity - energy_used

    final_soc = (final_energy / capacity) * 100

    remaining_soc.append(final_soc)

    print(f"\nBattery Capacity: {capacity} kWh")
    print(f"Energy Consumed: {energy_used:.2f} kWh")
    print(f"Remaining SOC: {final_soc:.2f}%")
    print(f"Remaining Energy: {final_energy:.2f} kWh")

# Create comparison graph
plt.figure(figsize=(9, 5))

plt.bar(
    [str(x) + " kWh" for x in battery_capacities],
    remaining_soc
)

plt.title("EV Battery Capacity Comparison")
plt.xlabel("Battery Capacity")
plt.ylabel("Remaining SOC (%)")

plt.ylim(0, 110)
plt.grid(axis="y")

plt.savefig("graphs/battery_comparison.png")
plt.show()

print("\nBattery comparison completed!")
