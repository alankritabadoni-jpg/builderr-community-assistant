import argparse
import csv
import json
import os
import sys
import time
from openai import OpenAI

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

SYSTEM_PROMPT = """You are the community assistant for Builderr (builderr.ai), \
a marketplace connecting important tasks with talented builders who can solve them.

Decide for each post:
1. should_respond: 'Yes' or 'No'
2. why: 1-2 sentence justification respecting community rules.
3. draft_response: draft message if 'Yes', or empty string if 'No'.
Never publish or post. Output JSON only: {"should_respond": "...", "why": "...", "draft_response": "..."}"""

def get_client():
    groq_key = os.environ.get("GROQ_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    if groq_key and groq_key.startswith("gsk_"):
        return OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1"), "llama-3.1-8b-instant"
    elif openai_key:
        return OpenAI(api_key=openai_key), "gpt-4o-mini"
    sys.exit("ERROR: Please set OPENAI_API_KEY or GROQ_API_KEY in your environment.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="sample_posts.csv")
    parser.add_argument("--output", default="results.csv")
    args = parser.parse_args()

    client, model = get_client()
    with open(args.input, newline="", encoding="utf-8") as f:
        posts = [r for r in csv.DictReader(f) if r.get("post_id")]

    results = []
    for row in posts:
        prompt = f"Community: {row['community']}\nContext: {row['community_context']}\nSummary: {row['post_summary']}"
        res = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        data = json.loads(res.choices[0].message.content)
        results.append({
            "post_id": row["post_id"],
            "should_respond": data.get("should_respond", "No"),
            "why": data.get("why", ""),
            "draft_response": data.get("draft_response", "")
        })

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["post_id", "should_respond", "why", "draft_response"])
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    main()