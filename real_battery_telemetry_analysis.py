"""
================================================================================
REAL-WORLD EV BATTERY TELEMETRY ANALYSIS & VALIDATION
================================================================================
Course: EEE3103 - Electric Vehicles and Battery Technologies
Institution: Presidency University, Bengaluru
Dataset: Stanford University Energy Control Laboratory (Bosoni et al., 2023)
Signals Processed:
  - Pack Current (Curr) [A]
  - Pack Voltage (Volt) [V]
  - State of Charge (SoC) [%]
  - Pack Temperature (Temp) [°C]
  - High-frequency Timestamps (TimeCurr, TimeVolt, Epoch) [s]
================================================================================
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Ensure matplotlib works in headless environments
os.environ['MPLCONFIGDIR'] = 'C:/Users/bhagy/AppData/Local/Temp'

try:
    import h5py
except ImportError:
    print("[ERROR] 'h5py' library is required to parse MATLAB v7.3 HDF5 archives.")
    print("Please install it via: pip install h5py")
    sys.exit(1)

# Paths configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "Real-world electric vehicle data driving and charging")
CHARGE_DIR = os.path.join(DATASET_DIR, "Charge")
DRIVE_DIR = os.path.join(DATASET_DIR, "Drive")
GRAPHS_DIR = os.path.join(BASE_DIR, "graphs")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(GRAPHS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


def parse_telemetry_mat(file_path):
    """
    Parses a Stanford EV dataset MATLAB v7.3 HDF5 file.
    Returns a dictionary of raw numpy arrays.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Telemetry archive not found at: {file_path}")

    data = {}
    with h5py.File(file_path, 'r') as f:
        if 'Raw' not in f:
            raise KeyError("Group 'Raw' not found in HDF5 archive.")
        raw = f['Raw']
        for key in ['Curr', 'Volt', 'SoC', 'Temp', 'TimeCurr', 'TimeVolt', 'TimeTemp', 'Epoch']:
            if key in raw:
                data[key] = np.array(raw[key]).squeeze()
    return data


def analyze_charging_session(charge_folder="Folder5"):
    """
    Analyzes an empirical charging session from the Stanford dataset.
    Extracts CC-CV transition, charging power profile, and temperature rise.
    """
    mat_path = os.path.join(CHARGE_DIR, charge_folder, "Raw.mat")
    print(f"\n[INFO] Ingesting Real-World Charging Session: {charge_folder}...")
    data = parse_telemetry_mat(mat_path)

    time_curr = data['TimeCurr']
    curr = data['Curr']
    volt = data['Volt']
    soc = data['SoC']

    # Compute relative time in minutes
    time_sec = time_curr - time_curr[0]
    time_min = time_sec / 60.0

    # In charging telemetry: current is negative (inflow into battery pack)
    # Instantaneous charging power: P = V * (-I) in kW
    charging_power_kw = (volt * (-curr)) / 1000.0

    # Trapezoidal numerical integration for energy delivered (kWh)
    dt_sec = np.diff(time_sec, prepend=0)
    energy_delivered_kwh = np.sum(np.maximum(charging_power_kw, 0) * (dt_sec / 3600.0))

    initial_soc = soc[0]
    final_soc = soc[-1]
    peak_power = np.max(charging_power_kw)
    avg_power = np.mean(charging_power_kw[charging_power_kw > 0])
    duration_min = time_min[-1]

    temp = data.get('Temp', None)
    initial_temp = temp[0] if temp is not None and len(temp) > 0 else np.nan
    final_temp = temp[-1] if temp is not None and len(temp) > 0 else np.nan
    temp_rise = final_temp - initial_temp if not np.isnan(initial_temp) else np.nan

    print("\n===== EMPIRICAL CHARGING SESSION METRICS =====")
    print(f"Session Duration         : {duration_min:.2f} minutes ({duration_min/60.0:.2f} hours)")
    print(f"Initial State of Charge  : {initial_soc:.2f}%")
    print(f"Final State of Charge    : {final_soc:.2f}%")
    print(f"Net SOC Gained           : {final_soc - initial_soc:.2f}%")
    print(f"Peak Charging Power      : {peak_power:.2f} kW")
    print(f"Average Charging Power   : {avg_power:.2f} kW")
    print(f"Total Energy Delivered   : {energy_delivered_kwh:.2f} kWh")
    if not np.isnan(temp_rise):
        print(f"Initial Pack Temperature : {initial_temp:.1f} °C")
        print(f"Final Pack Temperature   : {final_temp:.1f} °C")
        print(f"Thermal Rise             : +{temp_rise:.1f} °C")

    # Decimate signal for clean, high-performance visualization
    step = max(1, len(time_min) // 2000)
    t_plot = time_min[::step]
    p_plot = charging_power_kw[::step]
    v_plot = volt[::step]
    s_plot = soc[::step]

    # Plot empirical charging telemetry
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    ax1.plot(t_plot, s_plot, color='#1f77b4', lw=2)
    ax1.set_ylabel('SOC (%)', fontsize=11, fontweight='bold')
    ax1.set_title(f'Empirical EV Battery Charging Telemetry ({charge_folder})', fontsize=13, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.6)

    ax2.plot(t_plot, p_plot, color='#d62728', lw=1.5)
    ax2.set_ylabel('Power (kW)', fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.6)

    ax3.plot(t_plot, v_plot, color='#2ca02c', lw=1.5)
    ax3.set_ylabel('Pack Voltage (V)', fontsize=11, fontweight='bold')
    ax3.set_xlabel('Charging Time (Minutes)', fontsize=11, fontweight='bold')
    ax3.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plot_file = os.path.join(GRAPHS_DIR, "empirical_charging_session.png")
    plt.savefig(plot_file, dpi=200)
    plt.close()
    print(f"[SUCCESS] Charging session plot saved to: {plot_file}")

    return {
        'duration_min': duration_min,
        'delta_soc': final_soc - initial_soc,
        'energy_kwh': energy_delivered_kwh,
        'peak_power_kw': peak_power,
        'temp_rise_c': temp_rise
    }


def analyze_driving_session(drive_folder="Folder4", window_seconds=2400):
    """
    Analyzes an empirical driving session from the Stanford dataset.
    Extracts acceleration current spikes, internal resistance voltage sag,
    and regenerative braking energy recuperation.
    """
    mat_path = os.path.join(DRIVE_DIR, drive_folder, "Raw.mat")
    print(f"\n[INFO] Ingesting Real-World Driving Session: {drive_folder}...")
    data = parse_telemetry_mat(mat_path)

    time_curr = data['TimeCurr']
    curr = data['Curr']
    volt = data['Volt']
    soc = data['SoC']

    time_sec = time_curr - time_curr[0]
    # Select analytical window
    mask = (time_sec >= 0) & (time_sec <= window_seconds)
    t_sec = time_sec[mask]
    t_min = t_sec / 60.0
    c_arr = curr[mask]
    v_arr = volt[mask]
    s_arr = soc[mask]

    # Discharging power: P = V * I in kW (positive = discharge, negative = regen)
    p_kw = (v_arr * c_arr) / 1000.0
    dt_sec = np.diff(t_sec, prepend=0)

    # Separate driving discharge energy from regenerative energy recuperation
    discharge_mask = p_kw > 0
    regen_mask = p_kw < 0

    energy_discharged_kwh = np.sum(p_kw[discharge_mask] * (dt_sec[discharge_mask] / 3600.0))
    energy_recuperated_kwh = np.sum(np.abs(p_kw[regen_mask]) * (dt_sec[regen_mask] / 3600.0))
    net_energy_consumed_kwh = energy_discharged_kwh - energy_recuperated_kwh
    regen_efficiency_pct = (energy_recuperated_kwh / energy_discharged_kwh) * 100.0 if energy_discharged_kwh > 0 else 0.0

    peak_discharge_current = np.max(c_arr)
    peak_regen_current = np.min(c_arr)
    min_voltage = np.min(v_arr)
    max_voltage = np.max(v_arr)
    voltage_sag = max_voltage - min_voltage

    print("\n===== EMPIRICAL DRIVING SESSION METRICS =====")
    print(f"Analyzed Window Duration : {t_min[-1]:.2f} minutes")
    print(f"Initial SOC              : {s_arr[0]:.2f}%")
    print(f"Final SOC                : {s_arr[-1]:.2f}%")
    print(f"Net SOC Depletion        : {s_arr[0] - s_arr[-1]:.2f}%")
    print(f"Peak Discharge Current   : +{peak_discharge_current:.1f} A (Hard Acceleration)")
    print(f"Peak Regenerative Current: {peak_regen_current:.1f} A (Regen Braking)")
    print(f"Nominal / Max Voltage    : {max_voltage:.1f} V")
    print(f"Minimum Sagged Voltage   : {min_voltage:.1f} V")
    print(f"Transient Voltage Sag    : {voltage_sag:.1f} V (Internal Impedance Drop)")
    print(f"Traction Energy Used     : {energy_discharged_kwh:.2f} kWh")
    print(f"Regen Energy Recovered   : {energy_recuperated_kwh:.2f} kWh")
    print(f"Net Energy Consumed      : {net_energy_consumed_kwh:.2f} kWh")
    print(f"Regenerative Recovery %  : {regen_efficiency_pct:.2f}% of traction energy")

    # Decimate signal for plotting
    step = max(1, len(t_min) // 2000)
    t_plot = t_min[::step]
    c_plot = c_arr[::step]
    v_plot = v_arr[::step]
    s_plot = s_arr[::step]

    # Plot empirical driving telemetry
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    ax1.plot(t_plot, c_plot, color='#d62728', lw=1.2)
    ax1.axhline(0, color='black', lw=0.8, linestyle='--')
    ax1.set_ylabel('Current (A)\n[+Discharge / -Regen]', fontsize=10, fontweight='bold')
    ax1.set_title(f'Empirical EV Driving Session Telemetry ({drive_folder})', fontsize=12, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.6)

    ax2.plot(t_plot, v_plot, color='#2ca02c', lw=1.2)
    ax2.set_ylabel('Pack Voltage (V)', fontsize=10, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.6)

    ax3.plot(t_plot, s_plot, color='#1f77b4', lw=2)
    ax3.set_ylabel('SOC (%)', fontsize=10, fontweight='bold')
    ax3.set_xlabel('Driving Time (Minutes)', fontsize=10, fontweight='bold')
    ax3.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plot_file = os.path.join(GRAPHS_DIR, "empirical_driving_session.png")
    plt.savefig(plot_file, dpi=200)
    plt.close()
    print(f"[SUCCESS] Driving session plot saved to: {plot_file}")

    return {
        'delta_soc': s_arr[0] - s_arr[-1],
        'peak_accel_a': peak_discharge_current,
        'peak_regen_a': peak_regen_current,
        'voltage_sag_v': voltage_sag,
        'regen_recovered_kwh': energy_recuperated_kwh,
        'net_energy_kwh': net_energy_consumed_kwh
    }


def save_empirical_summary(ch_metrics, dr_metrics):
    """
    Saves numerical empirical metrics into a structured report text file.
    """
    out_file = os.path.join(RESULTS_DIR, "empirical_telemetry_results.txt")
    with open(out_file, "w") as f:
        f.write("============================================================\n")
        f.write("   REAL-WORLD EV BATTERY TELEMETRY EMPIRICAL RESULTS        \n")
        f.write("   Dataset: Stanford University Energy Control Laboratory   \n")
        f.write("============================================================\n\n")
        f.write("1. CHARGING SESSION OBSERVATIONS:\n")
        f.write(f"   - Session Duration          : {ch_metrics['duration_min']:.2f} min\n")
        f.write(f"   - Net SOC Added             : {ch_metrics['delta_soc']:.2f} %\n")
        f.write(f"   - Total Energy Delivered    : {ch_metrics['energy_kwh']:.2f} kWh\n")
        f.write(f"   - Peak Charging Power       : {ch_metrics['peak_power_kw']:.2f} kW\n")
        f.write(f"   - Thermal Pack Rise         : +{ch_metrics['temp_rise_c']:.1f} °C\n\n")
        f.write("2. DRIVING SESSION OBSERVATIONS:\n")
        f.write(f"   - Peak Acceleration Current : +{dr_metrics['peak_accel_a']:.1f} A\n")
        f.write(f"   - Peak Regenerative Current : {dr_metrics['peak_regen_a']:.1f} A\n")
        f.write(f"   - Transient Voltage Sag     : {dr_metrics['voltage_sag_v']:.1f} V\n")
        f.write(f"   - Regenerative Energy Recov.: {dr_metrics['regen_recovered_kwh']:.2f} kWh\n")
        f.write(f"   - Net Traction Energy Used  : {dr_metrics['net_energy_kwh']:.2f} kWh\n\n")
        f.write("3. KEY ENGINEERING TAKEAWAY:\n")
        f.write("   Real-world EV operation exhibits dynamic CC-CV power tapering and\n")
        f.write("   significant regenerative braking energy recapture that are completely\n")
        f.write("   neglected in classical linear textbook battery simulations.\n")
    print(f"\n[SUCCESS] Summary results file saved to: {out_file}")


def main():
    print("=" * 70)
    print("  EV BATTERY PERFORMANCE SIMULATION: REAL-WORLD TELEMETRY PIPELINE")
    print("=" * 70)
    ch_metrics = analyze_charging_session(charge_folder="Folder5")
    dr_metrics = analyze_driving_session(drive_folder="Folder4", window_seconds=2400)
    save_empirical_summary(ch_metrics, dr_metrics)
    print("\n[COMPLETE] Real-world telemetry analysis completed successfully.")


if __name__ == "__main__":
    main()
