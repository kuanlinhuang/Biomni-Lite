# Biomni-Lite

A lightweight, containerizable biomedical AI agent powered by a strong LLM. No local data lake required — datasets are fetched on demand from Zenodo.

Biomni-Lite ships two agents:

| Agent | Description |
|-------|-------------|
| **A1** | General-purpose biomedical agent |
| **AD1** | Extends A1 with Alzheimer's Disease domain expertise and data-sourcing protocols |

## Key Differences from Biomni

| Feature | Biomni | Biomni-Lite |
|---------|--------|-------------|
| Data lake | ~11 GB auto-download | On-demand from Zenodo |
| Environment | Heavy conda (100+ pkgs, R, CLI) | `pip install biomni-lite` |
| Default LLM | claude-sonnet-4-5 | claude-opus-4-5 |
| Docker-ready | No | Yes |
| Tool count | 180+ | 180+ (same) |
| External API tools | Yes | Yes |

## Quick Start (Python)

```bash
pip install biomni-lite
```

### A1 — General Biomedical Agent

```python
from biomni.agent import A1

agent = A1()  # No download on init
agent.go("Query UniProt for TP53 protein information")
agent.go("Search PubMed for recent APOE4 Alzheimer's disease papers")
agent.go("Analyze GWAS hits for type 2 diabetes")  # Downloads data from Zenodo on demand
```

### AD1 — Alzheimer's Disease Agent

```python
from biomni.agent import AD1

agent = AD1()
agent.go("Find GWAS loci associated with Alzheimer's disease across multi-ancestry cohorts")
agent.go("Annotate the top ADSP rare-variant hits with gnomAD and ClinVar")
```

## Data Lake

All 77 curated datasets are available on demand at: **https://zenodo.org/records/18759554**

The agent automatically downloads only the files it needs for each task and caches them locally.

To manually download a file:
```python
from biomni.tool.support_tools import download_data_lake_file

path = download_data_lake_file("gwas_catalog.pkl")
```

## Docker Deployment

### 1. Setup

```bash
# Copy the example env file and add your API key
cp .env.example .env
# Edit .env: ANTHROPIC_API_KEY=your_key_here
```

### 2. Gradio Web UI (recommended)

Launch the web interface — by default an agent-selector page appears at
startup where you can choose between A1 and AD1:

```bash
docker compose up biomni-lite-gradio
# → Open http://localhost:7860
```

To skip the selector and launch a specific agent directly, set
`BIOMNI_AGENT` in your `.env` (or pass it inline):

```bash
# Launch A1 directly
BIOMNI_AGENT=a1  docker compose up biomni-lite-gradio

# Launch AD1 directly
BIOMNI_AGENT=ad1 docker compose up biomni-lite-gradio
```

### 3. Command-Line (one-shot)

Run a single query from the command line — no web server needed:

```bash
# A1 agent
docker compose run --rm biomni-lite python -c "
from biomni.agent import A1
A1().go('List all protein-protein interaction datasets available')
"

# AD1 agent
docker compose run --rm biomni-lite python -c "
from biomni.agent import AD1
AD1().go('Summarize the latest Alzheimer GWAS meta-analysis results')
"
```

### 4. Deploy on a VM

```bash
# On any VM with Docker:
git clone <repo-url>
cd Biomni-Lite
echo "ANTHROPIC_API_KEY=your_key" > .env
docker compose up biomni-lite-gradio -d
# → Open http://<vm-ip>:7860
```

## Configuration

All settings can be set via environment variables or constructor arguments:

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | — | Required for Claude (default model) |
| `OPENAI_API_KEY` | — | Required for GPT models |
| `BIOMNI_LLM` | `claude-opus-4-5` | LLM model name |
| `BIOMNI_PATH` | `./data` | Working directory |
| `BIOMNI_TIMEOUT_SECONDS` | `600` | Code execution timeout |
| `BIOMNI_AGENT` | _(selector)_ | Agent for Gradio UI: `a1` or `ad1` |

```python
agent = A1(
    llm="claude-opus-4-5",   # or "gpt-4o", "gemini-2.0-flash", etc.
    path="./workspace",
    timeout_seconds=900,
)
```

## Tools

Biomni-Lite includes all 180+ biomedical tools from Biomni:
- **53 External Database APIs**: UniProt, AlphaFold, PDB, Ensembl, ClinVar, GWAS Catalog, gnomAD, Open Targets, cBioPortal, KEGG, STRING, OpenFDA, Reactome, and more
- **Literature search**: PubMed, arXiv, Google Scholar
- **Code execution**: Python REPL with bioinformatics libraries
- **Genomics, Pharmacology, Immunology, Cell Biology** and 16 other domains

## Citation

```bibtex
@article{huang2025biomni,
  title={Biomni: A General-Purpose Biomedical AI Agent},
  author={Huang, Kexin and others},
  journal={bioRxiv},
  year={2025}
}
```

## License

Apache 2.0 — see [LICENSE](LICENSE).
