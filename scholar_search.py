import requests
import arxiv


def search_arxiv(query):

    url = (
        "http://export.arxiv.org/api/query?"
        f"search_query=all:{query}"
        "&start=0&max_results=5"
    )

    try:
        response = requests.get(url, timeout=10)
        return response.text

    except Exception as e:
        return f"Error: {e}"


def get_arxiv_papers(query):

    papers = []

    try:

        client = arxiv.Client()

        search = arxiv.Search(
            query=query,
            max_results=5,
            sort_by=arxiv.SortCriterion.Relevance
        )

        for result in client.results(search):

            papers.append({
                "title": result.title,
                "authors": [
                    str(author)
                    for author in result.authors
                ],
                "summary": result.summary,
                "url": result.entry_id
            })

    except Exception as e:

        print(f"ArXiv Error: {e}")

    return papers