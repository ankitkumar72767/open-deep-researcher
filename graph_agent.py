import re


STOPWORDS = {
    "Executive",
    "Summary",
    "This",
    "That",
    "Research",
    "Report",
    "Conclusion",
    "Abstract",
    "Introduction",
    "Future",
    "References",
    "Paper",
    "Papers",
    "Survey",
    "Study",
    "Studies",
    "Review",
    "Results",
    "Discussion",
    "Methodology",
    "Findings",
    "Analysis",
    "Current",
    "Recent",
    "Emerging",
    "Natural",
    "Language",
    "Processing"
}


def graph_node(state):

    report = state["final_report"]

    keywords = []

    candidates = re.findall(
        r"\b[A-Z][a-zA-Z\-]{3,}\b",
        report
    )

    for word in candidates:

        word = word.strip()

        if word in STOPWORDS:
            continue

        if len(word) < 4:
            continue

        if word not in keywords:
            keywords.append(word)

    keywords = keywords[:12]

    return {
        "graph_keywords": keywords
    }