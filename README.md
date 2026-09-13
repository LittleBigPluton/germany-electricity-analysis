# Germany Electricity Analysis 2025

[![CI](https://github.com/LittleBigPluton/germany-electricity-analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/LittleBigPluton/germany-electricity-analysis/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)

Python-based analysis of Germany's 2025 electricity generation and consumption using SMARD data from the German Federal Network Agency.

The project compares renewable and conventional generation, production and consumption, renewable share, residual load, source-level variability, monthly energy balances, and within-year trends. It is structured as an installable Python package with a command-line workflow, automated tests, CI, and interactive Plotly visualizations.

## Key findings

- **Renewable generation exceeded conventional generation on 274 of 365 days.**
- **Total electricity generation exceeded total consumption on 82 of 365 days.**
- **Renewable generation alone exceeded total daily consumption on 2 days:** October 5 and October 26.
- **Highest daily renewable share:** **86.76%** on October 26.
- **Lowest daily renewable share:** **22.80%** on November 8.
- **Highest monthly renewable share:** **73.30%** in June.
- **Highest monthly consumption:** January.
- **Highest monthly residual load:** February.

These results show strong renewable penetration across much of the year, while also highlighting substantial residual load and the continuing need for balancing, storage, grid management, imports, or dispatchable generation during lower-renewable periods.

> **Interpretation note:** Renewable generation exceeding total daily consumption does **not** mean every hour of that day was fully renewable. The comparison is based on aggregated daily energy totals and does not model intraday balancing, storage, grid constraints, imports, or exports.

## Explore the results

- **[Detailed analysis](docs/Analysis/README.md)** — methodology, annual and monthly results, daily extremes, variability, trends, limitations, and interpretation.
- **[Interactive figure gallery](https://www.umutgokdemir.com/germany-electricity-analysis/)** — interactive Plotly visualizations published as HTML.
- **[Medium article](https://medium.com/@ckmzyol/germanys-electricity-in-2025-what-a-full-year-of-data-shows-6f5e6708681d)** — narrative overview of the analysis.

## Analysis scope

The project studies Germany's electricity system during 2025 using exported SMARD data.

Main questions include:

- How did renewable and conventional generation compare throughout the year?
- How often did total generation exceed total consumption?
- How often did renewable generation alone exceed total daily consumption?
- How did renewable share and residual load vary across days and months?
- Which periods showed the highest production, consumption, renewable share, and residual load?
- How variable were individual generation sources?
- What broad within-year trends appear in total production and consumption?

## Main metrics

### Renewable share

```text
Renewable Share [%] = Total Renewable Generation / Total Production × 100
```

### Residual load

```text
Residual Load = Total Consumption - Total Renewable Generation
```

### Net balance

```text
Net Balance = Total Production - Total Consumption
```

These metrics are used throughout the analysis and exported reports.

## Representative outputs

### Renewable share

![Renewable share drilldown](docs/Figures_png/Renewable_Share_Drilldown.png)

### Residual load

![Residual load drilldown](docs/Figures_png/Residual_Load_Drilldown.png)

### Production and consumption trends

![Production and consumption trends](docs/Figures_png/Total_Consumption_and_Production_with_Trend_Lines.png)

Interactive versions of these and the remaining figures are available in the **[figure gallery](https://www.umutgokdemir.com/germany-electricity-analysis/)**.

## Repository structure

```text
germany-electricity-analysis/
├── .github/
│   └── workflows/
│       └── ci.yml                     # Ruff + pytest CI
├── data/
│   └── yearly/
│       └── energy/
│           └── 2025/
│               ├── raw/               # Raw SMARD CSV exports
│               └── processed/         # Generated processed data
├── docs/
│   ├── analysis/
│   │   ├── README.md                  # Detailed interpretation
│   │   ├── analysis.txt
│   │   ├── key_findings_2025.txt
│   │   ├── Monthly_based_summary_stats.csv
│   │   ├── Top_Consumption_Days.csv
│   │   ├── Top_Production_Days.csv
│   │   ├── Top_Renewable_days.csv
│   │   └── Top_Residual_Load_Days.csv
│   ├── Figures_html/                  # Interactive Plotly exports
│   ├── Figures_png/                   # Static previews
│   ├── index.html                     # Published gallery
│   └── .nojekyll
├── src/
│   └── electricity_analyse/
│       ├── __init__.py
│       ├── analysis.py
│       ├── cli.py
│       ├── config.py
│       ├── export_utils.py
│       ├── io_utils.py
│       ├── plotting.py
│       └── stats_utils.py
├── tests/
│   ├── test_analysis.py
│   ├── test_io_utils.py
│   └── test_stats_utils.py
├── pyproject.toml
├── LICENSE
└── README.md
```

## Installation

### Requirements

- Python **3.10+**
- `pip`
- Git

Clone the repository:

```bash
git clone https://github.com/LittleBigPluton/germany-electricity-analysis.git
cd germany-electricity-analysis
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project:

```bash
python -m pip install -e .
```

For development tools including pytest and Ruff:

```bash
python -m pip install -e ".[dev]"
```

## Run the analysis

The package exposes the command-line entry point:

```bash
electricity-analyse
```

The workflow:

1. normalizes raw SMARD CSV headers,
2. loads hourly generation and consumption data,
3. builds the hourly generation/consumption visualization,
4. loads daily generation data,
5. calculates renewable, conventional, and total production,
6. aggregates hourly consumption to daily consumption,
7. calculates renewable share,
8. calculates residual load,
9. exports comparison results,
10. generates the monthly summary,
11. exports top-day rankings,
12. computes variability statistics,
13. generates key findings,
14. exports interactive HTML and PNG visualizations.

The command regenerates the processed datasets, analysis reports, summary CSVs, and figures.

## Configuration

Project paths, source categories, renewable/conventional groupings, datetime formats, plotting options, and file locations are defined in:

```text
src/electricity_analyse/config.py
```

The raw 2025 SMARD exports are expected under:

```text
data/yearly/energy/2025/raw/
```

Processed outputs are written to:

```text
data/yearly/energy/2025/processed/
```

Analysis reports are written to:

```text
docs/Analysis/
```

Interactive figures are written to:

```text
docs/Figures_html/
```

Static figure previews are written to:

```text
docs/Figures_png/
```

## Generated outputs

### Analysis reports

The main generated analysis artifacts are stored in `docs/Analysis/`:

```text
analysis.txt
key_findings_2025.txt
Monthly_based_summary_stats.csv
Top_Consumption_Days.csv
Top_Production_Days.csv
Top_Renewable_days.csv
Top_Residual_Load_Days.csv
```

For interpretation of these outputs, see the **[detailed analysis](docs/Analysis/README.md)**.

### Interactive figures

The workflow exports Plotly HTML figures including:

- hourly generation mix and total consumption,
- daily generation composition,
- renewable-share drilldown,
- residual-load drilldown,
- monthly energy summary,
- generation-source variability,
- aggregate production/consumption variability,
- total production and consumption trend lines.

Explore them at:

**https://www.umutgokdemir.com/germany-electricity-analysis/**

## Testing

Run the automated test suite with:

```bash
pytest
```

The tests cover deterministic parts of the analysis pipeline, including:

- daily generation aggregation,
- date indexing and validation,
- hourly-to-daily consumption aggregation,
- comparison-day logic,
- monthly summary generation,
- CSV/input helpers,
- and statistical utility functions.

Run Ruff separately with:

```bash
ruff check src tests
```

## Continuous integration

GitHub Actions runs linting and tests on pushes and pull requests to `main`.

The CI workflow checks:

```text
install package
    ↓
ruff check
    ↓
pytest + coverage
```

across the supported Python versions defined by the project workflow.

## Data source

The raw data comes from **SMARD**, the electricity-market data platform of the German Federal Network Agency.

- **SMARD download center:** https://www.smard.de/home/downloadcenter/download-marktdaten/

The repository uses CSV exports for:

- hourly electricity generation by source,
- hourly electricity consumption,
- daily electricity generation by source.

## Technical stack

- Python
- pandas
- NumPy
- Plotly
- Matplotlib
- statsmodels
- pytest
- Ruff
- `pyproject.toml` package structure
- GitHub Actions
- GitHub Pages / static HTML publication

## Interpretation and limitations

This repository analyzes electricity generation and consumption from the available SMARD exports. It does **not** model:

- imports or exports,
- storage charging/discharging,
- transmission constraints,
- balancing-market behavior,
- electricity prices,
- plant dispatch constraints,
- demand response,
- or forecasting uncertainty.

The result that renewable generation exceeded total consumption on two days applies to **daily aggregated energy totals**. It does not imply that every hour on those days was fully supplied by renewables.

For a fuller discussion of the results and limitations, see the **[detailed analysis](docs/Analysis/README.md)**.

## License

This project is released under the MIT License. See [`LICENSE`](LICENSE) for details.
