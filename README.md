# Data-Science

A curated learning lab of notebooks and mini-experiments across ML, NLP, web scraping, data engineering, and Haystack (RAG/agents). Built to document progress, practice core skills, and showcase growth over time.

> Note: This repository does not currently define a single package or entry point. Most content is intended to be run as standalone notebooks (`.ipynb`) or Python scripts (`.py`).

## Learning Themes & Skills Matrix

| Theme | Skills Practiced | Tools / Libraries | Key Artifacts |
|---|---|---|---|
| Classical ML (Foundations) | data prep, model training/validation, evaluation | pandas, numpy, scikit-learn, matplotlib/seaborn | [Hands on Machine Learning Book/CH1_TO_CH7.ipynb](Hands%20on%20Machine%20Learning%20Book/CH1_TO_CH7.ipynb) |
| Data Analysis (Pandas) | indexing, grouping, reshaping, time series basics | pandas, numpy | [Python for Data Analysis/python_for_data_analysis.ipynb](archive/Python for Data Analysis/CH1_CH5.ipynb) |
| NLP | tokenization, embeddings intro, classic NLP workflow | pandas, numpy, visualization libs | [NLP/jurafsky_nlp_book.ipynb](Roots of Knowledge/stanford cs224n/archive/Naive Bayes/Naive Bayes.ipynb) |
| Web Scraping | HTTP requests, parsing, exporting CSV/XLSX | requests, parsing libs (varied), pandas | [Web Scraping/web_scraping_football_news_websites.ipynb](Web%20Scraping/web_scraping_football_news_websites.ipynb) + [outputs](Web%20Scraping/scrapped_websites/) |
| Data Engineering (I/O) | reading/writing CSV & JSON, file handling | pandas, Python stdlib | Chapter 3 scripts under [Data Engineering …/Chapter 3 Reading and Writing Files](Data%20Engineering%20with%20Python%20Work%20with%20massive%20datasets%20to%20design%20data%20models%20and%20automate%20data%20pipelines%20using%20Python%20(Crickard,%20Paul)/Chapter%203%20Reading%20and%20Writing%20Files/) |
| Haystack (RAG/Agents) | pipelines, components, tool-calling agents | haystack (version TBD) | [haystack/getting_start.py](haystack/Concepts/getting_start.py), [Pipelines/](haystack/Concepts/Pipelines/), [Agents/](haystack/Concepts/Agents/) |

## Highlights & Milestones

- Completed core ML essentials through Géron’s Hands-On ML (Ch.1–7) with practice notebooks: feature scaling, model selection, and evaluation workflows.
- Built a pandas-focused notebook (from McKinney) exploring indexing, groupby, and reshaping patterns for tidy analysis.
- Created web scraping notebooks to collect football-related data and exported cleaned datasets to CSV/XLSX.
- Set up Haystack quickstart and explored pipeline templates (RAG, Indexing, Generative QA) and agent state/tool patterns.
- Practiced robust data I/O patterns (CSV/JSON) from the Data Engineering book’s examples.

## Lessons Learned (selected)

- Reliable data pipelines start with clear, reproducible I/O (consistent paths, schemas, and encodings).
- In notebooks, small, testable steps and frequent checkpoints (visualizations/metrics) make debugging easier.
- For ML baselines, start simple (linear/logistic, tree-based) before trying complex models; keep evaluation honest with proper splits.
- Web scraping benefits from idempotent exports and snapshots—store raw HTML/CSV alongside processed outputs when possible.
- LLM/RAG pipelines are orchestration-heavy—log intermediate node outputs and keep components loosely coupled.


## Stack Overview

- Language: Python (modern 3.x)
- Typical tooling:
  - Jupyter Notebook/JupyterLab for notebooks
  - Standard Python runtime for scripts
  - Likely common libraries (based on filenames and context): pandas, numpy, scikit-learn, matplotlib/seaborn, and Haystack. Specific versions are not pinned in this repo.
- Package manager: Not specified in the repo.

TODO:
- Add `requirements.txt` or `pyproject.toml` (or `environment.yml` for conda) to pin dependencies and versions.
- Document exact Python version used (e.g., 3.9/3.10/3.11).

---

## Repository Structure (high level)

- `Hands on Machine Learning Book/` — Notebook(s) from Géron’s Hands-On ML (e.g., `CH1_TO_CH7.ipynb`).
- `Python for Data Analysis/` — Notebook(s) from McKinney’s Python for Data Analysis (e.g., `python_for_data_analysis.ipynb`).
- `NLP/` — NLP-related notebook(s) (e.g., `jurafsky_nlp_book.ipynb`).
- `Web Scraping/` — Web scraping notebooks plus exported datasets in `scrapped_websites/`.
- `haystack/` — Examples and notes around the Haystack framework:
  - `Agents/`, `Components/`, `Pipelines/` — demos, templates, and theoretical notes.
  - `getting_start.py` — simple getting started script for Haystack.
- `datasets/` — Example datasets (e.g., `IMDB Dataset.csv`, `housing/`, `seeds/`).
- `Data Engineering with Python Work with massive datasets to design data models and automate data pipelines using Python (Crickard, Paul)/` — Chapter 3 examples (reading/writing files with pandas/CSV/JSON).
- `complementary_graphs_files/` — Images/arrays for plotting or examples.
- `Theoretical Notes/` — Misc notes (includes non-code files like `.xlsx`).
- `README.md` — This file.

This structure suggests the repo is a learning workspace with multiple domains rather than a deployable application.

---

## Requirements

Because dependencies are not pinned in the repository, install core tools first:

- Python 3 (modern version). Recommended to use a virtual environment.
- JupyterLab or Jupyter Notebook for `.ipynb` files.

Common libraries you may need (based on files and typical usage):
- pandas, numpy, scikit-learn
- matplotlib, seaborn
- jupyter, ipykernel
- For Haystack examples: `haystack-ai` (or corresponding package for your version of Haystack), plus any embedding/LLM backends you choose

TODO:
- Publish an authoritative dependency list (`requirements.txt` or `environment.yml`).
- Note any OS-specific dependencies (Windows/Mac/Linux) if encountered.

---

## Setup

1) Clone the repo
```
git clone <this-repo-url>
cd Data-Science
```

2) Create and activate a virtual environment (choose one)
- venv (built-in)
```
python -m venv .venv
.\.venv\Scripts\activate
```
- conda (if you prefer)
```
conda create -n ds-env python=3.10
conda activate ds-env
```

3) Install packages
- pip (placeholder until requirements are published)
```
pip install -U pip
# TODO: replace with: pip install -r requirements.txt
# Temporary guesses (adjust as needed):
pip install jupyter pandas numpy scikit-learn matplotlib seaborn
# For Haystack examples (adjust per your Haystack version):
# pip install haystack-ai
```
- conda (placeholder)
```
# TODO: add environment.yml and use: conda env create -f environment.yml
```

4) Enable the kernel for Jupyter (if using venv)
```
python -m ipykernel install --user --name data-science-notes
```

---

## Running Notebooks

- Launch JupyterLab or Jupyter Notebook
```
jupyter lab
# or
jupyter notebook
```
- Open any `.ipynb` under the folders (e.g., `Hands on Machine Learning Book/CH1_TO_CH7.ipynb`).
- If a notebook needs data from `datasets/`, ensure paths are correct relative to the notebook.

---

## Running Python Scripts

There is no unified entry point. Run individual scripts as needed. Examples:

```
# Haystack intro script (adjust if the filename changes)
python .\haystack\getting_start.py

# Data engineering chapter examples
python \
  ".\Data Engineering with Python Work with massive datasets to design data models and automate data pipelines using Python (Crickard, Paul)\Chapter 3 Reading and Writing Files\Reading CSVs.py"

python \
  ".\Data Engineering with Python Work with massive datasets to design data models and automate data pipelines using Python (Crickard, Paul)\Chapter 3 Reading and Writing Files\Reading json with pandas.py"

python \
  ".\Data Engineering with Python Work with massive datasets to design data models and automate data pipelines using Python (Crickard, Paul)\Chapter 3 Reading and Writing Files\Very basic writing.py"
```

Notes:
- Some files and folders contain spaces; on Windows PowerShell, quoting the path as shown above helps.
- Some scripts may expect certain CSV/JSON files located next to them; keep relative paths intact.

---

## Scripts and Utilities (non-exhaustive)

- Haystack:
  - `haystack/getting_start.py` — quick start script.
  - `haystack/Pipelines/` — templates for RAG, Chat with website, Generative QA, Indexing, and semantic search.
  - `haystack/Agents/` — examples for agent state, tools, and message handling.
  - `haystack/Components/` — custom components and super-components demos.
- Data engineering (Crickard book, Chapter 3):
  - `Reading CSVs.py`, `Reading json with pandas.py`, `Very basic writing.py` — basic I/O with pandas/CSV/JSON.
- Web scraping:
  - `Web Scraping/web_scraping_football_news_websites.ipynb`
  - `Web Scraping/web_scrabing_football_tshirts.ipynb`
  - Outputs under `Web Scraping/scrapped_websites/` (CSV/XLSX).
- ML & analysis notebooks:
  - `Hands on Machine Learning Book/CH1_TO_CH7.ipynb`
  - `Python for Data Analysis/python_for_data_analysis.ipynb`
  - `NLP/jurafsky_nlp_book.ipynb`

TODO:
- Add a consolidated `make`/`Invoke`/`nox`/`tox` command set (optional).

---

## Environment Variables

No environment variables are defined in this repository. Some Haystack or external-API examples may require credentials (e.g., OpenAI/Hugging Face) depending on which components you choose.

TODO:
- If any script requires API keys or endpoints, document the variable names here (e.g., `OPENAI_API_KEY`, `HF_TOKEN`, etc.) and how they’re used.

---

## Data

- Bundled sample datasets are provided under `datasets/` and elsewhere (e.g., `Web Scraping/scrapped_websites/`).
- Ensure licenses/terms of the datasets permit your intended use.

TODO:
- Document dataset provenance and licenses if necessary.

---

## Changelog

- 2025-11-08: Overhauled README with structure overview, setup guidance, and TODOs.
