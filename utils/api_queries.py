# Module contains functions to deal with querying and parsing the results of the Arxiv API.
# Details of this API can be found at: arxiv.org/help/api/user-manual

import urllib3
import xml.etree.ElementTree as ET

query_start = "http://export.arxiv.org/api/query?"
namespace = {"atom": "http://www.w3.org/2005/Atom"}


def get_entry(number):
    user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) ..'}
    # Arxiv rejects requests without a user agent
    http = urllib3.PoolManager(headers=user_agent)
    query_url = query_start + f"id_list={number}"
    text = http.request("GET", query_url).data
    root = ET.fromstring(text)
    return root.find("atom:entry", namespace)


def parse_entry(entry):
    """
    Get metadata from an entry returned by API query.
    :param entry: An XML Element object
    :return: Dict of metadata
    """
    authors = entry.findall("atom:author", namespace)
    names = [author.find("atom:name", namespace).text for author in authors]
    title = entry.find("atom:title", namespace).text
    abstract = entry.find("atom:summary", namespace).text
    cat = entry.find("atom:category", namespace).find("atom:term", namespace).text
    data = {"authors": names, "title": title, "abstract": abstract, "category": cat}
    return data


if __name__ == "__main__":
    entry = get_entry("2004.01128")
    print(parse_entry(entry))
