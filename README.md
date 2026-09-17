# Builderr Community Assistant

A community triage assistant that reads incoming community posts and evaluates:
1. **Should Builderr respond?**
2. **Why?** (Grounding decisions in community rules & platform mission)
3. **What should the response say?** (Draft-only — strictly no automated publishing)

`results.csv` in this repository already contains the generated output for all 8 posts in `sample_posts.csv`.

---

## Architecture & Product Decisions

- **Respecting Community Norms**: The assistant defaults to `No` in spaces hostile to automated or promotional replies (e.g. Post 2) or standard peer-sharing threads (e.g. Post 5), protecting Builderr's brand equity.
- **Value-First Engagement**: When engaging (e.g. founders looking for developers in Post 6, or students seeking real AI projects in Post 4), replies prioritize concrete scoping questions and genuine peer advice rather than overt marketing pitches.
- **Drafts Only**: Strictly read-only triage; no publish or comment hooks exist.

---

## Setup & Running

### 1. Install Dependencies
pip3 install -r requirements.txt

### 2. Configure API Key
Copy env.example to .env and enter your key:

cp env.example .env
(Supports OPENAI_API_KEY or GROQ_API_KEY)

###3. Run the Assistant (CLI)

python3 assistant.py
To run on a custom dataset:

python3 assistant.py --input path/to/posts.csv --output path/to/results.csv


###4. Optional: Streamlit Review Dashboard
To visually review post evaluations and drafts side-by-side in your browser:

streamlit run app.py

##Repository Files
assistant.py: Core CLI batch processor and LLM decision engine

app.py: Streamlit human review interface for evaluating drafts

sample_posts.csv: Inbound test dataset containing 8 community posts

results.csv: Pre-computed evaluation decisions, rationales, and drafts

requirements.txt: Python package dependencies

env.example: Template for environment configuration
