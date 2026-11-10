from scraper.claude_cli import call_claude

MAX_CHARS = 15000

SYSTEM_PROMPT = (
    "You are a B2B sales prospecting analyst. Analyze the given company website "
    "content and fill in the required JSON fields: what_they_sell (1-3 sentences), "
    "possible_problems (likely pain points, one per item), decision_makers (which "
    "of CEO, CFO, CTO, or Head of Sales most likely decides here, and why), and "
    "spin_questions (situation, problem, implication, and need_payoff, using the "
    "SPIN selling framework, where need_payoff creates the need for our solution: "
    "{our_solution}). If information is missing, make a reasonable inference and "
    "say so, max 20 words per one, only one question per space, with only one interrogation sign "
    "open questions without suggesting an answer , in the need payoff , make the client describe the benefit in their own words"
)

JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "what_they_sell": {"type": "string"},
        "possible_problems": {"type": "array", "items": {"type": "string"}},
        "decision_makers": {"type": "string"},
        "spin_questions": {
            "type": "object",
            "properties": {
                "situation": {"type": "string"},
                "problem": {"type": "string"},
                "implication": {"type": "string"},
                "need_payoff": {"type": "string"},
            },
            "required": ["situation", "problem", "implication", "need_payoff"],
            "additionalProperties": False,
        },
    },
    "required": ["what_they_sell", "possible_problems", "decision_makers", "spin_questions"],
    "additionalProperties": False,
}


def format_card(data):
    spin = data["spin_questions"]
    lines = [
        "WHAT THEY SELL:",
        data["what_they_sell"],
        "",
        "POSSIBLE PROBLEMS:",
        *(f"  - {problem}" for problem in data["possible_problems"]),
        "",
        "DECISION MAKERS:",
        data["decision_makers"],
        "",
        "SPIN QUESTIONS:",
        f"  Situation: {spin['situation']}",
        f"  Problem: {spin['problem']}",
        f"  Implication: {spin['implication']}",
        f"  Need-payoff: {spin['need_payoff']}",
    ]
    return "\n".join(lines)


def generate_prospect_card(our_solution, url, title, text):
    excerpt = text[:MAX_CHARS]

    system_prompt = SYSTEM_PROMPT.format(our_solution=our_solution)
    user_prompt = f"URL: {url}\nTitle: {title}\n\nWebsite text:\n{excerpt}"

    data = call_claude(system_prompt, user_prompt, model="claude-opus-5", json_schema=JSON_SCHEMA)

    return format_card(data)
