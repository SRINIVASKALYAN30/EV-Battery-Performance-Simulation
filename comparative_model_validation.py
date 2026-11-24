"""
================================================================================
THEORETICAL MODEL VS. REAL-WORLD TELEMETRY COMPARATIVE VALIDATION
================================================================================
Course: EEE3103 - Electric Vehicles and Battery Technologies
Institution: Presidency University, Bengaluru

This script directly benchmarks the theoretical simulation equations against
empirical on-road measurements from the Stanford University EV Dataset:
  1. Compares idealized linear charging vs. non-linear CC-CV tapering
  2. Compares idealized monotonic discharge vs. dynamic driving & regenerative braking
  3. Quantifies discrepancy percentages and outputs comparative plots.
================================================================================
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

os.environ['MPLCONFIGDIR'] = 'C:/Users/bhagy/AppData/Local/Temp'

try:
    import h5py
except ImportError:
    print("[ERROR] 'h5py' is required to parse MATLAB v7.3 HDF5 archives.")
    sys.exit(1)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "Real-world electric vehicle data driving and charging")
GRAPHS_DIR = os.path.join(BASE_DIR, "graphs")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(GRAPHS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


def load_charge_telemetry(folder="Folder5"):
    mat_path = os.path.join(DATASET_DIR, "Charge", folder, "Raw.mat")
    with h5py.File(mat_path, 'r') as f:
        raw = f['Raw']
        time_curr = np.array(raw['TimeCurr']).squeeze()
        time_sec = time_curr - time_curr[0]
        curr = np.array(raw['Curr']).squeeze()
        volt = np.array(raw['Volt']).squeeze()
        soc = np.array(raw['SoC']).squeeze()
    return time_sec, curr, volt, soc


def load_drive_telemetry(folder="Folder4", max_sec=2400):
    mat_path = os.path.join(DATASET_DIR, "Drive", folder, "Raw.mat")
    with h5py.File(mat_path, 'r') as f:
        raw = f['Raw']
        time_curr = np.array(raw['TimeCurr']).squeeze()
        time_sec = time_curr - time_curr[0]
        mask = (time_sec >= 0) & (time_sec <= max_sec)
        t_sec = time_sec[mask]
        curr = np.array(raw['Curr']).squeeze()[mask]
        volt = np.array(raw['Volt']).squeeze()[mask]
        soc = np.array(raw['SoC']).squeeze()[mask]
    return t_sec, curr, volt, soc


def validate_charging():
    """
    Compares the linear theoretical charging model against real Stanford charging data.
    """
    print("\n[INFO] Running Comparative Validation: Charging Dynamics...")
    time_sec, curr, volt, real_soc = load_charge_telemetry("Folder5")
    time_min = time_sec / 60.0
    time_hr = time_sec / 3600.0

    # Net energy delivered in real telemetry
    power_kw = (volt * (-curr)) / 1000.0
    dt_sec = np.diff(time_sec, prepend=0)
    real_energy_kwh = np.sum(np.maximum(power_kw, 0) * (dt_sec / 3600.0))

    initial_soc = real_soc[0]
    final_soc = real_soc[-1]
    delta_soc = final_soc - initial_soc

    # Estimate pack capacity from empirical data: Cap = E_del / (delta_soc / 100)
    effective_pack_cap = real_energy_kwh / (delta_soc / 100.0)

    # Theoretical Linear Model: assumes constant charging power equal to average real power
    avg_power = np.mean(power_kw[power_kw > 0])
    theo_soc = initial_soc + (avg_power * time_hr / effective_pack_cap) * 100.0
    theo_soc = np.clip(theo_soc, 0, final_soc)

    # Decimate for plot
    step = max(1, len(time_min) // 1500)
    t_plot = time_min[::step]
    r_soc_plot = real_soc[::step]
    t_soc_plot = theo_soc[::step]

    # Calculate Mean Absolute Error (MAE) between theoretical and real SOC
    mae_soc = np.mean(np.abs(real_soc - theo_soc))

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(t_plot, t_soc_plot, '--', color='#d62728', lw=2, label=f'Idealized Linear Model (P = {avg_power:.1f} kW const)')
    ax.plot(t_plot, r_soc_plot, '-', color='#1f77b4', lw=2, label='Empirical Measured Telemetry (Stanford Dataset)')
    ax.set_title('Charging Profile: Theoretical Linear Model vs. Empirical Telemetry', fontsize=12, fontweight='bold')
    ax.set_xlabel('Charging Time (Minutes)', fontsize=11, fontweight='bold')
    ax.set_ylabel('State of Charge (SOC %)', fontsize=11, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='lower right', fontsize=10)

    # Annotate CC-CV divergence
    ax.annotate('Constant Voltage (CV) Tapering\nCauses Non-Linear Deviation',
                xy=(t_plot[int(len(t_plot)*0.75)], r_soc_plot[int(len(r_soc_plot)*0.75)]),
                xytext=(t_plot[int(len(t_plot)*0.4)], r_soc_plot[int(len(r_soc_plot)*0.75)] - 15),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.2),
                fontsize=9.5, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', fc='#ffffcc', ec='gray'))

    plt.tight_layout()
    plot_file = os.path.join(GRAPHS_DIR, "validation_charging_comparison.png")
    plt.savefig(plot_file, dpi=200)
    plt.close()
    print(f"[SUCCESS] Charging validation plot saved to: {plot_file}")
    print(f"  Theoretical vs Real SOC Mean Absolute Error: {mae_soc:.2f} %")

    return {
        'avg_power_kw': avg_power,
        'effective_cap_kwh': effective_pack_cap,
        'mae_soc': mae_soc
    }


def validate_discharging():
    """
    Compares the linear theoretical discharge model against real driving telemetry with regen.
    """
    print("\n[INFO] Running Comparative Validation: Driving Discharging Dynamics...")
    t_sec, curr, volt, real_soc = load_drive_telemetry("Folder4", max_sec=2400)
    t_min = t_sec / 60.0

    # Real energy consumed
    p_kw = (volt * curr) / 1000.0
    dt_sec = np.diff(t_sec, prepend=0)

    pos_p = np.maximum(p_kw, 0)
    neg_p = np.minimum(p_kw, 0)

    traction_energy_kwh = np.sum(pos_p * (dt_sec / 3600.0))
    regen_energy_kwh = np.sum(np.abs(neg_p) * (dt_sec / 3600.0))
    net_energy_kwh = traction_energy_kwh - regen_energy_kwh

    initial_soc = real_soc[0]
    total_delta_soc = initial_soc - real_soc[-1]

    # Theoretical model without regenerative braking: drains energy monotonically based on average gross power
    gross_avg_power = np.mean(pos_p)
    pack_cap = (net_energy_kwh / total_delta_soc) * 100.0

    # Theoretical SOC trajectory without regen
    theo_soc_no_regen = initial_soc - (np.cumsum(pos_p * (dt_sec / 3600.0)) / pack_cap) * 100.0

    # Decimate for plot
    step = max(1, len(t_min) // 1500)
    t_plot = t_min[::step]
    r_soc_plot = real_soc[::step]
    t_soc_plot = theo_soc_no_regen[::step]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(t_plot, t_soc_plot, '--', color='#d62728', lw=2, label='Idealized Model without Regenerative Braking')
    ax.plot(t_plot, r_soc_plot, '-', color='#1f77b4', lw=2, label='Empirical Driving Telemetry (with Active Regen)')
    ax.set_title('Driving Profile: Impact of Regenerative Braking on SOC Depletion', fontsize=12, fontweight='bold')
    ax.set_xlabel('Driving Time (Minutes)', fontsize=11, fontweight='bold')
    ax.set_ylabel('State of Charge (SOC %)', fontsize=11, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='lower left', fontsize=10)

    # Highlight energy recovery
    regen_gain_soc = r_soc_plot[-1] - t_soc_plot[-1]
    ax.annotate(f'Regenerative Braking Advantage:\n+{regen_gain_soc:.2f}% SOC Preserved ({regen_energy_kwh:.2f} kWh)',
                xy=(t_plot[-1], r_soc_plot[-1]),
                xytext=(t_plot[-1] - 12, r_soc_plot[-1] - 8),
                arrowprops=dict(facecolor='green', arrowstyle='->', lw=1.2),
                fontsize=9.5, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', fc='#e6ffed', ec='green'))

    plt.tight_layout()
    plot_file = os.path.join(GRAPHS_DIR, "validation_driving_comparison.png")
    plt.savefig(plot_file, dpi=200)
    plt.close()
    print(f"[SUCCESS] Discharging validation plot saved to: {plot_file}")
    print(f"  Regen Energy Recovered: {regen_energy_kwh:.2f} kWh (Preserves +{regen_gain_soc:.2f} % SOC)")

    return {
        'traction_kwh': traction_energy_kwh,
        'regen_kwh': regen_energy_kwh,
        'regen_soc_preserved': regen_gain_soc
    }


def save_validation_results(ch_res, dr_res):
    out_file = os.path.join(RESULTS_DIR, "comparative_validation_results.txt")
    with open(out_file, "w") as f:
        f.write("============================================================\n")
        f.write("  COMPARATIVE VALIDATION: THEORETICAL VS REAL-WORLD TELEMETRY\n")
        f.write("============================================================\n\n")
        f.write("1. CHARGING DYNAMICS VALIDATION:\n")
        f.write(f"   - Average Effective Power        : {ch_res['avg_power_kw']:.2f} kW\n")
        f.write(f"   - Empirical Effective Pack Cap   : {ch_res['effective_cap_kwh']:.2f} kWh\n")
        f.write(f"   - Theoretical vs Real SOC MAE    : {ch_res['mae_soc']:.2f} %\n")
        f.write("   - Physical Discrepancy Identified: Constant Voltage (CV) phase causes\n")
        f.write("     current tapering above 80% SOC, which idealized flat models underestimate.\n\n")
        f.write("2. DRIVING & REGENERATION DYNAMICS VALIDATION:\n")
        f.write(f"   - Gross Traction Energy Consumed : {dr_res['traction_kwh']:.2f} kWh\n")
        f.write(f"   - Regenerative Energy Recaptured : {dr_res['regen_kwh']:.2f} kWh\n")
        f.write(f"   - Net SOC Preserved via Regen    : +{dr_res['regen_soc_preserved']:.2f} %\n")
        f.write("   - Physical Discrepancy Identified: Linear models over-predict battery\n")
        f.write("     depletion because they completely omit kinetic energy recovery during braking.\n")
    print(f"\n[SUCCESS] Comparative validation results saved to: {out_file}")


def main():
    print("=" * 70)
    print("  EV BATTERY PERFORMANCE: THEORETICAL VS REAL-WORLD VALIDATION")
    print("=" * 70)
    ch_res = validate_charging()
    dr_res = validate_discharging()
    save_validation_results(ch_res, dr_res)
    print("\n[COMPLETE] Comparative validation pipeline finished successfully.")


if __name__ == "__main__":
    main()
