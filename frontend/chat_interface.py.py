import gradio as gr
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm.prompt_tuning import ask_gpt  # Import prompttuning from the llm file

# introduction text
INTRO_TEXT = """
---
💡 **Task Introduction**  
- Analyze supply chain optimization solutions
- Answer **What-if** questions
- Provide feasibility analysis based on optimization calculations
- Support multiple rounds of interaction, keeping context in mind
Our AI will provide you with intelligent parsing!
"""

# Gradio Chatbox interface
iface = gr.ChatInterface(
    fn=ask_gpt,
    title="📦 AI Supply Chain Assistant",
    description=INTRO_TEXT,
    theme="soft",
    retry_btn="🔄 resubmit",
    undo_btn="↩️ undo",
    clear_btn="Clear out",
    submit_btn="Send",
)

iface.launch()

