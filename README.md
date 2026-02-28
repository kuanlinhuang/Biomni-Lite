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
# On any VM with Docker (requires internet access to pull the image):
git clone <repo-url>
cd Biomni-Lite
echo "ANTHROPIC_API_KEY=your_key" > .env
docker compose up biomni-lite-gradio -d
# → Open http://<vm-ip>:7860
```

### 5. Deploy on a Restricted-Internet / Air-gapped VM

If your VM has **no or limited outbound internet access**, build the image on a
connected machine, export it as a tarball, transfer it, and load it on the VM.

**Step 1 – On an internet-connected machine** (once):

```bash
git clone <repo-url>
cd Biomni-Lite
bash scripts/save-image.sh          # builds image, writes biomni-lite.tar.gz
```

**Step 2 – Transfer the tarball to your VM** (e.g. via SCP or a USB drive):

```bash
scp biomni-lite.tar.gz user@<vm-ip>:~/Biomni-Lite/
```

**Step 3 – On the VM** (no internet required after this point):

```bash
cd ~/Biomni-Lite
bash scripts/load-and-run.sh        # loads image, prompts for .env, starts UI
# → Open http://<vm-ip>:7860
```

The helper script will:
- Load the image from the tarball (skips if already loaded)
- Create `.env` from `.env.example` if it does not exist and prompt you to fill in your API key
- Create the `workspace/` directory for run outputs
- Start `biomni-lite-gradio` in the background via `docker compose up -d`

**Change the host port** (e.g. if 7860 is blocked on your VM):

```bash
GRADIO_PORT=8080 docker compose up biomni-lite-gradio -d
# or set GRADIO_PORT=8080 in your .env file
```

**Useful commands on the VM:**

```bash
docker compose logs -f biomni-lite-gradio   # tail live logs
docker compose down                          # stop the service
docker compose up biomni-lite-gradio -d      # restart
```

### 6. Troubleshooting VPN / Corporate Networks

If you see **SSL errors** (`UNEXPECTED_EOF_WHILE_READING`) or
**connection refused** errors, your corporate VPN/firewall is likely
doing SSL inspection.

**Quick fix** — add these to your `.env`:

```bash
# Skip the selector page (avoids a server restart that can cause connection errors):
BIOMNI_AGENT=ad1

# If your organization provides a CA bundle for SSL inspection:
SSL_CERT_FILE=/path/to/corporate-ca-bundle.crt
REQUESTS_CA_BUNDLE=/path/to/corporate-ca-bundle.crt
```

Then restart: `docker compose down && docker compose up biomni-lite-gradio -d`


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
| `BIOMNI_USE_TOOL_RETRIEVER` | `false` (Docker) | Smart tool selection (extra LLM call per query) |
| `GRADIO_PORT` | `7860` | Host port for the Gradio web UI |
| `SSL_CERT_FILE` | — | Path to CA bundle for VPN/corporate SSL inspection |

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
