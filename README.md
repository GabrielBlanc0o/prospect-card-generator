# Prospect Card Generator

Console tool for B2B sales prospecting. Give it a company's website URL and it
scrapes the page, then asks Claude to produce a prospect card:

- **What they sell**
- **Possible problems** (likely pain points)
- **Decision makers** (CEO, CFO, CTO or Head of Sales, and why)
- **SPIN questions** (situation, problem, implication, need-payoff)

## Requirements

- Python 3
- [Claude Code CLI](https://claude.com/claude-code) installed and logged in.
  Prompts run through `claude -p` on your subscription, so no API key is needed.

## Setup

```
pip install -r requirements.txt
```

## Run

```
python main.py
```

Enter a URL when prompted (the `https://` prefix is optional).

## Project layout

```
main.py                 entry point
scraper/core.py         fetches and parses the page
scraper/analyzer.py     prompt, JSON schema and card formatting
scraper/claude_cli.py   wrapper around the Claude Code CLI
```

To describe your own product, edit `OUR_SOLUTION` in `main.py`.
