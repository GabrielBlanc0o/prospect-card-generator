# Prospect Card Generator

**Paste a company URL. Get a sales prospect card in seconds.**

![Python](https://img.shields.io/badge/python-3-blue)
![Powered by Claude](https://img.shields.io/badge/powered%20by-Claude-d97757)

It scrapes the site, hands the text to Claude, and prints what you need before a first call.

```
$ python main.py
Enter the company's website URL: acme.com

WHAT THEY SELL:
Cloud invoicing software for small logistics companies.

POSSIBLE PROBLEMS:
  - Manual data entry between tools
  - Slow payment collection

DECISION MAKERS:
CFO, since the product touches billing and cash flow.

SPIN QUESTIONS:
  Situation: How do you handle invoicing today?
  Problem: Where does that process slow you down?
  Implication: What happens to cash flow when invoices go out late?
  Need-payoff: What would faster invoicing let your team do?
```

*Illustrative output.*

## Quick start

```
pip install -r requirements.txt
python main.py
```

Needs Python 3 and the [Claude Code CLI](https://claude.com/claude-code), logged in. No API key.

## Make it yours

Set `OUR_SOLUTION` in `main.py` to what you sell. The need-payoff question is built around it.
