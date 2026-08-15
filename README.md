\# Simulation-Driven Optimization of Mg Ion Implantation in GaN



\## Project Overview



This project investigates the optimization of magnesium (Mg) ion implantation conditions in gallium nitride (GaN) for achieving an implantation depth close to 100 nm.



A design-of-experiments approach was performed using SRIM by varying:



\- Implantation energy: 50, 75, and 100 keV

\- Implantation tilt: 0°, 7°, and 15°



The resulting SRIM data were analyzed using Python to study projected range, lateral range, vacancy production, target-depth error, fluence scaling, and an estimated Mg concentration profile.



The simulation results were then compared with published Mg-implanted GaN experimental data to identify a literature-supported reference process condition.



\---



\## Objectives



The main objectives of this project are:



1\. Determine the implantation energy required to reach approximately 100 nm depth.

2\. Study the effect of implantation tilt on projected and lateral range.

3\. Analyze implantation-induced vacancy production.

4\. Identify process conditions within a 95–105 nm target-depth window.

5\. Use Python for systematic analysis and visualization of SRIM results.

6\. Compare the selected simulation condition with published Mg:GaN experimental work.

7\. Estimate an Mg concentration profile using a Gaussian approximation.

8\. Develop a literature-supported reference implantation and annealing process.



\---



\## Methodology



The project follows the workflow:



SRIM Simulation  

↓  

3 × 3 Design of Experiments  

↓  

Python Data Analysis  

↓  

Target-Depth Screening  

↓  

Process-Window Identification  

↓  

Literature Comparison  

↓  

Mg Concentration-Profile Estimation  

↓  

Literature-Supported Process Proposal



\---



\## SRIM Design of Experiments



Nine implantation conditions were analyzed.



| Energy | Tilt |

|---|---|

| 50 keV | 0° |

| 50 keV | 7° |

| 50 keV | 15° |

| 75 keV | 0° |

| 75 keV | 7° |

| 75 keV | 15° |

| 100 keV | 0° |

| 100 keV | 7° |

| 100 keV | 15° |



The main SRIM outputs analyzed were:



\- Projected range (Rp)

\- Longitudinal straggling

\- Lateral range

\- Vacancy production per incident ion



\---



\## Key Simulation Results



The average projected ranges obtained for each energy were approximately:



| Energy | Average Rp |

|---|---:|

| 50 keV | 50.5 nm |

| 75 keV | 75.7 nm |

| 100 keV | 101.4 nm |



This shows that increasing implantation energy significantly increases implantation depth.



The 100 keV conditions were therefore identified as the appropriate energy region for the approximately 100 nm target.



\---



\## 100-nm Process Window



A screening window of 95–105 nm was used for identifying conditions close to the 100 nm target.



The conditions within this window were:



| Run | Energy | Tilt | Rp | Depth Error | Lateral Range |

|---:|---:|---:|---:|---:|---:|

| 5 | 100 keV | 15° | 99.3 nm | 0.7 nm | 44.0 nm |

| 4 | 100 keV | 7° | 102.1 nm | 2.1 nm | 40.2 nm |

| 3 | 100 keV | 0° | 102.8 nm | 2.8 nm | 37.0 nm |



\---



\## Selected Reference Condition



The project uses:



\*\*100 keV / 7°\*\*



as the primary reference condition.



The SRIM results for this condition are:



| Parameter | Result |

|---|---:|

| Energy | 100 keV |

| Tilt | 7° |

| Projected range | 102.1 nm |

| Target depth | 100 nm |

| Depth error | 2.1 nm |

| Lateral range | 40.2 nm |

| Vacancies per ion | 828.4 |

| Longitudinal straggling | 45.2 nm |



Although the 15° condition has a slightly smaller depth error, the 7° condition provides a good balance between target depth and lateral spread and has published experimental precedent under comparable implantation conditions.



\---



\## Python Analysis



Python was used to process and analyze the SRIM results.



The analysis uses:



\- Python 3.11

\- Pandas

\- NumPy

\- Matplotlib



The analysis includes:



\- Dataset inspection

\- Energy and tilt comparisons

\- Energy × tilt tables

\- Target-depth ranking

\- Process-window screening

\- Fluence scaling

\- Vacancy-event estimation

\- Literature comparison

\- Gaussian Mg concentration-profile estimation

\- Final data visualization



\---



\## Literature Comparison



The selected 100 keV / 7° condition was compared with published Mg-implanted GaN experimental work.



The literature reference uses:



\- Mg implantation energy: 100 keV

\- Tilt: 7°

\- Fluence: approximately 3 × 10¹⁴ cm⁻²

\- Experimental Mg depth: approximately 100 nm based on SIMS



Our SRIM result:



\*\*Rp = 102.1 nm\*\*



is therefore consistent with the approximately 100 nm experimental Mg depth reported under comparable implantation conditions.



\### Important distinction



SRIM projected range and SIMS concentration peak are related quantities but are not identical measurements.



Therefore, this comparison is treated as a consistency check rather than an exact one-to-one validation.



\---



\## Fluence Analysis



A literature-referenced fluence of:



\*\*3 × 10¹⁴ ions/cm²\*\*



was used for the concentration-profile estimation.



Fluence represents the number of implanted ions per unit area:



\*\*ions/cm²\*\*



It should not be confused with concentration, which has units of:



\*\*ions/cm³\*\*



Vacancy-event scaling was also examined using:



\*\*Fluence × vacancies per ion\*\*



This provides an estimate of fluence-scaled vacancy events and should not be interpreted as the final permanent vacancy concentration.



\---



\## Estimated Mg Concentration Profile



For the selected 100 keV / 7° condition:



\- Projected range = 102.1 nm

\- Longitudinal straggling = 45.2 nm

\- Reference fluence = 3 × 10¹⁴ cm⁻²



A Gaussian approximation was used to estimate the Mg depth distribution.



The estimated peak concentration was:



\*\*2.648 × 10¹⁹ cm⁻³\*\*



with an estimated peak depth of:



\*\*102.1 nm\*\*



\### Important limitation



This concentration is a model-based estimate using the SRIM projected range and longitudinal straggling.



It is not an experimentally measured Mg concentration and is not an exact SRIM depth histogram.



\---



\## Reference Annealing Process



Published Mg-implanted GaN studies were used to establish a reference post-implantation annealing condition.



A literature-supported reference condition is approximately:



\- Temperature: \*\*1230°C\*\*

\- Time: \*\*30 min\*\*

\- Atmosphere: \*\*N₂\*\*



This is treated as a literature reference rather than an experimentally optimized condition for this project.



High-temperature annealing is associated with implantation-damage recovery and Mg activation, while excessive temperature can introduce problems such as surface degradation and dopant redistribution.



\---



\## Final Proposed Process



Based on the simulation results and literature comparison, the project proposes the following reference process:



\*\*Mg implantation into GaN\*\*



\- Energy: \*\*100 keV\*\*

\- Tilt: \*\*7°\*\*

\- Literature reference fluence: \*\*3 × 10¹⁴ cm⁻²\*\*



followed by a literature-supported reference annealing condition of approximately:



\*\*1230°C / 30 min / N₂\*\*



This process is a simulation- and literature-supported proposal and requires experimental validation.



\---



\## Results



\### Projected Range



!\[Projected Range](results/projected\_range\_heatmap.png)



\### Lateral Range



!\[Lateral Range](results/lateral\_range\_heatmap.png)



\### Vacancy Production



!\[Vacancy Production](results/vacancy\_heatmap.png)



\### 100-nm Process Window



!\[Process Window](results/process\_window.png)



\### Estimated Mg Depth Profile



!\[Mg Depth Profile](results/mg\_depth\_profile.png)



\---



\## Project Structure



```text

Mg\_GaN\_Project/

│

├── data/

│   └── SRIM\_9Run\_Master.csv

│

├── results/

│   ├── projected\_range\_heatmap.png

│   ├── lateral\_range\_heatmap.png

│   ├── vacancy\_heatmap.png

│   ├── process\_window.png

│   ├── mg\_depth\_profile.png

│   ├── ranked\_process\_conditions.csv

│   ├── 100nm\_process\_window.csv

│   ├── dose\_comparison.csv

│   └── literature\_validation.csv

│

├── src/

│   └── analysis.py

│

├── analysis.py

├── analysis\_working.py

├── README.md

└── requirements.txt

