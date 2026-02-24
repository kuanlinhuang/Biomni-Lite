"""
Biomni-Lite Gradio web UI entrypoint.

Launch with:
    python serve.py
    # or inside Docker:
    docker compose up biomni-lite-gradio
"""

import os

from biomni.agent import A1


def main():
    llm = os.getenv("BIOMNI_LLM", "claude-opus-4-5")
    path = os.getenv("BIOMNI_PATH", "./data")

    agent = A1(llm=llm, path=path)
    agent.launch()


if __name__ == "__main__":
    main()
