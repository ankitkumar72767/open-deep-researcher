from scholarly import scholarly


def search_scholar(query):

    papers = []

    try:

        search_query = scholarly.search_pubs(query)

        for _ in range(5):

            paper = next(search_query)

            papers.append({
                "title": paper["bib"].get("title", "N/A"),
                "authors": paper["bib"].get("author", "N/A"),
                "year": paper["bib"].get("pub_year", "N/A"),
                "abstract": paper["bib"].get("abstract", "N/A")
            })

    except Exception as e:
        print(e)

    return papers