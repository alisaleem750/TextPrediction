from TextPrediction.Ngrams.Ngrams import Ngrams
from TextPrediction.DataMining.ArticleExtractor import ArticleExtractor as extractor

# This class is used to mine articles from the web (specifically the BBC News and Sky News websites. A total of 300 articles from
# BBC and 700 articles from Sky News. This gives us a total of 1000 articles from which we have taken our Ngrams using the
# emergency term. Furthermore, we have taken another 50 articles from Sky News for each of the following searches:
# hurricane, tsunami, earthquake, accident, flood, tornado, heart attack, stroke, disease, epidemic giving us another
# 500 articles. In total data was mined from 1500 articles
class MiningAndConvertingToGrams:

    def __init__(self):
        self.extractor = extractor()
        self.Ngram = Ngrams()

        #self.bbc_articles = self.extractor.get_bbc_articles()
        self.sky_articles = self.extractor.get_sky_articles(1, 5)

        #self.extract_bbctext_and_convert_to_n_grams()
        self.extract_skytext_and_convert_to_n_grams()

        #self.Ngram.load_bigrams()
        #self.Ngram.load_trigrams()

    # Extract text from Sky News articles and convert it into n-grams.
    def extract_skytext_and_convert_to_n_grams(self):
        n = len(self.sky_articles)
        for article in self.sky_articles:
            print n
            n -= 1
            text = self.extractor.get_sky_text(article[1:-1])
            self.Ngram.set_list(text)
            self.Ngram.find_trigrams(self.Ngram.get_list())
            self.Ngram.find_bigrams(self.Ngram.get_list())

    # Extract text from BBC News articles and convert it into n-grams.
    def extract_bbctext_and_convert_to_n_grams(self):
        n = len(self.bbc_articles)
        for article in self.bbc_articles:
            print n
            n -= 1
            text = self.extractor.get_bbc_text(article[1:-1])
            self.Ngram.set_list(text)
            self.Ngram.find_trigrams(self.Ngram.get_list())
            self.Ngram.find_bigrams(self.Ngram.get_list())

MiningAndConvertingToGrams()