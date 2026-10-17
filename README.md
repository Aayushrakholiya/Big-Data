<div align="center">

# 📊 Big Data — Canadian Labour Force Analytics

**An end-to-end big-data pipeline over a huge Government of Canada labour force survey: stream-parse gigabytes of SDMX XML, aggregate employment counts, and explore them in Power BI.**

Python · SDMX XML Streaming · ETL · Power BI

<br>

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![XML ETL](https://img.shields.io/badge/SDMX_XML_ETL-orange?style=flat-square)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logo=powerbi&logoColor=black)
![Statistics Canada](https://img.shields.io/badge/Data-Statistics_Canada-red?style=flat-square)

</div>

---

## 📌 Table of Contents

- [About](#-about)
- [The Problem](#-the-problem)
- [Pipeline](#-pipeline)
- [Project Structure](#%EF%B8%8F-project-structure)
- [Getting Started](#-getting-started)
- [Team](#-team)

## 👋 About

Statistics Canada publishes its Labour Force Survey as a **12 GB SDMX XML file** — far too large to load into memory, let alone Excel. This project (built with Darsh Patel) takes that raw federal dataset and turns it into something explorable:

1. **Stream-parse** the XML with `ET.iterparse`, aggregating on the fly and clearing elements as it goes so memory stays flat no matter the file size
2. **Filter and aggregate** employment counts by province, occupation, and age group
3. **Export a tidy CSV** that feeds a **Power BI dashboard** (`a6.pbix`) for interactive analysis

## 🧩 The Problem

The source dataset (`99-012-X2011033`) is the Canadian Labour Force Survey in SDMX format:

- 11 GB `Generic_*.xml` with millions of observation series
- A companion `Structure_*.xml` describing every code list (provinces, NOC 2011 occupation codes, age groups)

Naively opening the XML in a tree editor kills the machine — which is exactly the point of the assignment. The pipeline only keeps records whose dimensions fall inside curated code sets:

| Dimension | Kept values |
| --- | --- |
| **Geography** | Canada + 13 provinces/territories (`01`, `10`, `11`, … `62`) |
| **Occupation (NOC 2011)** | 10 major groups — management, business/finance, health, sales, trades, and more |
| **Age group** | 5 bands (15–24 years and up) |

## ⚙️ Pipeline

```text
┌───────────────────────────┐     ┌──────────────────────────────┐     ┌──────────────────┐
│  99-012-X2011033.ZIP      │     │  extract_data.py             │     │  Data.csv        │
│  • Generic XML (11 GB)    │ ──▶ │  1. Parse structure codelists│ ──▶ │  Province_Name,  │
│  • Structure XML (code    │     │  2. iterparse stream,        │     │  Occupation,     │
│    lists for GEO/NOC/AGE) │     │     filter + aggregate       │     │  Age_Group,      │
│                           │     │  3. Clear elements as we go  │     │  Count           │
└───────────────────────────┘     └──────────────────────────────┘     └────────┬─────────┘
                                                                                │
                                                                        ┌───────▼────────┐
                                                                        │  a6.pbix       │
                                                                        │  Power BI      │
                                                                        │  dashboard     │
                                                                        └────────────────┘
```

Key streaming trick: the parser listens for `</Series>` end events, reads just the series key + observation value, accumulates into a `defaultdict`, then calls `element.clear()` — so RAM never grows with file size.

## 🗂️ Project Structure

```text
Big-Data/
├── extract_data (1).py        🐍 Streaming ETL script (SDMX XML → CSV)
├── 99-012-X2011033.ZIP        📦 Raw Statistics Canada source (12 GB uncompressed)
├── a6.zip                     📈 Power BI dashboard (a6.pbix)
├── Data (1).csv               🧾 Aggregated output sample
└── arakholiya_dpatel_A6_Report.pdf   📄 Project report
```

## 🚀 Getting Started

```bash
# 1. unzip the source data (needs ~12 GB free)
unzip 99-012-X2011033.ZIP

# 2. run the extraction (script expects the XMLs in the working dir)
python "extract_data (1).py"

# 3. output lands in output/Data.csv — open it or explore a6.pbix in Power BI Desktop
```

Output schema: `Province_Name, Occupation, Age_Group, Count` — ready for Power BI, Excel, or any BI tool.

## 👥 Team

Built by **Ayushkumar Rakholiya & Darsh Patel** — Assignment 6 report included as PDF.

---

<div align="center">

⭐ **Star this repo if you find it useful** ⭐

</div>
