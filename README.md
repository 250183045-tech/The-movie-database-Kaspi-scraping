# E-Commerce Market Intelligence: Kaspi.kz Strategic Analysis

## Table of Contents
- [About](#about)
- [Technical Pipeline](#technical-pipeline)
- [Getting Started](#getting-started)
- [Data Structure](#data-structure)
- [Key Insights](#key-insights)
- [Repository Structure](#repository-structure)
- [Execution Guide](#execution-guide)

## About
This project provides a comprehensive analytical framework for the e-commerce sector, focusing on the jewelry and accessories market. It integrates asynchronous web scraping, automated data enrichment, and advanced statistical modeling to transform raw web data into actionable market insights.

## Technical Pipeline
1. **Data Acquisition:** Asynchronous scraping via `Playwright` and `Asyncio`.
2. **Preprocessing:** Heuristic material detection and brand standardization.
3. **Exploratory Data Analysis:** Price distribution and anomaly detection using the IQR method.
4. **Predictive Modeling:** Linear Regression analysis of market success factors.

## Getting Started
### Prerequisites
- Python 3.9+
- Playwright browser binaries

### Installation
1. Clone the repository:
   `git clone https://github.com/yourusername/project-name.git`
2. Install dependencies:
   `pip install -r requirements.txt`
3. Install Playwright:
   `playwright install`

## Data Structure
The final dataset (`kaspi_smart_data.csv`) includes the following key features:
- **Price:** Sanitized numeric current price.
- **Material:** Categorized tier (Luxury, Silver, Alloy).
- **Type:** Product classification (Tiara, Hairpin, etc.).
- **Success Score:** Calculated success metric based on ratings and engagement.

## Key Insights
- Statistical analysis revealed that Luxury (Gold/Gem) items concentrate 21,7% of total market value.
- Machine Learning coefficients indicate that product ratings have a stronger impact on success than raw popularity.

## Repository Structure
* `kaspi_data_part3.py` — Asynchronous scraping engine.
* `cleaning.py` — Data enrichment and feature engineering module.
* `analysis.py` — Statistical modeling and hypothesis testing script.
* `visualization.py` — Automated 12-chart reporting suite.
* `requirements.txt` — List of required Python dependencies.

---

## Execution Guide
1. **Install dependencies:** `pip install -r requirements.txt`
2. **Run the pipeline in order:** `python scripts/kaspi_data_part3.py`  
   `python cleaning.py`  
   `python analysis.py`  
   `python visualization.py`

---
