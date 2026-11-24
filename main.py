"""
================================================================================
EV BATTERY PERFORMANCE SIMULATION & EMPIRICAL TELEMETRY VALIDATION
================================================================================
Course: EEE3103 - Electric Vehicles and Battery Technologies
Department of Electrical & Electronics Engineering
Presidency University, Bengaluru

Master Execution Console:
  [1] Run Baseline EV Battery Simulation (Charging + 100 km Drive)
  [2] Run Charging Comparison (Slow 7 kW AC vs. Fast 50 kW DC)
  [3] Run Cruising Speed vs. Energy Consumption & Range Simulation
  [4] Run Battery Pack Capacity Comparison (30, 60, 90 kWh)
  [5] Run Real-World Telemetry Analysis (Stanford EV Dataset)
  [6] Run Comparative Model Validation (Theory vs. Empirical Telemetry)
  [7] Run Complete Project Suite (All Experiments)
  [8] Generate Project Summary Report & Exit
================================================================================
"""

import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print("=" * 72)
    print("      PRESIDENCY UNIVERSITY - DEPARTMENT OF EEE")
    print("   EEE3103: ELECTRIC VEHICLES AND BATTERY TECHNOLOGIES")
    print("   CA-3 MINI PROJECT: EV BATTERY PERFORMANCE SIMULATION")
    print("=" * 72)

def print_menu():
    print("\nPlease select an experiment to run:")
    print("  [1] Baseline EV Battery Simulation (Charging + 100 km Journey)")
    print("  [2] Charging Infrastructure Comparison (Slow 7 kW vs. Fast 50 kW)")
    print("  [3] Cruising Speed vs. Specific Consumption & Range Simulation")
    print("  [4] Battery Pack Capacity Sensitivity (30, 60, 90 kWh Packs)")
    print("  [5] Real-World Telemetry Analysis (Stanford EV HDF5 Dataset)")
    print("  [6] Theoretical Model vs. Empirical Telemetry Validation")
    print("  [7] Run Entire Experimental Suite (Options 1 to 6)")
    print("  [8] View Project Summary & Exit")
    print("=" * 72)

def run_script(script_name):
    script_path = os.path.join(BASE_DIR, script_name)
    if not os.path.exists(script_path):
        print(f"\n[ERROR] Target script '{script_name}' not found at: {script_path}")
        return False
    
    print(f"\n>>> Executing Module: {script_name} ...")
    print("-" * 72)
    result = subprocess.run([sys.executable, script_path])
    print("-" * 72)
    if result.returncode == 0:
        print(f"[SUCCESS] {script_name} completed successfully.")
        return True
    else:
        print(f"[FAILED] {script_name} exited with error code {result.returncode}.")
        return False

def show_summary():
    print("\n" + "=" * 72)
    print("                      PROJECT EXECUTIVE SUMMARY")
    print("=" * 72)
    print("1. SYSTEM UNDER STUDY:")
    print("   - EV Architecture: 60 kWh Lithium-ion Pack, 400 V nominal bus.")
    print("   - Initial SOC: 30%, Charged to 51% (2h Level-2 AC), Driven 100 km.")
    print("   - Final Retained SOC: 26%, Remaining Range: 104 km.")
    print("\n2. INFRASTRUCTURE EFFICIENCY:")
    print("   - 50 kW DC Fast Charging saves 4.13 hours (86.7% dwell time reduction)")
    print("     compared to standard 7 kW Level-2 AC charging.")
    print("\n3. AERODYNAMIC ROAD LOAD:")
    print("   - Cruising at 100 km/h nearly doubles consumption (22 kWh/100 km)")
    print("     and reduces range by 45.5% compared to 30 km/h urban driving.")
    print("\n4. REAL-WORLD DATASET VALIDATION (STANFORD EV DATASET):")
    print("   - Unmasked CC-CV power tapering above 80% SOC and +7°C pack thermal rise.")
    print("   - Documented +901 A transient acceleration spikes with ~50 V internal voltage sag.")
    print("   - Demonstrated -361 A active regenerative braking energy recovery.")
    print("\n5. ARTIFACTS GENERATED:")
    print("   - Technical Report : EEE3103_niproject report format.docx")
    print("   - Presentation Deck: EEE3103_CA3_Mini_Project_Presentation_Template_FINAL.pptx")
    print("   - Graphical Assets : graphs/ (9 high-resolution engineering figures)")
    print("=" * 72)

def main():
    while True:
        print_banner()
        print_menu()
        choice = input("Enter option [1-8]: ").strip()
        
        if choice == '1':
            run_script("ev_battery_simulation.py")
        elif choice == '2':
            run_script("charging_comparison.py")
        elif choice == '3':
            run_script("speed_range_simulation.py")
        elif choice == '4':
            run_script("battery_comparison.py")
        elif choice == '5':
            run_script("real_battery_telemetry_analysis.py")
        elif choice == '6':
            run_script("comparative_model_validation.py")
        elif choice == '7':
            print("\n>>> Launching Full Automated Project Suite...")
            scripts = [
                "ev_battery_simulation.py",
                "charging_comparison.py",
                "speed_range_simulation.py",
                "battery_comparison.py",
                "real_battery_telemetry_analysis.py",
                "comparative_model_validation.py"
            ]
            for s in scripts:
                run_script(s)
            show_summary()
        elif choice == '8':
            show_summary()
            print("\nExiting program. Thank you!")
            break
        else:
            print("\n[INVALID] Please select a valid number between 1 and 8.")
        
        input("\nPress [Enter] to return to the main menu...")
        clear_screen()

if __name__ == "__main__":
    main()
