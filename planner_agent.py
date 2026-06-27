def planner_node(state, llm):

    topic = state["topic"]

    history = state.get(
        "chat_history",
        ""
    )

    search_mode = state.get(
        "search_mode",
        "General Web"
    )

    # ==========================
    # SEARCH MODE LOGIC
    # ==========================
    if search_mode == "Academic Papers":

        mode_instruction = """
        Focus on:
        - Scientific Research Papers
        - IEEE Papers
        - Springer Papers
        - ACM Papers
        - Research PDFs
        - Peer Reviewed Journals
        """

    elif search_mode == "ArXiv":

        mode_instruction = """
        Focus ONLY on:
        - ArXiv Research Papers
        - Latest AI Research
        - Machine Learning Papers
        - Deep Learning Papers
        - Large Language Models
        - Computer Vision Research
        - NLP Research
        """

    else:

        mode_instruction = """
        Focus on:
        - General Web Information
        - Tutorials
        - Articles
        - Blogs
        - News Sources
        """

    prompt = f"""
You are an Expert Research Planner.

PREVIOUS CONVERSATION:

{history}

CURRENT USER REQUEST:

{topic}

# ==================================================
# CONTEXT ANALYSIS
# ==================================================

CASE 1:
If the current query is related to the previous conversation,
use the previous context.

CASE 2:
If the current query is unrelated,
ignore all previous context and treat it as a new topic.

# ==================================================
# TASK
# ==================================================

Generate 3 highly effective search queries.

Search Mode:

{search_mode}

Instructions:

{mode_instruction}

Rules:

1. Generate exactly 3 search queries.
2. Queries should be detailed and research-oriented.
3. Do not number the queries.
4. Return only the queries.
5. One query per line.

"""

    response = llm.invoke(prompt)

    queries = [
        q.strip()
        for q in response.content.split("\n")
        if q.strip()
    ]

    return {
        "research_plan": queries[:3]
    }
