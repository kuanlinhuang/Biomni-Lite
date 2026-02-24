# Biomni-Lite

A lightweight, containerizable biomedical AI agent powered by a strong LLM. No local data lake required — datasets are fetched on demand from Zenodo.

## Key Differences from Biomni

| Feature | Biomni | Biomni-Lite |
|---------|--------|-------------|
| Data lake | ~11GB auto-download | On-demand from Zenodo |
| Environment | Heavy conda (100+ pkgs, R, CLI) | `pip install biomni-lite` |
| Default LLM | claude-sonnet-4-5 | claude-opus-4-5 |
| Docker-ready | No | Yes |
| Tool count | 180+ | 180+ (same) |
| External API tools | Yes | Yes |

## Quick Start

```bash
pip install biomni-lite
```

```python
from biomni.agent import A1

agent = A1()  # No download on init
agent.go("Query UniProt for TP53 protein information")
agent.go("Search PubMed for recent APOE4 Alzheimer's disease papers")
agent.go("Analyze GWAS hits for type 2 diabetes")  # Downloads gwas_catalog.pkl from Zenodo on demand
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

```bash
# Copy .env.example to .env and add your API key
cp .env.example .env
# Edit .env: ANTHROPIC_API_KEY=your_key_here

# Run interactive agent
docker compose run biomni-lite python -c "
from biomni.agent import A1
agent = A1()
agent.go('List all protein-protein interaction datasets available')
"

# Run Gradio web UI
docker compose up biomni-lite-gradio
# → Open http://localhost:7860
```

### Deploy on a VM

```bash
# On any VM with Docker:
git clone <repo-url>
cd Biomni-Lite
echo "ANTHROPIC_API_KEY=your_key" > .env
docker compose up biomni-lite-gradio -d
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
