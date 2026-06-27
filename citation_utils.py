def generate_citation(title, author="Unknown", year="2025"):

    apa = f"{author}. ({year}). {title}."

    ieee = f"[1] {author}, \"{title}\", {year}."

    mla = f"{author}. \"{title}\". {year}."

    return {
        "APA": apa,
        "IEEE": ieee,
        "MLA": mla
    }