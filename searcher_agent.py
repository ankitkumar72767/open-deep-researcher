from google_scholar import search_scholar
from scholar_search import get_arxiv_papers


def searcher_node(state, tavily_client):
    """
    Executes search and returns results.
    """

    search_mode = state.get(
        "search_mode",
        "General Web"
    )

    topic = state.get(
        "topic",
        ""
    )

    queries = state.get(
        "research_plan",
        []
    )

    results = []

    # =====================================
    # GOOGLE SCHOLAR SEARCH
    # =====================================

    if search_mode == "Google Scholar":

        try:

            papers = search_scholar(topic)

            if not papers:

                return {
                    "search_results":
                    "No Google Scholar papers found."
                }

            scholar_results = []

            for paper in papers:

                scholar_results.append(
                    f"""
Title:
{paper.get('title', 'N/A')}

Authors:
{paper.get('authors', 'N/A')}

Year:
{paper.get('year', 'N/A')}

Abstract:
{paper.get('abstract', 'N/A')}

------------------------------------------------
"""
                )

            return {
                "search_results":
                "\n".join(scholar_results)
            }

        except Exception as e:

            return {
                "search_results":
                f"Google Scholar Error: {str(e)}"
            }

    # =====================================
    # ARXIV SEARCH
    # =====================================

    elif search_mode == "ArXiv":

        try:

            papers = get_arxiv_papers(topic)

            if not papers:

                return {
                    "search_results":
                    "No ArXiv papers found."
                }

            arxiv_results = []

            for paper in papers:

                arxiv_results.append(
                    f"""
Title:
{paper.get('title', 'N/A')}

Authors:
{', '.join(paper.get('authors', []))}

Summary:
{paper.get('summary', 'N/A')}

URL:
{paper.get('url', '')}

------------------------------------------------
"""
                )

            return {
                "search_results":
                "\n".join(arxiv_results)
            }

        except Exception as e:

            return {
                "search_results":
                f"ArXiv Search Error: {str(e)}"
            }

    # =====================================
    # GENERAL WEB SEARCH (TAVILY)
    # =====================================

    else:

        for q in queries:

            try:

                response = tavily_client.search(
                    query=q,
                    max_results=3,
                    search_depth="advanced"
                )

                for r in response.get(
                    "results",
                    []
                ):

                    title = r.get(
                        "title",
                        "Unknown Source"
                    )

                    url = r.get(
                        "url",
                        "#"
                    )

                    content = r.get(
                        "content",
                        ""
                    )

                    results.append(
                        f"""
Title:
{title}

URL:
{url}

Content:
{content}

------------------------------------------------
"""
                    )

            except Exception as e:

                results.append(
                    f"Error searching {q}: {str(e)}"
                )

        return {
            "search_results":
            "\n".join(results)
        }
