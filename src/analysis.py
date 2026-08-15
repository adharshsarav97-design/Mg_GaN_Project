# ============================================================
# Mg IMPLANTATION IN GaN
# Simulation-Driven Process Analysis
#
# SRIM + Python
#
# Purpose:
#   Analyze Mg implantation conditions for an approximately
#   100 nm target depth in GaN.
#
# Simulation DOE:
#   Energy : 50, 75, 100 keV
#   Tilt   : 0, 7, 15 degrees
#
# Reference process selected from simulation + literature:
#   100 keV / 7 degrees
#
# IMPORTANT:
#   SRIM results are simulation results.
#   Literature values are kept separate.
#   Concentration profile is a Gaussian approximation.
# ============================================================


# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 2. FILE PATHS
# ============================================================

DATA_FILE = "data/SRIM_9Run_Master.csv"
RESULTS_DIR = "results"

os.makedirs(RESULTS_DIR, exist_ok=True)


# ============================================================
# 3. LOAD SRIM DATA
# ============================================================

data = pd.read_csv(DATA_FILE)

print("\n========================================")
print("Mg IMPLANTATION IN GaN")
print("SRIM + PYTHON PROCESS ANALYSIS")
print("========================================")

print("\nDataset shape:")
print(data.shape)

print("\nColumns:")
print(list(data.columns))


# ============================================================
# 4. BASIC DATA SUMMARY
# ============================================================

print("\n========================================")
print("SRIM DATASET")
print("========================================")

print(
    data[
        [
            "Run",
            "Energy_keV",
            "Tilt_deg",
            "Rp_nm",
            "Longitudinal_Straggling_nm",
            "Lateral_Range_nm",
            "Vacancies_per_Ion"
        ]
    ].to_string(index=False)
)


# ============================================================
# 5. TARGET DEFINITION
# ============================================================

TARGET_DEPTH = 100.0
LOWER_LIMIT = 95.0
UPPER_LIMIT = 105.0

data["Depth_Error_nm"] = abs(
    data["Rp_nm"] - TARGET_DEPTH
)


# ============================================================
# 6. AVERAGE PROJECTED RANGE BY ENERGY
# ============================================================

energy_analysis = (
    data.groupby("Energy_keV")["Rp_nm"]
    .mean()
)

print("\n========================================")
print("AVERAGE PROJECTED RANGE BY ENERGY")
print("========================================")

print(energy_analysis)


# ============================================================
# 7. AVERAGE PROJECTED RANGE BY TILT
# ============================================================

tilt_analysis = (
    data.groupby("Tilt_deg")["Rp_nm"]
    .mean()
)

print("\n========================================")
print("AVERAGE PROJECTED RANGE BY TILT")
print("========================================")

print(tilt_analysis)


# ============================================================
# 8. AVERAGE LATERAL RANGE BY TILT
# ============================================================

lateral_analysis = (
    data.groupby("Tilt_deg")["Lateral_Range_nm"]
    .mean()
)

print("\n========================================")
print("AVERAGE LATERAL RANGE BY TILT")
print("========================================")

print(lateral_analysis)


# ============================================================
# 9. AVERAGE VACANCIES PER ION BY ENERGY
# ============================================================

vacancy_analysis = (
    data.groupby("Energy_keV")["Vacancies_per_Ion"]
    .mean()
)

print("\n========================================")
print("AVERAGE VACANCIES PER ION BY ENERGY")
print("========================================")

print(vacancy_analysis)


# ============================================================
# 10. ENERGY × TILT TABLES
# ============================================================

rp_table = data.pivot(
    index="Energy_keV",
    columns="Tilt_deg",
    values="Rp_nm"
)

lateral_table = data.pivot(
    index="Energy_keV",
    columns="Tilt_deg",
    values="Lateral_Range_nm"
)

vacancy_table = data.pivot(
    index="Energy_keV",
    columns="Tilt_deg",
    values="Vacancies_per_Ion"
)


print("\n========================================")
print("ENERGY × TILT — PROJECTED RANGE")
print("========================================")

print(rp_table)


print("\n========================================")
print("ENERGY × TILT — LATERAL RANGE")
print("========================================")

print(lateral_table)


print("\n========================================")
print("ENERGY × TILT — VACANCIES PER ION")
print("========================================")

print(vacancy_table)


# ============================================================
# 11. RANK CONDITIONS BY 100-nm TARGET
# ============================================================

ranked = data.sort_values(
    "Depth_Error_nm"
).copy()

print("\n========================================")
print("PROCESS CONDITIONS RANKED BY 100-nm TARGET")
print("========================================")

print(
    ranked[
        [
            "Run",
            "Energy_keV",
            "Tilt_deg",
            "Rp_nm",
            "Depth_Error_nm",
            "Lateral_Range_nm",
            "Vacancies_per_Ion"
        ]
    ].to_string(index=False)
)


# ============================================================
# 12. 95–105 nm PROCESS WINDOW
# ============================================================

process_window = data[
    data["Rp_nm"].between(
        LOWER_LIMIT,
        UPPER_LIMIT
    )
].sort_values("Depth_Error_nm")


print("\n========================================")
print("PROCESS CONDITIONS WITHIN 95–105 nm")
print("========================================")

print(
    process_window[
        [
            "Run",
            "Energy_keV",
            "Tilt_deg",
            "Rp_nm",
            "Depth_Error_nm",
            "Lateral_Range_nm",
            "Vacancies_per_Ion"
        ]
    ].to_string(index=False)
)


# ============================================================
# 13. SELECT REFERENCE CONDITION
# ============================================================
#
# We select 100 keV / 7 degrees as the reference condition
# because:
#
#   Rp = 102.1 nm
#   Lateral range = 40.2 nm
#
# It is inside the 95–105 nm screening window and has
# published experimental precedent at comparable conditions.
#
# This is a proposed reference condition, NOT an experimental
# optimization performed by us.
# ============================================================

REFERENCE_RUN = 4

reference = data[
    data["Run"] == REFERENCE_RUN
].iloc[0]

reference_energy = reference["Energy_keV"]
reference_tilt = reference["Tilt_deg"]
reference_rp = reference["Rp_nm"]
reference_sigma = reference["Longitudinal_Straggling_nm"]
reference_lateral = reference["Lateral_Range_nm"]
reference_vacancies = reference["Vacancies_per_Ion"]


# ============================================================
# 14. FLUENCE SCREENING
# ============================================================
#
# Literature reference fluence:
#
#   3 × 10^14 ions/cm^2
#
# This is NOT an SRIM output.
# It is kept separate as a literature-based reference.
#
# Vacancy-event scaling:
#
#   fluence × vacancies/ion
#
# This represents fluence-scaled vacancy events, NOT permanent
# vacancy concentration.
# ============================================================

literature_fluence = 3e14

screening_fluences = np.array([
    1e14,
    5e14,
    1e15,
    5e15
])

dose_screening = pd.DataFrame({
    "Fluence_ions_cm2": screening_fluences,
    "Vacancies_per_Ion": reference_vacancies
})

dose_screening[
    "Estimated_Vacancy_Events_cm2"
] = (
    dose_screening["Fluence_ions_cm2"]
    * dose_screening["Vacancies_per_Ion"]
)


print("\n========================================")
print("FLUENCE SCREENING")
print("========================================")

print(
    dose_screening.to_string(index=False)
)


# ============================================================
# 15. DOSE COMPARISON FOR 100-nm PROCESS WINDOW
# ============================================================

dose_comparison = []

for _, row in process_window.iterrows():

    for fluence in screening_fluences:

        vacancy_events = (
            fluence *
            row["Vacancies_per_Ion"]
        )

        dose_comparison.append({

            "Run": int(row["Run"]),

            "Energy_keV": row["Energy_keV"],

            "Tilt_deg": row["Tilt_deg"],

            "Rp_nm": row["Rp_nm"],

            "Lateral_Range_nm":
                row["Lateral_Range_nm"],

            "Vacancies_per_Ion":
                row["Vacancies_per_Ion"],

            "Fluence_ions_cm2":
                fluence,

            "Estimated_Vacancy_Events_cm2":
                vacancy_events
        })


dose_comparison = pd.DataFrame(
    dose_comparison
)


print("\n========================================")
print("DOSE COMPARISON — 100-nm PROCESS WINDOW")
print("========================================")

print(
    dose_comparison.to_string(index=False)
)


# ============================================================
# 16. LITERATURE VALIDATION
# ============================================================
#
# Published reference:
#
#   Energy       = 100 keV
#   Tilt         = 7 degrees
#   Fluence      ≈ 3 × 10^14 cm^-2
#   Mg depth     ≈ 100 nm SIMS peak
#
# IMPORTANT:
#   Our SRIM Rp and experimental SIMS peak are related but
#   are NOT identical measurements.
# ============================================================

literature_depth_nm = 100.0

literature_validation = pd.DataFrame({

    "Source": [
        "Our SRIM simulation",
        "Published Mg:GaN experiment"
    ],

    "Energy_keV": [
        reference_energy,
        100
    ],

    "Tilt_deg": [
        reference_tilt,
        7
    ],

    "Fluence_ions_cm2": [
        np.nan,
        literature_fluence
    ],

    "Depth_nm": [
        reference_rp,
        literature_depth_nm
    ]
})


print("\n========================================")
print("SIMULATION vs LITERATURE VALIDATION")
print("========================================")

print(
    literature_validation.to_string(index=False)
)


# ============================================================
# 17. LITERATURE-SUPPORTED PROCESS REFERENCE
# ============================================================

process_reference = pd.DataFrame({

    "Parameter": [

        "Implantation energy",

        "Implantation tilt",

        "Fluence",

        "SRIM projected range",

        "Published Mg depth",

        "Reference anneal temperature",

        "Reference anneal time",

        "Anneal atmosphere"
    ],

    "Our_SRIM_Design": [

        "100 keV",

        "7 degrees",

        "Not simulated",

        f"{reference_rp:.1f} nm",

        "Not measured",

        "Not experimentally tested",

        "Not experimentally tested",

        "Not experimentally tested"
    ],

    "Literature_Reference": [

        "100 keV",

        "7 degrees",

        "3e14 cm^-2",

        "Not reported as SRIM Rp",

        "~100 nm SIMS Mg peak",

        "1230 degrees C",

        "30 min",

        "N2"
    ]
})


print("\n========================================")
print("LITERATURE-SUPPORTED PROCESS REFERENCE")
print("========================================")

print(
    process_reference.to_string(index=False)
)


# ============================================================
# 18. ESTIMATED Mg CONCENTRATION PROFILE
# ============================================================
#
# Gaussian approximation:
#
#       Phi
# C(x)= ---------------- exp[-(x-Rp)^2/(2*sigma^2)]
#       sqrt(2*pi)*sigma
#
# where:
#
#   Phi   = literature fluence
#   Rp    = SRIM projected range
#   sigma = SRIM longitudinal straggling
#
# IMPORTANT:
# This is an estimated model, NOT a measured concentration
# profile and NOT an exact SRIM depth histogram.
# ============================================================

sigma_cm = (
    reference_sigma * 1e-7
)

rp_cm = (
    reference_rp * 1e-7
)

depth_nm = np.linspace(
    0,
    250,
    1000
)

depth_cm = (
    depth_nm * 1e-7
)


concentration = (

    literature_fluence
    /
    (
        np.sqrt(2 * np.pi)
        * sigma_cm
    )

    *

    np.exp(
        -(
            (depth_cm - rp_cm) ** 2
        )
        /
        (
            2 * sigma_cm ** 2
        )
    )
)


peak_concentration = (
    concentration.max()
)

peak_depth = (
    depth_nm[
        np.argmax(concentration)
    ]
)


print("\n========================================")
print("ESTIMATED Mg CONCENTRATION PROFILE")
print("========================================")

print(
    "Reference condition:",
    f"{reference_energy:.0f} keV / "
    f"{reference_tilt:.0f} degrees"
)

print(
    "Literature reference fluence:",
    f"{literature_fluence:.3e}",
    "ions/cm^2"
)

print(
    "Projected range:",
    f"{reference_rp:.1f}",
    "nm"
)

print(
    "Longitudinal straggling:",
    f"{reference_sigma:.1f}",
    "nm"
)

print(
    "Estimated peak concentration:",
    f"{peak_concentration:.3e}",
    "cm^-3"
)

print(
    "Estimated peak depth:",
    f"{peak_depth:.1f}",
    "nm"
)


# ============================================================
# 19. FINAL ENGINEERING SUMMARY
# ============================================================

print("\n========================================")
print("FINAL ENGINEERING SUMMARY")
print("========================================")

print(
    f"Reference energy      : "
    f"{reference_energy:.0f} keV"
)

print(
    f"Reference tilt        : "
    f"{reference_tilt:.0f} degrees"
)

print(
    f"SRIM projected range  : "
    f"{reference_rp:.1f} nm"
)

print(
    f"Target depth          : "
    f"{TARGET_DEPTH:.1f} nm"
)

print(
    f"Depth error           : "
    f"{abs(reference_rp - TARGET_DEPTH):.1f} nm"
)

print(
    f"Lateral range         : "
    f"{reference_lateral:.1f} nm"
)

print(
    f"Vacancies per ion     : "
    f"{reference_vacancies:.1f}"
)

print(
    f"Literature fluence    : "
    f"{literature_fluence:.3e} ions/cm^2"
)

print(
    f"Estimated Mg peak     : "
    f"{peak_concentration:.3e} cm^-3"
)

print(
    "Reference anneal      : "
    "1230 degrees C / 30 min / N2"
)

print("\nStatus:")
print(
    "Simulation + literature-supported "
    "reference process"
)

print(
    "The process is proposed and requires "
    "experimental validation."
)


# ============================================================
# 20. FINAL FIGURES
# ============================================================


# ------------------------------------------------------------
# FIGURE 1 — PROJECTED RANGE HEATMAP
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.imshow(
    rp_table.values,
    aspect="auto",
    origin="lower"
)

plt.xticks(
    range(len(rp_table.columns)),
    rp_table.columns
)

plt.yticks(
    range(len(rp_table.index)),
    rp_table.index
)

plt.xlabel("Tilt angle (degrees)")
plt.ylabel("Energy (keV)")

plt.title(
    "Projected Range of Mg Ions in GaN"
)

plt.colorbar(
    label="Projected range (nm)"
)

plt.tight_layout()

plt.savefig(
    f"{RESULTS_DIR}/projected_range_heatmap.png",
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# FIGURE 2 — LATERAL RANGE HEATMAP
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.imshow(
    lateral_table.values,
    aspect="auto",
    origin="lower"
)

plt.xticks(
    range(len(lateral_table.columns)),
    lateral_table.columns
)

plt.yticks(
    range(len(lateral_table.index)),
    lateral_table.index
)

plt.xlabel("Tilt angle (degrees)")
plt.ylabel("Energy (keV)")

plt.title(
    "Lateral Range of Mg Ions in GaN"
)

plt.colorbar(
    label="Lateral range (nm)"
)

plt.tight_layout()

plt.savefig(
    f"{RESULTS_DIR}/lateral_range_heatmap.png",
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# FIGURE 3 — VACANCY HEATMAP
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.imshow(
    vacancy_table.values,
    aspect="auto",
    origin="lower"
)

plt.xticks(
    range(len(vacancy_table.columns)),
    vacancy_table.columns
)

plt.yticks(
    range(len(vacancy_table.index)),
    vacancy_table.index
)

plt.xlabel("Tilt angle (degrees)")
plt.ylabel("Energy (keV)")

plt.title(
    "Vacancy Production per Incident Ion"
)

plt.colorbar(
    label="Vacancies per ion"
)

plt.tight_layout()

plt.savefig(
    f"{RESULTS_DIR}/vacancy_heatmap.png",
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# FIGURE 4 — 100-nm PROCESS WINDOW
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.axhspan(
    LOWER_LIMIT,
    UPPER_LIMIT,
    alpha=0.2,
    label="95–105 nm target window"
)

plt.scatter(
    data["Energy_keV"],
    data["Rp_nm"],
    s=70
)

plt.scatter(
    process_window["Energy_keV"],
    process_window["Rp_nm"],
    s=100,
    marker="o",
    label="Within target window"
)

plt.axhline(
    TARGET_DEPTH,
    linestyle="--",
    label="100 nm target"
)

plt.xlabel("Implantation energy (keV)")
plt.ylabel("Projected range (nm)")

plt.title(
    "Mg Implantation Process Window"
)

plt.legend()

plt.grid(
    True,
    alpha=0.25
)

plt.tight_layout()

plt.savefig(
    f"{RESULTS_DIR}/process_window.png",
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# FIGURE 5 — ESTIMATED Mg DEPTH PROFILE
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    depth_nm,
    concentration,
    linewidth=2
)

plt.axvline(
    reference_rp,
    linestyle="--",
    label="SRIM projected range"
)

plt.axvline(
    literature_depth_nm,
    linestyle=":",
    label="Literature Mg depth ≈ 100 nm"
)

plt.xlabel("Depth (nm)")

plt.ylabel(
    "Estimated Mg concentration (cm$^{-3}$)"
)

plt.title(
    "Estimated Mg Depth Profile — "
    "100 keV / 7°"
)

plt.legend()

plt.grid(
    True,
    alpha=0.25
)

plt.tight_layout()

plt.savefig(
    f"{RESULTS_DIR}/mg_depth_profile.png",
    dpi=300
)

plt.close()


# ============================================================
# 21. SAVE IMPORTANT TABLES
# ============================================================

ranked[
    [
        "Run",
        "Energy_keV",
        "Tilt_deg",
        "Rp_nm",
        "Depth_Error_nm",
        "Lateral_Range_nm",
        "Vacancies_per_Ion"
    ]
].to_csv(
    f"{RESULTS_DIR}/ranked_process_conditions.csv",
    index=False
)


process_window[
    [
        "Run",
        "Energy_keV",
        "Tilt_deg",
        "Rp_nm",
        "Depth_Error_nm",
        "Lateral_Range_nm",
        "Vacancies_per_Ion"
    ]
].to_csv(
    f"{RESULTS_DIR}/100nm_process_window.csv",
    index=False
)


dose_comparison.to_csv(
    f"{RESULTS_DIR}/dose_comparison.csv",
    index=False
)


literature_validation.to_csv(
    f"{RESULTS_DIR}/literature_validation.csv",
    index=False
)


# ============================================================
# 22. COMPLETION MESSAGE
# ============================================================

print("\n========================================")
print("ANALYSIS COMPLETE")
print("========================================")

print(
    "Figures and result tables saved in:"
)

print(
    f"{RESULTS_DIR}/"
)

print("\nGenerated figures:")

print("1. projected_range_heatmap.png")
print("2. lateral_range_heatmap.png")
print("3. vacancy_heatmap.png")
print("4. process_window.png")
print("5. mg_depth_profile.png")

print("\nProject analysis completed successfully.")