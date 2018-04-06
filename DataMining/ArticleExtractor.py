import re as rgx
import urllib
from goose import Goose

# This class is used to extract the articles from the BBC News and Sky news website. The BBC articles are extracted using Goose
# meanwhile the Sky articles are extracted manually by looking for the line containing the JSON text for the text in the article.
class ArticleExtractor:

    # Constructor intialises Goose, which is used to extract text from the BBC articles.
    def __init__(self):
        self.goose = Goose()

    # This method takes a page URL and an HTML pattern as input. It comiples a regular expression using this pattern and then
    # opens the URL given as input. It then searches this page for instances where the pattern matches the text in the URL's
    # HTML and adds it to a list, which it returns as its output.
    def get_url_links(self, page_url, html_pattern):
        pattern = rgx.compile(html_pattern)
        htmlfile = urllib.urlopen(page_url)
        htmltext = htmlfile.read()
        links = rgx.findall(pattern, htmltext)
        list(set(links));
        return links

    # This method removes the duplicate entries in the input list.
    def remove_duplicates(self, l):
        return list(set(l))

    # This method uses the get_url_links method to extract all URL links to articles on the BBC news search page with
    # "Emergency" as search value. It then filters out the duplicate links and returns the obtained list of URLs.
    def get_bbc_articles(self):
        bbc_articles_emergency = []
        bbc_articles_emergency += self.get_url_links('http://www.bbc.co.uk/search?q=emergency&filter=news&suggid=#page=30', '"http://www.bbc.co.uk/news/.+?"')
        bbc_emergency = self.remove_duplicates(bbc_articles_emergency)
        return bbc_emergency

    # n is the number of pages we want to extract articles off from Sky news
    def get_sky_articles(self, n, m):
        sky_articles_emergency = []
        for number in range(n, n+m):
            sky_articles_emergency += self.get_url_links('http://news.sky.com/search?q=emergency&sortby=date&page='+str(number), '"http://news.sky.com/story/.+?"')
        sky_emergency = self.remove_duplicates(sky_articles_emergency)
        return sky_emergency

    # This method returns the number of articles present in the list of articles given as input.
    def get_number_of_articles(self, article_list):
        return len(article_list)

    # This method uses the goose extractor's extract feature to extrace content from a page's URL.
    def get_article(self, page_url):
        article = self.goose.extract(url=page_url)
        return article

    # This method is used to extract the text from the BBC articles using the goose extractor's features.
    def get_bbc_text(self, page_url):
        article = self.get_article(page_url)
        article_text = article.cleaned_text
        return article_text

    # This method takes the article text from the url's HTML and then takes away the whitespaces from the line
    # containing the article text. It then removes the irrelevant text in the line containing the article's text
    # and replaces the hex code for apostrophes and quotation marks with string equivalents of them.
    def get_sky_text(self, page_url):
        url = urllib.urlopen(page_url)
        text = ""
        for line in url:
            if '"articleBody": "' in line:
                text = line.lstrip()
                text = text.rstrip()
                text = text[len('"articleBody": "'):-1]
                text = text.replace("&#x27;", "'")
                text = text.replace("&quot;", '"')
        return text

