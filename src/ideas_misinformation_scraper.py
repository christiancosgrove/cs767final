import requests
import os
import string
import pandas as pd
from bs4 import BeautifulSoup, Tag
from collections import defaultdict
from util.scraper import Scraper


class IdeasMisinformationScraper(Scraper):

    def scrape(self):
        url = 'https://www.cmu.edu/ideas-social-cybersecurity/research/coronavirus.html'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        content = soup.find('div', attrs={'class', 'content'})
        data = []
        for div in content.find_all('div'):
            if not self.contains_tag('ol', div):
                # no misinformation bullets
                continue
            for d in div.find_all(['h2', 'p', 'ol']):
                if d.name == 'h2' and d.get('id') is not None:
                    # gets date added to site
                    last_updated = d.get_text()
                if d.name == 'p' and not self.contains_tag('strong', d):
                    # not misinformation topic
                    continue
                if d.name == 'p' and not any(c in string.punctuation for c in d.get_text()):
                    key = d.get_text()
                elif d.name == 'ol':
                    next_node = d
                    while next_node is not None:
                        if isinstance(next_node, Tag):
                            # print(key, next_node)
                            # print()
                            # print([tag.name for tag in next_node.find_all()])
                            for li in next_node.find_all('li'):
                                if 'Stories relating' in li.get_text() or 'Stories describing' in li.get_text():
                                    # not misinformation bullet
                                    continue
                                data.append((last_updated, key, li.get_text()))
                        next_node = next_node.nextSibling
            key = ''

        df = pd.DataFrame(data, columns=['last_updated', 'topic', 'story'])
        df.to_csv(os.path.join(self._path, self._filename), index=False)

    def contains_tag(self, tag, result_set):
        return True if tag in [tag.name for tag in result_set.find_all()] else False


def main():
    scraper = IdeasMisinformationScraper(
        path='../data/misinformation/', filename='ideas_misinformation.csv')
    scraper.scrape()


if __name__ == '__main__':
    main()
