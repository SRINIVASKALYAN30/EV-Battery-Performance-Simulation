
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs("graphs", exist_ok=True)
os.makedirs("results", exist_ok=True)

# EV specifications
battery_capacity = 60
initial_soc = 80

# Available battery energy
available_energy = battery_capacity * initial_soc / 100

# Driving speeds in km/h
speeds = [30, 40, 60, 80, 100]

# Assumed energy consumption in kWh per 100 km
consumption = [12, 13, 15, 18, 22]

# Calculate estimated driving range
driving_range = [
    (available_energy / value) * 100
    for value in consumption
]

print("\n===== EV SPEED AND RANGE SIMULATION =====")

print(f"Battery Capacity: {battery_capacity} kWh")
print(f"Initial SOC: {initial_soc}%")
print(f"Available Energy: {available_energy:.2f} kWh")

for speed, energy, distance in zip(
    speeds, consumption, driving_range
):
    print(f"\nDriving Speed: {speed} km/h")
    print(f"Energy Consumption: {energy} kWh/100 km")
    print(f"Estimated Driving Range: {distance:.2f} km")

# Energy consumption graph
plt.figure(figsize=(9, 5))

plt.plot(speeds, consumption, marker="o")

plt.title("Driving Speed vs Battery Energy Consumption")
plt.xlabel("Driving Speed (km/h)")
plt.ylabel("Energy Consumption (kWh/100 km)")
plt.grid(True)

plt.savefig("graphs/speed_consumption.png")
plt.show()

# Driving range graph
plt.figure(figsize=(9, 5))

plt.bar(
    [str(speed) + " km/h" for speed in speeds],
    driving_range
)

plt.title("Driving Speed vs Estimated EV Range")
plt.xlabel("Driving Speed")
plt.ylabel("Estimated Range (km)")
plt.grid(axis="y")

plt.savefig("graphs/speed_range.png")
plt.show()

# Save results
with open("results/speed_range_results.txt", "w") as file:
    file.write("EV SPEED AND RANGE SIMULATION\n")
    file.write(f"Battery Capacity: {battery_capacity} kWh\n")
    file.write(f"Initial SOC: {initial_soc}%\n")

    for speed, energy, distance in zip(
        speeds, consumption, driving_range
    ):
        file.write(
            f"\nSpeed: {speed} km/h"
            f"\nConsumption: {energy} kWh/100 km"
            f"\nEstimated Range: {distance:.2f} km\n"
        )

print("\nSpeed and range simulation completed!")
