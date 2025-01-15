from crawl import WebCrawler
from data_extractor import TextExtractor

class IntentAi:
    def __init__(self, url: str):
        self.url = url
        self.links = []
        self.data = []
        

    def crawl_data(self):
        crawler = WebCrawler(self.url)
        self.links = crawler.crawl()

    def extract_text(self):
        extractor = TextExtractor(self.links)
        self.data = extractor.extract()
    
    