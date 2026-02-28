"""
Biomni-Lite Gradio web UI entrypoint.

Launch with:
    python serve.py
    # or inside Docker:
    docker compose up biomni-lite-gradio

Agent selection
---------------
Set the BIOMNI_AGENT env var to bypass the selector:
    BIOMNI_AGENT=a1   → launch A1  (general biomedical agent)
    BIOMNI_AGENT=ad1  → launch AD1 (Alzheimer's Disease agent)

When BIOMNI_AGENT is unset a landing page is shown at port 7860 so the
user can pick their agent interactively before the full UI loads.

CLI usage (no Gradio):
    python -c "from biomni.agent import A1; A1().go('your query')"
    python -c "from biomni.agent.ad1 import AD1; AD1().go('your query')"
"""

import os
import threading

# Disable Gradio analytics and set server binding before any Gradio import so
# that no external CDN calls are made at startup (required for air-gapped VMs).
os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")
os.environ.setdefault("GRADIO_SERVER_NAME", "0.0.0.0")


def main() -> None:
    llm = os.getenv("BIOMNI_LLM", "claude-opus-4-5")
    path = os.getenv("BIOMNI_PATH", "./data")
    env = os.getenv("BIOMNI_AGENT", "").strip().lower()

    # ── Direct launch via env var (skips selector) ──────────────────────────
    if env == "a1":
        from biomni.agent import A1
        A1(llm=llm, path=path).launch_gradio_demo()
        return

    if env == "ad1":
        from biomni.agent.ad1 import AD1
        AD1(llm=llm, path=path).launch_ui()
        return

    # ── Interactive selector landing page ────────────────────────────────────
    import gradio as gr

    chosen: dict = {"value": "a1"}
    ready = threading.Event()

    with gr.Blocks(title="Biomni-Lite — Select Agent") as selector:
        gr.Markdown(
            "# 🧬 Biomni-Lite\n"
            "**Choose an agent to launch:**"
        )
        with gr.Row():
            btn_a1 = gr.Button(
                "🔬 A1 — General Biomedical",
                variant="primary",
                scale=1,
            )
            btn_ad1 = gr.Button(
                "🧠 AD1 — Alzheimer's Disease",
                variant="secondary",
                scale=1,
            )
        status = gr.Markdown(
            "_A1: broad biomedical tasks &nbsp;·&nbsp; "
            "AD1: extends A1 with Alzheimer's Disease domain expertise_"
        )

        def _pick(val: str) -> str:
            chosen["value"] = val
            ready.set()
            return f"Launching **{val.upper()}**…"

        btn_a1.click(lambda: _pick("a1"), outputs=status)
        btn_ad1.click(lambda: _pick("ad1"), outputs=status)

    selector.launch(
        server_name="0.0.0.0",
        server_port=7860,
        prevent_thread_lock=True,
        share=False,
        show_api=False,
    )

    # Block until the user clicks a button
    ready.wait()
    selector.close()

    import time
    time.sleep(0.5)  # allow the selector server to shut down cleanly

    # ── Launch selected agent ────────────────────────────────────────────────
    if chosen["value"] == "ad1":
        from biomni.agent.ad1 import AD1
        AD1(llm=llm, path=path).launch_ui(server_name="0.0.0.0")
    else:
        from biomni.agent import A1
        A1(llm=llm, path=path).launch_gradio_demo(server_name="0.0.0.0")


if __name__ == "__main__":
    main()
