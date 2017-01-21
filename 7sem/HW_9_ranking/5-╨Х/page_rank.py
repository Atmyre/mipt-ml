def update_page_rank(graph, page_rank, damp_factor):
    new_page_rank = {url: damp_factor / len(graph) for url in graph}

    for url in graph:
        child_number = len(graph[url])

        if child_number > 0:
            for child in graph[url]:
                new_rank = (1 - damp_factor) * page_rank[url] / child_number
                new_page_rank[child] += new_rank
        else:
            new_url_rank = (1 - damp_factor) * page_rank[url]
            new_page_rank[url] += new_url_rank

    difference = sum([abs(new_page_rank[url] - page_rank[url])
                     for url in graph])
    return difference, new_page_rank.copy()


def page_rank(graph, damp_factor=0, eps=0.0005):
    page_rank = {url: float(1) / len(graph) for url in graph}

    difference = eps * 10
    while difference > eps:
        difference, page_rank = update_page_rank(graph, page_rank, damp_factor)

    return page_rank
