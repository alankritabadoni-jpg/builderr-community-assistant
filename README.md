# Builderr Community Assistant

A small assistant that reads community posts and, for each one, decides:

1. **Should Builderr respond?**
2. **Why?**
3. **What should the response say?** (a draft only — nothing is ever posted or published)

`results.csv` in this repo already contains the assistant's output for the 8 posts
in `sample_posts.csv`, so you can review the results without running anything.
Instructions below are for re-running it yourself.

## How it works

`assistant.py` sends each post — its community, the community's norms, and a
summary of the post — to Grok (xAI's API), along with a system prompt that
encodes when a company voice is welcome versus unwelcome (e.g. it treats
"this community dislikes automated promotional replies" very differently from
"this is a designated hiring thread"). The model returns a decision, a reason,
and a draft reply as JSON, which gets written to a results CSV.

The assistant only ever writes drafts to a file. It has no ability to post,
comment, or publish anything anywhere.

## Setup (takes about 2 minutes)

**1. Install Python** (3.9+), if you don't already have it: https://www.python.org/downloads/
(On Mac, use `python3` and `pip3` below — plain `python`/`pip` may not exist.)

**2. Get an xAI (Grok) API key**
- Go to https://console.x.ai/
- Sign up / log in, add a payment method under Billing (a few dollars of
  credit is plenty for this task), then create a key under "API Keys"

**3. Install the dependencies**

Open a terminal in this folder and run:

```bash
pip3 install -r requirements.txt
```

**4. Add your API key**

Copy `.env.example` to a new file called `.env` and paste your key in:

```bash
cp .env.example .env
```

Then open `.env` in any text editor and replace `your-xai-api-key-here` with
your real key.

**5. Run it**

```bash
python3 assistant.py
```

This reads `sample_posts.csv` and writes `results.csv` with the assistant's
decisions and drafts, printing progress as it goes.

To run it on a different file:

```bash
python3 assistant.py --input other_posts.csv --output other_results.csv
```

Your input CSV needs these columns: `post_id, community, community_context,
post_summary`.

## Files

- `assistant.py` — the assistant
- `sample_posts.csv` — the 8 posts provided for this task
- `results.csv` — the assistant's output for those 8 posts
- `requirements.txt` — Python dependencies
- `.env.example` — template for your API key

## Design notes

- **Judgment, not "always yes."** The prompt explicitly weighs community norms
  (e.g. a community actively complaining about promotional bots gets a "No"
  even for an on-topic post) against genuine fit with Builderr's mission
  (matching builders to real tasks).
- **Drafts lead with value, not a pitch.** Builderr is mentioned only when
  directly relevant, in one short, honest sentence — never a link, never a
  hard call-to-action.
- **Structured output.** The model is asked to return JSON only, which is
  parsed directly into the CSV — no brittle text scraping.
- **Draft-only, by design.** The assistant has no posting capability at all,
  matching the requirement that it must not publish anything.
