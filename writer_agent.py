def writer_node(state, llm):

    topic = state["topic"]

    data = state["search_results"]

    history = state.get(
        "chat_history",
        ""
    )

    length = state.get(
        "summary_length",
        "Detailed"
    )

    search_mode = state.get(
        "search_mode",
        "General Web"
    )

    # ==================================
    # REPORT LENGTH
    # ==================================

    if length == "Short":

        b_length_instruction = """
        Generate 400-600 words.
        Be concise and focused.
        """

    else:

        b_length_instruction = """
        Generate 1200-2000 words.
        Include deep analysis and insights.
        """

    # ==================================
    # REPORT STRUCTURES
    # ==================================

    if search_mode == "Academic Papers":

        role_desc = """
        You are a Senior Academic Researcher.
        Produce publication-quality reports.
        """

        structure = f"""
        # Title
        ## Executive Summary
        ## Abstract
        ## Literature Review
        ## Methodology
        ## Results and Discussion
        ## Research Gaps
        ## Limitations
        ## Future Scope
        ## Conclusion
        ## References

        References format:
        - [Paper Title](URL)

        {b_length_instruction}
        """

    elif search_mode == "ArXiv":

        role_desc = """
        You are an AI Research Scientist.
        Create a professional survey paper.
        """

        structure = f"""
        # Research Topic
        ## Executive Summary
        ## Top Papers Reviewed
        ## Comparative Analysis
        ## Key Contributions
        ## Technical Findings
        ## Research Trends
        ## Research Gaps
        ## Future Research Directions
        ## Conclusion
        ## References

        References format:
        - [Paper Title](URL)

        {b_length_instruction}
        """

    elif search_mode == "Google Scholar":

        role_desc = """
        You are a Literature Review Expert.
        """

        structure = f"""
        # Research Topic
        ## Executive Summary
        ## Key Papers
        ## Literature Review
        ## Comparative Analysis
        ## Research Gaps
        ## Future Scope
        ## Conclusion
        ## References

        Mention:
        - Author
        - Year
        - Findings

        {b_length_instruction}
        """

    else:

        role_desc = """
        You are an Expert Research Analyst.
        """

        structure = f"""
        # Introduction
        ## Executive Summary
        ## Key Findings
        ## Detailed Analysis
        ## Opportunities
        ## Risks
        ## Conclusion

        {b_length_instruction}
        """

    # ==================================
    # FINAL PROMPT
    # ==================================

    prompt = f"""
    {role_desc}

    PREVIOUS CONVERSATION:
    {history}

    CURRENT USER INPUT:
    {topic}

    SEARCH MODE:
    {search_mode}

    REPORT STRUCTURE:
    {structure}

    VERIFIED RESEARCH DATA:
    {data}

    RULES:

    1. Use ONLY provided data.
    2. No hallucinated references.
    3. Use professional markdown formatting.
    4. Use headings and subheadings.
    5. Start directly with report.
    6. Do not use code blocks.
    7. Highlight important findings.
    8. Include actionable insights.
    9. Write professionally.
    10. Create a clean and readable report.
    """

    response = llm.invoke(prompt)

    clean_content = (
        response.content
        .replace("```markdown", "")
        .replace("```", "")
        .strip()
    )

    return {
        "final_report": clean_content
    }
