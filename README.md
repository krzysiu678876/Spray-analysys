# Spray Analysys

Analysis of fuel spray behavior in a test chamber using **Mie Scattering**, image processing, and Python-based post-processing.  
Project based on laboratory work documented in `TOPT_raport1.pdf`, focused on the influence of **temperature** and **mass flow rate** on spray development and center-of-mass motion [file:9].

---

## Project Overview

The goal of this project is to evaluate how operating conditions affect fuel injection into a research chamber and to demonstrate a Mie Scattering measurement workflow [file:9].

The analysis was performed for five test cases, each recorded in 7 separate video series, then converted to TIFF images, processed in ImageJ, exported to CSV, and analyzed in Python using NumPy-based calculations of time and droplet cloud center of mass [file:9].

---

## Test Cases

The following operating conditions were investigated [file:9]:

| Case | Temperature | Mass Flow Rate |
|---|---:|---:|
| 1 | 60°C | 305 kg/h |
| 2 | 60°C | 0 kg/h |
| 3 | 100°C | 305 kg/h |
| 4 | 140°C | 0 kg/h |
| 5 | 140°C | 305 kg/h |

Each case includes 7 measurement series, and final trends were obtained using arithmetic averaging across the series [file:9].

---

## Methodology

### Measurement workflow

1. Record spray videos for each operating condition.
2. Convert recordings to `.tiff` using **FPV4**.
3. Process images in **ImageJ**.
4. Export particle data to CSV.
5. Post-process data in Python [file:9].

### Image filtering

During ImageJ processing:
- particles smaller than 10 pixels were ignored,
- thresholding was applied to remove weakly illuminated pixels [file:9].

### Extracted quantities

The CSV files contain particle-level data for all frames. The most important fields are [file:9]:
- `X`, `Y` — particle position in pixels,
- `Area` — droplet area in pixels,
- `Slice` — frame number.

### Python calculations

For each frame, the script computes [file:9]:
- time, based on frame number and camera rate of **10,000 fps**,
- center-of-mass coordinates:

\[
X_{CM} = \frac{\sum (X_i \cdot A_i)}{\sum A_i}, \qquad
Y_{CM} = \frac{\sum (Y_i \cdot A_i)}{\sum A_i}
\]

The results are then averaged over 7 measurement series for each operating point [file:9].

---

## Outputs

The report presents the following processed results [file:9]:

- Average center-of-mass position in the **X direction**
- Average center-of-mass position in the **Y direction**
- **Trajectory** of the average center of mass in the X-Y plane
- **Total spray area** as a function of time
- Example plot with **deviation bands** for selected cases

These outputs help compare the spatial evolution and stability of the spray cloud under different thermal and flow conditions [file:9].

---

## Main Findings

Key conclusions from the report include [file:9]:

- Measurement noise strongly affects the analysis, especially at the beginning of the sequence before the spray cloud is fully visible.
- Even after conversion to 8-bit images, noise can artificially increase both detected spray area and center-of-mass position.
- For **zero mass flow rate**, there is practically no meaningful displacement in the X direction, which matches the expectation of observing more of a cloud than a directed jet.
- For **nonzero mass flow rate**, the difference in X-direction behavior between **60°C** and **100°C** is small within the error range, while the largest difference appears at **140°C**.
- In the **Y direction**, the smallest difference is observed at higher temperature trends, and the variation is not clearly correlated with mass flow rate.
- The largest total center-of-mass migration occurs for:
  - **ṁ = 305 kg/h, T = 140°C**
  - **ṁ = 0 kg/h, T = 60°C** [file:9]

---

## Tools Used

- **FPV4** — conversion of recorded videos to TIFF images [file:9]
- **ImageJ** — particle detection and threshold-based filtering [file:9]
- **Python**
- **NumPy** — frame-by-frame numerical post-processing [file:9]

---

## Limitations

This analysis is sensitive to image noise and threshold selection, especially in the early frames of each sequence [file:9].  
A possible improvement would be to either start the analysis later in time or apply machine-learning-based image segmentation methods, although that would increase implementation complexity and processing time [file:9].

---

## Authors

- **Jan Starachowski**
- **Kacper Malinowski** [file:9]
