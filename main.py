from src.crawl import WebCrawler
from src.data_extractor import TextExtractor
from src.vsctore import VectorstoreUploader
from src.genai import DataLLM
class WebAi:
    def __init__(self, url: str):
        self.url = url
        self.links = []
        self.data = []
        self.vstore = None
        self.genai = None
        

    def crawl_data(self):
        crawler = WebCrawler(self.url)
        self.links = crawler.crawl()

    def extract_text(self):
        extractor = TextExtractor(self.links)
        self.data = extractor.extract()
    
    def upload_vectorstore(self):
        uploader = VectorstoreUploader(self.data, "intentjs")
        # uploader.execute()
        self.vstore = uploader.get_vstore()

    def load_ai(self):
        self.genai = DataLLM(self.vstore)

    def prerun(self):
        # self.crawl_data()
        # self.extract_text()
        self.upload_vectorstore()
        self.load_ai()

    def query(self, prompt, session_id):
        return self.genai.query(prompt, session_id)
    
if __name__ == "__main__":
    webai = WebAi("")
    webai.prerun()
    respone = webai.vstore.search("intentjs", "similarity")
    print(respone)
    # while True:
    #     query = input("Prompt: ")
    #     print("Response: " + webai.query(query, "session"))