# Climate Change — Longitudinal Multivariate Analysis

Bachelor's Thesis in **Statistics and Information Management**  
University of Milano-Bicocca

## Overview

Climate change is a multidimensional phenomenon involving environmental, economic, and geographical factors that evolve jointly over time.

This project investigates long-term patterns associated with both potential **drivers** and plausible **consequences** of climate change across countries.

The analysis combines historical data on **CO₂ emissions, emission intensity, international trade, surface temperature, forest and carbon indicators, and climate-related disasters**.

The main objective was to reduce high-dimensional longitudinal information into interpretable indicators and identify countries and groups of countries displaying distinctive environmental trajectories.

The study is entirely **exploratory**: its purpose is to identify structures, temporal patterns, similarities, and anomalies in the data rather than estimate causal effects.

## Data

The analysis is based on official data collected from the **International Monetary Fund Climate Change Indicators Dashboard**.

Five datasets were selected from four main areas:

- Greenhouse Gas Emissions
- Climate and Weather
- Mitigation
- Adaptation

Dataset selection was based on:

- temporal coverage;
- country-level granularity;
- data completeness;
- consistency across datasets.

Depending on data availability, the analysis covers approximately **60–66 countries** and historical periods extending over several decades.

## What I Did

The project was developed as a progressive multivariate analysis pipeline.

### Exploratory Data Analysis

Initial analyses were conducted to study distributions, temporal trends, and extreme observations through:

- time-series plots;
- violin plots;
- raincloud plots;
- correlation analysis;
- heatmaps;
- geographical visualisations;
- robust statistics for outlier detection.

### Longitudinal Principal Component Analysis

The original variables were transformed into a smaller set of interpretable longitudinal indicators using **Principal Component Analysis (PCA)**.

The objective was to reduce dimensionality while preserving the main temporal patterns describing the environmental evolution of each country.

### PARAFAC Decomposition

For the more complex emissions dataset, where observations varied simultaneously across:

- countries;
- years;
- environmental indicators;
- industrial sectors;

the analysis was extended using **PARAFAC**, a multiway decomposition technique designed for three-dimensional data structures.

This allowed the simultaneous identification of latent patterns across countries, industries, and time.

### Multivariate Time-Series Clustering

The longitudinal indicators obtained from the dimensionality-reduction stage were subsequently analysed using **multivariate time-series clustering**.

Dynamic Time Warping-based distances were used to group countries according to similarities in their environmental trajectories rather than only their absolute values.

Climate-related disaster indicators were then analysed within the resulting clusters to investigate how different environmental profiles were associated with different patterns of potential climate consequences.

## Notable Results

The exploratory analysis revealed several persistent structures in the data.

- **China, India, the United States, and Russia** repeatedly emerged among the countries with the most extreme emission profiles.

- Industrial and transport-related sectors showed substantially higher absolute CO₂ emissions than most service-sector activities.

- Emission intensity generally decreased over the analysed period, indicating changes in the relationship between economic output and emissions.

- A three-factor **PARAFAC model explained approximately 75.6% of the variability** in the multiway emissions dataset.

- The PARAFAC components captured distinct dimensions related to:
  - emission intensity and emission multipliers;
  - absolute emissions;
  - emission concentration across economic activities.

- PCA applied to climate-related disasters reduced six original variables to three components explaining approximately **82% of total variance**.

- These components were mainly associated with:
  - hydrogeological events;
  - storms and wildfires;
  - extreme-temperature events.

- Longitudinal clustering separated **61 countries into three distinct temporal profiles**.

- One large cluster, mainly composed of European and other Western countries, showed decreasing emission-related indicators, while the remaining clusters displayed different emission and forest-related trajectories.

- A recurring result throughout the study was the persistence of specific **outlier countries across multiple environmental dimensions**, suggesting that extreme environmental profiles were not restricted to a single indicator or dataset.

## Technologies and Methods

### Languages and Software

- **R**
- **RStudio**
- **Tableau**

### R Packages

- `ggplot2`
- `ggpubr`
- `dplyr`
- `tidyr`
- `psych`
- `corrplot`
- `multiway`
- `dtwclust`

### Statistical and Mathematical Methods

- Exploratory Data Analysis
- Longitudinal Data Analysis
- Principal Component Analysis
- Dimensionality Reduction
- PARAFAC / Multiway Tensor Decomposition
- Multivariate Time-Series Analysis
- Dynamic Time Warping
- Time-Series Clustering
- Correlation Analysis
- Outlier Analysis
- Robust Statistics
- Median Absolute Deviation
- Temporal Data Visualisation
- Spatial Data Visualisation

## Repository

This repository is intended as a **portfolio presentation of the project**.

It contains the thesis and selected results and visualisations. The original analysis code is not included.
