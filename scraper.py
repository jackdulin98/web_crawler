import requests
import re
from urllib.parse import urlparse

class PyCrawler(object):
    def __init__(self, starting_url):
        self.starting_url = starting_url
        self.visited = set()

    # get html at the current link
    def get_html(self, url):
        try:
            html = requests.get(url)
        except Exception as e:
            print(e)
            return ""
        return html.content.decode('latin-1')

    # extracts links from the current page
    def get_links(self, url):
        html = self.get_html(url)
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', html)
        for i, link in enumerate(links):
            if not urlparse(link).netloc:
                link_with_base = base + link
                links[i] = link_with_base

        return set(filter(lambda x: 'mailto' not in x, links))

    # extract specific information on the page
    # in this case, meta tag information if found
    def extract_info(self, url):
        html = self.get_html(url)
        meta = re.findall("<meta .*?name=[\"'](.*?)['\"].*?content=[\"'](.*?)['\"].*?>", html)
        return dict(meta)

    # go through each of the links recursively
    # the outer-most function, starts from root link
    def crawl(self, url):
        for link in self.get_links(url):
            if link in self.visited:
                continue
            print(link)
            self.visited.add(link)
            info = self.extract_info(link)
            self.crawl(link)

    def start(self):
        self.crawl(self.starting_url)

if __name__ == "__main__":
    crawler = PyCrawler("http://lillysingh.blogspot.com")
    crawler.start()
