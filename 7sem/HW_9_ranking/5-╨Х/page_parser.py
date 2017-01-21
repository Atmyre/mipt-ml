from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse, urljoin


def is_inside_link(url, ref):
    return (urlparse(ref).netloc == urlparse(url).netloc and
            urlparse(ref).scheme == urlparse(url).scheme)


def parse_url(url, graph):
    graph[url] = set()
    page = BeautifulSoup(urlopen(url), "lxml")

    for ref in page.find_all('a'):
        next_url = urljoin(url, ref.get('href'))

        if not is_inside_link(url, next_url):
            continue
        try:
            connection = urlopen(next_url)
            graph[url].add(urljoin(url, next_url))
            connection.close()
        except Exception:
            continue


def parse_site(page, graph, max_depth=100, verbose=False):
    to_parse = [(page, 0)]
    parsed = set()
    index_to_parse = 0

    while index_to_parse < len(to_parse):
        url, depth = to_parse[index_to_parse]

        # further there are only pages with greater rank
        if depth >= max_depth:
            break

        if verbose:
            print('parsing url: %s of depth: %d' % (url, depth))

        parse_url(url, graph)

        index_to_parse += 1
        parsed.add(url)

        for ref in graph[url]:
            if ref in parsed:
                continue
            to_parse.append((ref, depth + 1))
            parsed.add(ref)
