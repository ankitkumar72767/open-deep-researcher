def reviewer_node(state, llm):

    report = state["final_report"]

    prompt = f"""
    You are a Professional Research Reviewer.

    Evaluate the report and provide:

    # Research Score (0-100)

    # Writing Quality

    # Research Coverage

    # Strengths

    # Weaknesses

    # Suggestions

    REPORT:

    {report}
    """

    response = llm.invoke(prompt)

    return {
        "review_feedback": response.content
    }